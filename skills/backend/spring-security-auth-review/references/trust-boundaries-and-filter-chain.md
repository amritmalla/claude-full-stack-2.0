# Trust Boundaries and Filter Chain

Use this reference to map auth boundaries and review Spring Security configuration.

## Trust boundary map

Identify:

- users,
- browser/mobile/server clients,
- API gateway or edge proxy,
- auth issuer,
- token type,
- downstream services,
- protected resources,
- tenant boundaries,
- service-to-service paths,
- machine identities.

Flag:

- authenticated-but-unauthorized requests reaching services,
- services trusting upstream auth context without re-validating,
- end-user tokens used for service-to-service calls,
- missing tenant boundary checks,
- gateway-only authorization.

If no trust boundary map exists, create a minimal structured map before continuing.

## Spring stack and version

Identify:

- Spring Boot version,
- Spring Security version,
- Servlet vs reactive stack,
- Spring Security 6 Lambda DSL vs older adapter style,
- method security configuration.

Spring Security 6+ should use Lambda DSL and `SecurityFilterChain`; `WebSecurityConfigurerAdapter` is obsolete.

Reactive applications require `SecurityWebFilterChain`; auth propagation must use Reactor Context, not ThreadLocal assumptions.

## Filter chain review

Locate all:

- `SecurityFilterChain` beans,
- `SecurityWebFilterChain` beans,
- `securityMatcher` or path matcher scopes,
- `authorizeHttpRequests` or `authorizeExchange` rules,
- custom filters,
- exception handlers,
- actuator chains.

Check for:

- overlapping matchers where earlier chains shadow later chains,
- broad `/**` matchers,
- catch-all `permitAll`,
- actuator endpoints with weaker rules,
- static resources exposed under authenticated paths,
- custom filters in the wrong order,
- missing auth on mutable endpoints.

Risk examples:

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/**").permitAll()
);
```

```java
http.authorizeExchange(exchanges -> exchanges
    .pathMatchers("/**").permitAll()
);
```

## Actuator exposure

The only commonly-public actuator endpoints are:

- `health` (and its `liveness` / `readiness` groups) — for orchestrator probes.
- `info` — if scrubbed of build identifiers that aid attacker reconnaissance.
- `prometheus` — only when reachable solely from a metrics-scraper network.

Every other actuator endpoint is sensitive and leaks production internals. Treat as authenticated-by-default:

| Endpoint | Why sensitive |
|---|---|
| `env`, `configprops` | Exposes property values including injected secrets and resolved config |
| `beans`, `mappings` | Enumerates the application surface (controllers, beans, filters) |
| `loggers` | Allows runtime log-level changes; can disable security logging |
| `heapdump`, `threaddump` | Leaks JVM memory, in-flight requests, possibly credentials in heap |
| `httpexchanges` | Leaks recent request/response pairs |
| `caches` | Lists cache names and contents metadata |
| `auditevents` | Leaks authentication and authorization history |
| `metrics` | Enumerable surface; some metrics carry tenant identifiers |
| `scheduledtasks`, `quartz` | Reveals background job topology |
| `flyway`, `liquibase` | Reveals migration history and schema state |
| `shutdown` | Direct DoS if exposed |

Reject any sensitive actuator endpoint reachable without authentication in non-dev profiles. Where the platform terminates auth at a gateway, verify the gateway's actuator policy is at least as strict as the service-level rule.
