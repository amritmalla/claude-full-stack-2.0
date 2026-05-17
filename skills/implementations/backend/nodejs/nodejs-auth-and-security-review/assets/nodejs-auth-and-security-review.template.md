# Node.js Auth and Security Review — Reference

Use this as the canonical middleware, guard, secret-config, and test-matrix reference when adding auth and hardening to a scaffolded Node.js service. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. The framework is `<framework>` from `backend-architecture.md`; the auth model is from `architecture/security`. Branch the framework-specific wiring; everything else is shared.

## Directory additions (over the scaffold)

```
src/
├── auth/
│   ├── principal.ts                      # typed Principal { sub, roles|scopes, ... }
│   ├── authenticate.ts                   # strategy: Passport | JWT-JWKS | OAuth2/OIDC
│   ├── authorize.ts                      # default-deny guard; per-route decision
│   └── policies.ts                       # RBAC/ABAC/scope model from architecture/security
├── security/
│   ├── headers.ts                        # helmet + CSP + HSTS; strip x-powered-by
│   ├── csrf.ts                           # cookie-session state-change protection
│   └── rate-limit.ts                     # auth-endpoint limiter
test/
└── security/
    ├── authz-matrix.test.ts              # positive + negative; matrix table
    └── token.test.ts                     # expired / tampered / wrong-aud rejection
```

## Config schema additions (extend the scaffold zod schema)

```ts
// add to src/config/index.ts schema — choose the subset the model needs
AUTH_ISSUER: z.string().url(),
AUTH_AUDIENCE: z.string().min(1),
AUTH_JWKS_URI: z.string().url(),
// OAuth2/OIDC code flow:
OAUTH_CLIENT_ID: z.string().min(1),
OAUTH_CLIENT_SECRET: z.string().min(1),
// cookie session:
SESSION_SECRET: z.string().min(32),
```

`.env.example` gets the same keys with placeholder values only — never a real secret.

## Principal + authentication seam fill

```ts
// src/auth/principal.ts
export interface Principal {
  sub: string;
  roles: readonly string[];   // or scopes: readonly string[]
  tenant?: string;
}

// src/auth/authenticate.ts (JWT-JWKS example with `jose`)
import { createRemoteJWKSet, jwtVerify } from 'jose';
import { config } from '../config/index.js';

const jwks = createRemoteJWKSet(new URL(config.AUTH_JWKS_URI));

export async function authenticate(token: string): Promise<Principal> {
  const { payload } = await jwtVerify(token, jwks, {
    issuer: config.AUTH_ISSUER,
    audience: config.AUTH_AUDIENCE,
  }); // throws on expired/tampered/wrong-aud → caller maps to 401
  return { sub: String(payload.sub), roles: (payload.roles as string[]) ?? [] };
}
```

This fills the scaffold principal-provider seam — it does not re-create config or logging.

## Default-deny authorization guard

```ts
// src/auth/authorize.ts
import type { Principal } from './principal.js';

export function requires(decision: (p: Principal, ctx: AuthzContext) => boolean) {
  return (p: Principal | undefined, ctx: AuthzContext) => {
    if (!p) throw new HttpError(401, 'unauthenticated');
    if (!decision(p, ctx)) throw new HttpError(403, 'forbidden'); // fail closed
  };
}

// Usage — resource access bound to the principal (anti-IDOR):
requires((p, ctx) => p.roles.includes('admin') || ctx.resource.ownerId === p.sub);
```

A route with no `requires(...)` is unreachable by convention — enforce this in route registration, not by hoping.

## Hardening wiring (scaffold app factory, after context middleware)

```ts
// Fastify: app.register(helmet, { contentSecurityPolicy: { /* deny-by-default */ } });
// Express: app.use(helmet({ hsts: true })); app.disable('x-powered-by');
// Nest:    app.use(helmet()); + a global guard for authorize()
// Plus: CSRF on cookie-session state-changing routes; rate limiter on /auth/*.
```

Order matters: request-context middleware → security headers → rate limit → auth → routes, so every denial is logged with a request id.

## Authorization matrix (test file table)

| Route | Anonymous | role:user | role:user (other's resource) | role:admin |
|---|---|---|---|---|
| `GET /me` | 401 | 200 | n/a | 200 |
| `GET /orders/:id` | 401 | 200 (own) | 403 (IDOR) | 200 |
| `POST /admin/*` | 401 | 403 | 403 | 200 |

Every cell is an assertion in `authz-matrix.test.ts`. The "other's resource" column is the IDOR guard.

## Secret-rotation note (service README security section)

Document: where each secret lives in the CI/secret store, JWKS cache TTL and key-rollover behavior, session-secret rotation procedure, and the `npm audit` cadence. No values — only the procedure and locations.
