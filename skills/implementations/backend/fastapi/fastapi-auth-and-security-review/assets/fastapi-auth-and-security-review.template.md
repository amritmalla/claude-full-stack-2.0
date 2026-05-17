# FastAPI Auth and Security Review — Reference

Use this as the canonical dependency, guard, secret-settings, and test-matrix reference when adding auth and hardening to a scaffolded FastAPI service. Placeholder tokens use `<kebab-case>` or `<PascalCase>`. The auth model is from `architecture/security`. FastAPI is a single framework; everything below is shared. Versions are pinned examples — never use unbounded specifiers.

## Directory additions (over the scaffold)

```
app/
├── auth/
│   ├── principal.py                      # typed Principal { sub, roles|scopes, ... }
│   ├── authenticate.py                   # strategy: OAuth2/OIDC | JWT-JWKS | API-key
│   ├── authorize.py                      # default-deny dependency; per-route decision
│   └── policies.py                       # RBAC/ABAC/scope model from architecture/security
├── security/
│   ├── headers.py                        # security-headers middleware: CSP + HSTS
│   ├── csrf.py                           # cookie-session state-change protection
│   └── rate_limit.py                     # auth-endpoint limiter
tests/
└── security/
    ├── test_authz_matrix.py              # positive + negative; matrix table
    └── test_token.py                     # expired / tampered / wrong-aud rejection
```

## Settings additions (extend the scaffold Settings model)

```python
# add to app/config.py Settings — choose the subset the model needs
auth_issuer: str
auth_audience: str
auth_jwks_uri: str
# OAuth2/OIDC code flow:
oauth_client_id: str
oauth_client_secret: str
# cookie session:
session_secret: str          # min length enforced; no default (required → fail-fast)
```

`.env.example` gets the same keys with placeholder values only — never a real secret.

## Principal + authentication seam fill

```python
# app/auth/principal.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Principal:
    sub: str
    roles: tuple[str, ...]      # or scopes
    tenant: str | None = None

# app/auth/authenticate.py (JWT-JWKS example)
from jose import jwt
from app.config import settings

async def authenticate(token: str) -> Principal:
    claims = jwt.decode(
        token, await _jwks(), audience=settings.auth_audience,
        issuer=settings.auth_issuer, algorithms=["RS256"],
    )  # raises on expired/tampered/wrong-aud → handler maps to 401
    return Principal(sub=claims["sub"], roles=tuple(claims.get("roles", [])))
```

This fills the scaffold principal `Depends` seam — it does not re-create settings or logging.

## Default-deny authorization dependency

```python
# app/auth/authorize.py
from fastapi import Depends, HTTPException
from app.auth.principal import Principal

def requires(decision):
    async def dep(principal: Principal | None = Depends(get_principal)) -> Principal:
        if principal is None:
            raise HTTPException(401, "unauthenticated")
        if not decision(principal):
            raise HTTPException(403, "forbidden")     # fail closed
        return principal
    return dep

# Usage — resource access bound to the principal (anti-IDOR):
@router.get("/orders/{order_id}")
async def get_order(order_id: str, p: Principal = Depends(requires(lambda p: True))):
    order = await repo.get(order_id)
    if order.owner_id != p.sub and "admin" not in p.roles:
        raise HTTPException(403, "forbidden")          # bind to principal, not id alone
```

A route with no `requires(...)` dependency is unreachable by convention — enforce in router registration.

## Hardening wiring (after the scaffold context middleware)

```python
app.add_middleware(SecurityHeadersMiddleware)  # CSP deny-by-default + HSTS
# strip server banner: uvicorn --no-server-header / Starlette response header removal
# CSRF on cookie-session state-changing routes; rate limiter dependency on /auth/*.
```

Order: request-context middleware → security headers → rate limit → auth dependency → routes, so every denial is logged with a request id.

## Authorization matrix (test file table)

| Route | Anonymous | role:user | role:user (other's resource) | role:admin |
|---|---|---|---|---|
| `GET /me` | 401 | 200 | n/a | 200 |
| `GET /orders/{id}` | 401 | 200 (own) | 403 (IDOR) | 200 |
| `POST /admin/*` | 401 | 403 | 403 | 200 |

Every cell is an assertion in `test_authz_matrix.py`. The "other's resource" column is the IDOR guard.

## Secret-rotation note (service README security section)

Document: where each secret lives in the CI/secret store, JWKS cache TTL and key-rollover behavior, session-secret rotation procedure, and the `pip-audit` cadence. No values — only the procedure and locations.

## pyproject additions (pinned examples)

```
python-jose[cryptography]==3.3.0   # or pyjwt==2.9.0
itsdangerous==2.2.0                # signed cookie sessions
pip-audit==2.7.3                   # dev: dependency vulnerability audit
```
