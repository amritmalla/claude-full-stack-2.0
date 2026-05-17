# Node.js Service Scaffold — Layout Reference

Use this as the canonical directory-layout, configuration, and entry-point reference when generating a Node.js service scaffold. Placeholder tokens use `<kebab-case>` or `<PascalCase>` style. The framework is `<framework>` from `backend-architecture.md` (Express, Fastify, or NestJS) — branch the framework-specific files accordingly; everything else is framework-agnostic.

## Directory tree

```
<service-name>/
├── package.json                          # all deps pinned — no ^ or ~; engines.node set
├── package-lock.json                     # (or pnpm-lock.yaml) committed
├── tsconfig.json                         # strict: true, noUncheckedIndexedAccess
├── .eslintrc.cjs                         # lint config
├── .gitignore                            # covers .env, node_modules, dist, coverage
├── .dockerignore                         # excludes node_modules, .env, tests
├── .env.example                          # documents env vars; placeholder values only
├── Dockerfile                            # multi-stage, non-root, digest-pinned base
├── src/
│   ├── main.ts                           # composition root + bootstrap (see pattern below)
│   ├── config/
│   │   └── index.ts                      # zod schema over process.env; frozen typed config
│   ├── server/
│   │   ├── app.ts                        # framework app factory (<framework>-specific)
│   │   ├── process-handlers.ts           # uncaughtException + unhandledRejection
│   │   ├── error-handler.ts              # framework error handler (<framework>-specific)
│   │   └── shutdown.ts                    # SIGTERM/SIGINT graceful drain
│   ├── observability/
│   │   ├── logger.ts                     # pino; level from config; PII redaction
│   │   ├── context.ts                    # AsyncLocalStorage<RequestContext>
│   │   └── telemetry.ts                  # no-op Tracer/Metrics seam (TODO: observability skill)
│   ├── health/
│   │   └── probes.ts                     # /healthz (liveness) + /readyz (readiness registry)
│   ├── container/
│   │   └── index.ts                      # DI container (<container> from backend-architecture.md)
│   └── modules/
│       └── <domain>/                     # one directory per domain (per backend-architecture.md)
├── test/
│   └── smoke.test.ts                     # boot → GET /healthz 200 → clean shutdown
```

## package.json stub

```json
{
  "name": "<service-name>",
  "version": "1.0.0",
  "engines": { "node": ">=20.11.0 <21" },
  "type": "module",
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --max-warnings 0",
    "test": "vitest run",
    "start": "node dist/main.js"
  },
  "dependencies": {
    "pino": "9.3.2",
    "zod": "3.23.8"
  },
  "devDependencies": {
    "typescript": "5.5.4",
    "vitest": "2.0.5",
    "eslint": "9.9.0"
  }
}
```

Framework dependency added per `backend-architecture.md`: `fastify: 4.28.1` / `express: 4.21.0` / `@nestjs/core: 10.4.1` (+ platform). All versions are pinned examples — replace with the exact current stable release at scaffold time. Never use `^` or `~`.

## config/index.ts pattern

```ts
import { z } from 'zod';

const schema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']).default('development'),
  PORT: z.coerce.number().int().positive().default(3000),
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug']).default('info'),
  SHUTDOWN_TIMEOUT_MS: z.coerce.number().int().positive().default(10_000),
  // Add required secrets/URLs here — no defaults for required secrets.
});

const parsed = schema.safeParse(process.env);
if (!parsed.success) {
  // eslint-disable-next-line no-console
  console.error('Invalid configuration:', parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const config = Object.freeze(parsed.data);
export type Config = typeof config;
```

## Bootstrap pattern (src/main.ts)

```ts
import { config } from './config/index.js';
import { logger } from './observability/logger.js';
import { registerProcessHandlers } from './server/process-handlers.js';
import { createApp } from './server/app.js';
import { registerShutdown } from './server/shutdown.js';

registerProcessHandlers(logger); // uncaughtException + unhandledRejection → exit non-zero

const app = await createApp();   // framework app w/ context middleware, probes, error handler
const server = app.listen(config.PORT, () =>
  logger.info({ port: config.PORT, env: config.NODE_ENV }, 'service listening'),
);

registerShutdown(server, logger); // SIGTERM/SIGINT → drain → close hooks → exit
```

`createApp` is the only framework-specific file: Fastify (`fastify()` + `setErrorHandler` + hooks), Express (`express()` + error middleware last), or NestJS (`NestFactory.create` + exception filter + `enableShutdownHooks`). The context middleware/hook runs first; `/healthz` and `/readyz` register before feature routes.

## Dockerfile stub

```dockerfile
# Build stage
FROM node:20.11.0-slim@sha256:<digest> AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:20.11.0-slim@sha256:<digest> AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY --from=build /app/dist ./dist
USER node
HEALTHCHECK --interval=30s --timeout=3s CMD node -e "fetch('http://localhost:'+(process.env.PORT||3000)+'/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "dist/main.js"]
```

No secrets baked. Runtime config arrives via environment. Replace `<digest>` with the pinned base-image digest at scaffold time.

## Seams for downstream archetypes

Document these explicitly in the service README:

| Seam | File | Filled by |
|---|---|---|
| Token verification, session, route guards | `src/container/index.ts` (principal shell + TODO) | `nodejs-auth-and-security-review` |
| OpenTelemetry tracing + prom-client metrics | `src/observability/telemetry.ts` (no-op stub) | `nodejs-observability-readiness` |
| Queue/broker producers and consumers | `src/container/index.ts` (no client registered) | `nodejs-queue-and-event-integration` |
| Backpressure, circuit breakers, load-test gates | server + CI configuration | `nodejs-performance-and-resilience` |
| Data-layer client (Prisma/Drizzle/TypeORM) | `src/container/index.ts` (placeholder) | data-layer implementation per `backend-architecture.md` |

## .gitignore additions (secrets and build)

```
# Secrets and environment
.env
.env.*
!.env.example

# Node build and deps
node_modules/
dist/
build/
coverage/
*.tsbuildinfo

# Logs
*.log
```
