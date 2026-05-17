# Node.js Service Scaffold Playbook

Load this when implementing any owned area of `nodejs-service-scaffold` or checking the anti-pattern list. It expands the operating rules and process steps in `SKILL.md` with the detail needed to produce a production-grade service shell.

## Why this workflow exists

A Node.js service scaffold done wrong takes weeks to fix: floating dependency ranges cause irreproducible CI builds; configuration read ad hoc from `process.env` fails as a runtime `undefined` deep in a request instead of at boot; a missing process-level handler turns one unhandled rejection into a silently wedged event loop; no graceful shutdown drops in-flight requests on every deploy; and observability bolted on later means the first production incident is diagnosed by guesswork.

The goal is a service that boots deterministically, fails fast on bad config, logs with request correlation, handles every error tier, and shuts down cleanly — a baseline every downstream archetype extends safely, not a working feature, not a tutorial app.

## Behavioral rules in depth

### 1. Consume architecture; do not invent it

Read `backend-architecture.md` before writing a single file. Framework (Express/Fastify/NestJS), domain boundaries, data layer, and API/event contracts are architectural decisions — not scaffold defaults. Auth provider and secret handling come from `architecture/security`. If any needed decision is missing, surface an ADR candidate before proceeding. The scaffold implements what was decided; it does not decide.

### 2. Pin every dependency — no exceptions

Use exact version pins in `package.json` (e.g. `fastify: 4.28.1`, not `^4.28.1`). Floating ranges cause version-resolution divergence between developer machines and CI. The lockfile (`package-lock.json` / `pnpm-lock.yaml`) is committed and is the sole source of truth for reproducibility. Set `engines.node` to the target LTS so a wrong runtime fails install, not production. Never add a dependency without a pinned version.

### 3. Configuration is validated at boot — never read ad hoc

A single typed config object is built once at startup by parsing `process.env` through a schema (zod or equivalent). Required variables that are missing or malformed abort the process with a clear message naming the variable — not a runtime `undefined` surfacing inside request handling hours later. The config object is frozen and imported everywhere; `process.env` is never read outside `src/config`.

### 4. All four error tiers — no fewer

Node error propagation has four independent tiers, each catching failures the others miss:

| Tier | What it catches | Where to wire |
|---|---|---|
| `process.on('uncaughtException')` | Synchronous throws with no handler on the stack | `src/server/process-handlers.ts`, before server start |
| `process.on('unhandledRejection')` | Rejected promises with no `.catch` | `src/server/process-handlers.ts`, before server start |
| Framework error handler | Errors thrown in route/middleware handlers | Express error middleware / Fastify `setErrorHandler` / Nest exception filter |
| Graceful shutdown (`SIGTERM`/`SIGINT`) | Process termination during in-flight work | `src/server/shutdown.ts`, registered before listen |

The two process handlers log fatal, flush logs, and exit non-zero — a process in an unknown state must not keep serving. The framework handler returns a structured body with no stack or internals outside dev. Graceful shutdown stops accepting connections, drains in-flight requests, closes the server and every registered resource hook within a bounded timeout, then exits. Missing any tier leaves a class of production failure unhandled.

### 5. Observability is a seam the scaffold installs, not a vendor it chooses

The pino logger and AsyncLocalStorage request context are mandatory baseline infrastructure: every log line carries a request id so a production trace is a filter, not an archaeology dig. The tracer/metrics interface is a no-op stub implementing the same shape; `nodejs-observability-readiness` replaces the stub with OpenTelemetry and prom-client. Wire the context middleware/hook first so it wraps every later handler. Reject PII field names (`email`, `token`, `password`, `authorization`) in default log serializers.

### 6. The DI seam owns the shell; auth owns the flow

Register the principal/auth-context provider as a typed shell (e.g. an `AsyncLocalStorage<Principal>` accessor, or a container-registered `PrincipalProvider` interface). Mark the deferred work explicitly with the owning archetype:

```ts
// TODO(nodejs-auth-and-security-review): verify token and populate Principal
// TODO(nodejs-auth-and-security-review): wire protected-route guard
```

The scaffold owns the registration point and the type. `nodejs-auth-and-security-review` owns the implementation. The data-layer client is registered the same way — a seam owned by the data implementation, not built here.

### 7. Liveness and readiness are different questions

`/healthz` answers "is the process up" — it returns 200 as soon as the event loop runs and must not check dependencies, or a slow database will trigger a pointless pod restart. `/readyz` answers "should this instance receive traffic" — it iterates registered dependency-check hooks and returns 503 until all pass, so a starting instance is kept out of the load balancer. Conflating them causes either restart storms or traffic to a not-ready instance.

### 8. The image references secrets — it never contains them

No `.env`, secret, key, or credential is copied into the image or committed. The container runs as a non-root user from a digest-pinned base image (`node:20.x.x-slim@sha256:...`), uses a multi-stage build so build tooling is absent from the runtime layer, and receives all configuration at runtime via environment variables. The repository holds only the reference pattern and `.env.example` with placeholders.

### 9. A broken build is not a scaffold

Run `tsc --noEmit` first — zero errors, no exceptions. Then the lint command, then the test command, then a boot smoke check: start the server, assert `GET /healthz` returns 200, shut down cleanly. If a check cannot run in the environment, document it in the README — do not declare the scaffold done on an unverified build.

## Step detail

**Step 1 — Gather context.** Load `backend-architecture.md`. Extract framework, domain boundaries, data layer, contracts, and the auth provider decision from `architecture/security`. Confirm the target directory. If a needed decision is missing, raise an ADR candidate — do not guess.

**Step 2 — Project layout.** Generate `package.json` with all deps pinned and `engines.node` set; `tsconfig.json` with `strict: true`, `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes`; ESLint config; `.gitignore` per the template. Choose the directory structure (feature-first or layered) per `backend-architecture.md`.

**Step 3 — Configuration.** Implement `src/config/index.ts`: a zod schema over `process.env`, parsed at module load, exported as a frozen typed object. On a parse failure, print the aggregated error and `process.exit(1)`. Create `.env.example` with every variable and placeholder values.

**Step 4 — Logging and request context.** Implement `src/observability/logger.ts` (pino, level from config, redaction list for PII fields), `src/observability/context.ts` (`AsyncLocalStorage<RequestContext>` with a `getRequestId()` accessor), framework middleware/hook that reads or generates an `x-request-id` and runs the rest of the request inside the context with a bound child logger, and `src/observability/telemetry.ts` (no-op `Tracer`/`Metrics` interface with TODOs naming `nodejs-observability-readiness`).

**Step 5 — Error handling.** Implement `src/server/process-handlers.ts` (`uncaughtException`, `unhandledRejection` → log fatal, flush, `process.exit(1)`), the framework error handler (structured `{ error, requestId }` body; map known error types to status; no stack outside dev), and `src/server/shutdown.ts` (`SIGTERM`/`SIGINT` → stop listener, await in-flight drain with timeout, run registered close hooks, exit).

**Step 6 — Health probes.** Implement `/healthz` (static 200) and `/readyz` (iterate a registry of `() => Promise<boolean>` dependency checks; 200 only when all pass, else 503 with the failing check names). Register both before feature routes.

**Step 7 — DI/principal seam.** Implement `src/container/index.ts` with the container from `backend-architecture.md`. Register the principal provider shell and the data-layer client placeholder. Add explicit TODO comments naming `nodejs-auth-and-security-review` and the data implementation as owners.

**Step 8 — Container packaging.** Write a multi-stage `Dockerfile` (deps → build → slim runtime), `USER node` (non-root), digest-pinned base, `HEALTHCHECK CMD` hitting `/healthz`, and a `.dockerignore` excluding `node_modules`, `.env`, tests, and source maps as appropriate.

**Step 9 — Local-run docs.** In the service README, document run commands per environment, every env var (mirrored from `.env.example`), the runtime-config contract, and the seam table from the template.

**Step 10 — Build verification and standards.** Run `tsc --noEmit`, lint, tests, boot smoke. Then check deployment-standards (env-agnostic image, non-root, runtime config), observability-standards (request-correlated structured logs, tracer seam), security-standards (no secrets, fail-fast config), naming-conventions. Document any unresolved gap explicitly — do not hide it.

## Anti-patterns to detect

Call these out explicitly when found:

- `^` or `~` version ranges anywhere in `package.json`; lockfile not committed
- `process.env.X` read directly outside `src/config`
- Config read lazily so a missing required variable fails mid-request instead of at boot
- Missing `uncaughtException` or `unhandledRejection` handler, or a handler that logs and continues instead of exiting
- No graceful shutdown — `SIGTERM` kills in-flight requests
- Framework error handler leaking a stack trace or internal message in non-dev
- `/healthz` checking the database (turns a slow dependency into a restart storm), or no separate `/readyz`
- Logging without request-id correlation; PII field names unredacted in default serializers
- Auth token/session logic implemented in the scaffold instead of delegated to `nodejs-auth-and-security-review`
- Secrets, `.env`, or credentials copied into the image; container running as root; unpinned (`:latest`) base image
- Build not verified (typecheck/lint/test/boot smoke) before declaring the scaffold complete
