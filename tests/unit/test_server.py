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
    tools = await server.list_tools()
    names = [t.name for t in tools]
    # Each skill + workflow exposed as a tool, plus the two meta tools.
    assert "system-design" in names
    assert "memory-management" in names
    assert "list_skills" in names
    assert "get_skill_reference" in names
    assert len(tools) == len(load_entries()) + 2


@pytest.mark.asyncio
async def test_skill_tool_returns_body_without_duplicating_it():
    """A skill tool returns its body as text content only.

    structured_output is disabled on purpose: leaving it on repeats the whole
    document in structured_content, doubling the payload for every skill.
    """
    server = build_server()
    result = await server.call_tool("system-design", {})
    assert result.structured_content is None
    assert len(result.content) == 1
    entry = {e.name: e for e in load_entries()}["system-design"]
    assert result.content[0].text == entry.body


@pytest.mark.asyncio
async def test_reference_tool_schema_is_derived_from_signature():
    server = build_server()
    tool = next(t for t in await server.list_tools() if t.name == "get_skill_reference")
    assert set(tool.input_schema["required"]) == {"skill", "reference"}


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
