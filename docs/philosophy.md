# Philosophy

## AI-native, not AI-assisted

Most "AI for code" repositories collect prompts. This plugin ships *skills* — imperative recipes that Claude executes end-to-end, with defined inputs, deterministic outputs, and verifiable quality checks. A skill is invocable, not just readable.

## Production over prototype

The differentiation here is not "Claude can write a Hello World." It is the parts of software engineering most AI repos skip: production hardening, supply-chain security, observability, on-call ergonomics, and incident response. The first 12 skills bias hard toward that — five of them are pure DevOps/SRE.

## One reference example per stack

Every skill is exercised against a single reference service (`orders-api` on Spring Boot in v0.1). When you read a skill, you can look at the `.skill-outputs/` directory and see exactly what running it produces. This prevents skills from drifting into generic advice.

## Composable, not monolithic

Skills are independent units. Workflows sequence them. If you only need observability work, invoke `observability-readiness` alone. If you are taking a service from idea to production, run the capstone workflow that chains all 12. There is no orchestration framework — Claude reads the workflow and invokes the skills.

## Quality bar over volume

v0.1 ships 12 skills, not 600. Each is invoked end-to-end against the reference service before merge, and each has binary-verifiable quality checks. Scaling skill count without that gate produces a plausible-looking but unusable plugin. The roadmap deliberately adds skills slowly.

## Stability promise

Skill `name`, `description`, and output contracts stabilize at v1.0. Until then, names and outputs may change; pin to a specific version if that matters for your workflow.
