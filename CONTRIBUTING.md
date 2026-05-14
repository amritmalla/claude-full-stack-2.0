# Contributing

Thank you for considering a contribution. This document describes how to propose, author, and ship a new skill or workflow.

## Flow

1. **Open an issue** using the *Skill Proposal* template. Include the proposed name (kebab-case), the target architecture domain or implementation directory, when-to-use paragraph, and expected outputs.
2. **Wait for a maintainer to claim or assign.** This avoids duplicate work.
3. **Open a PR** that includes:
   - For technology-agnostic skills: `architecture/<domain>/<name>/SKILL.md`.
   - For ecosystem-specific skills: `implementations/<category>/<ecosystem>/<name>/SKILL.md`.
   - Either way, follow [`SKILL_SPEC.md`](SKILL_SPEC.md). See [`docs/architecture/research.md`](docs/architecture/research.md) for the architecture-vs-implementations distinction.
   - The skill's example output committed under `examples/spring-boot/orders-api/.skill-outputs/<name>/`.
   - An entry added under the relevant domain or ecosystem in [`docs/architecture/registry.md`](docs/architecture/registry.md) (the single source of truth for domain/ecosystem charter and skill index). Per-directory `README.md` files inside `architecture/<domain>/` or `implementations/<category>/<ecosystem>/` are deprecated.
   - An Output contract section in `SKILL.md` linking to any [`standards/`](standards/) the skill conforms to.
   - The PR description must include **3 should-match** and **2 should-NOT-match** trigger prompts, with your manual verification result for each.
4. **Review.** One maintainer reviews. CI must be green (`validate-skills.sh` + markdown lint).
5. **Squash-merge** with `skill: add <name>` (or `workflow: …`, `docs: …`, `chore: …` as appropriate).

## Authoring rules (summary)

See [`SKILL_SPEC.md`](SKILL_SPEC.md) for the full contract.

- `description` is load-bearing. Starts with "Use when", ≤ 1024 characters.
- `name` matches the directory name exactly.
- Quality checks are binary-verifiable.
- One skill = one repeatable job.
- `SKILL.md` ≤ ~400 lines; overflow moves to `references/`.

## Governance

v0.1 is single-maintainer. CODEOWNERS will be added in v0.2 once contributor volume grows. RFC process will be defined alongside.

## License

By contributing, you agree your contributions are licensed under the MIT License (see [`LICENSE`](LICENSE)).
