# naming-conventions

Cross-cutting naming rules. Every architecture domain, implementation, pattern, workflow, and standard MUST conform.

## Repository entities

| Entity | Pattern | Example |
|---|---|---|
| Architecture domain directory | `kebab-case`, noun phrase | `backend-architecture` |
| Implementation directory | `kebab-case`, ecosystem name | `spring-boot`, `nextjs` |
| Pattern directory | `kebab-case`, architectural noun | `event-driven`, `cqrs` |
| Workflow directory | `kebab-case`, outcome-oriented | `startup-mvp` |
| Standard directory | `kebab-case`, `-schema` or `-standards` suffix | `api-standards` |
| Skill folder | `kebab-case`, verb-led when action | `rest-api-contract-design` |
| Skill entry file | `SKILL.md` (uppercase) | `SKILL.md` |
| Supporting markdown | `kebab-case.md` | `discovery-playbook.md` |

## Skill frontmatter

Every `SKILL.md` MUST start with YAML frontmatter:

```yaml
---
name: <kebab-case identifier, matches folder name>
description: <Use when ...> One sentence. Names the trigger and the deliverable.
---
```

The `description` MUST begin with "Use when" so the agent matcher can route correctly.

## Code-facing identifiers

Apply to artifacts produced *by* skills (schemas, configs, generated code):

| Artifact | Convention |
|---|---|
| API path segments | `kebab-case` (`/user-profiles`) |
| JSON / YAML keys | `snake_case` for backend payloads; `camelCase` for frontend-facing payloads. Pick one per surface and document it. |
| Environment variables | `SCREAMING_SNAKE_CASE` |
| Database tables | `snake_case`, plural (`user_accounts`) |
| Database columns | `snake_case`, singular (`created_at`) |
| Event / Kafka topics | `dot.namespaced.lowercase` (`billing.invoice.created`) |
| Container images | `kebab-case`, registry-prefixed |
| Kubernetes resources | `kebab-case`, suffixed by kind when ambiguous (`payments-api-deploy`) |
| Terraform modules | `kebab-case`, provider-prefixed when relevant (`aws-vpc-base`) |

## Reserved suffixes

- `-schema` — declarative contract (`prd-schema`).
- `-standards` — multi-rule normative document (`api-standards`).
- `-template` — scaffolding starter (`architecture-template`).
- `-playbook` — operational procedure.

## Anti-patterns

- `snake_case` directory names.
- Trailing version suffixes in folder names (`api-v2/`). Version inside the artifact, not the path.
- Tool names in architecture domain folders (`spring-security/` inside `architecture/`). Architecture domains are ecosystem-neutral.
- Vague verbs in skill names (`do-stuff`, `helper`).
