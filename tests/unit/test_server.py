import json
import pytest

from claude_full_stack_skills.server import (
    build_server,
    _do_list_skills,
    _do_get_reference,
)
from claude_full_stack_skills.loader import load_entries


def test_build_server_succeeds():
    server = build_server()
    assert server is not None


@pytest.mark.asyncio
async def test_list_tools_returns_skills_workflows_and_meta():
    server = build_server()
    handlers = getattr(server, "request_handlers", None)
    assert handlers, "server has no request handlers"
    from mcp.types import ListToolsRequest
    handler = handlers[ListToolsRequest]
    res = await handler(ListToolsRequest(method="tools/list", params=None))
    tools = list(res.root.tools)
    names = [t.name for t in tools]
    # Each skill + workflow exposed as a tool, plus two meta tools.
    assert "system-design" in names
    assert "memory-management" in names
    assert "list_skills" in names
    assert "get_skill_reference" in names
    assert len(tools) >= 85  # 83 skills + 4 workflows + 2 meta


def test_list_skills_filters_by_kind():
    entries = load_entries()
    out = _do_list_skills(entries, {"kind": "workflow"})
    payload = json.loads(out[0].text)
    assert payload["skills"] == []
    assert len(payload["workflows"]) >= 3


def test_list_skills_filters_by_contains():
    entries = load_entries()
    out = _do_list_skills(entries, {"contains": "memory"})
    payload = json.loads(out[0].text)
    all_hits = payload["skills"] + payload["workflows"]
    assert any(h["name"] == "memory-management" for h in all_hits)


def test_get_reference_returns_content():
    entries = {e.name: e for e in load_entries()}
    if "memory-management" not in entries:
        pytest.skip("memory-management skill missing")
    out = _do_get_reference(entries, {"skill": "memory-management", "reference": "setup"})
    text = out[0].text
    # The setup reference must mention the install command.
    assert "claude-repo-mem" in text
    assert "pip install" in text


def test_get_reference_unknown_skill_returns_error():
    entries = {e.name: e for e in load_entries()}
    out = _do_get_reference(entries, {"skill": "nope-not-real", "reference": "x"})
    payload = json.loads(out[0].text)
    assert "error" in payload


def test_get_reference_unknown_file_returns_available_list():
    entries = {e.name: e for e in load_entries()}
    if "memory-management" not in entries:
        pytest.skip("memory-management skill missing")
    out = _do_get_reference(entries, {"skill": "memory-management", "reference": "no-such-file"})
    payload = json.loads(out[0].text)
    assert "error" in payload
    assert "setup.md" in payload["available"]
