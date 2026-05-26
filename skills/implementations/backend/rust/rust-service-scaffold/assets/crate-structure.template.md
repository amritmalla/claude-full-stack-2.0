# Crate Structure

Use the crate structure that matches the service size and capability shape.

## Baseline Layered Structure

```text
[service-name]/
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── Makefile
├── README.md
├── config/
│   ├── default.toml
│   ├── dev.toml
│   └── prod.toml
├── migrations/
│   └── 0001_init.sql        # placeholder; filled by schema skill
└── src/
    ├── main.rs              # thin: load config, init telemetry, run server
    ├── lib.rs               # exports build_app(state) for tests
    ├── config.rs            # typed Settings + loader
    ├── app.rs               # Router construction + layer stack
    ├── telemetry.rs         # tracing + metrics init
    ├── error.rs             # AppError + IntoResponse
    ├── health.rs            # liveness/readiness handlers
    ├── routes.rs            # route registration
    ├── handlers/
    │   └── mod.rs
    ├── domain/
    │   └── mod.rs
    ├── repo/
    │   └── mod.rs
    └── dto/
        └── mod.rs
```

## Capability-Oriented Structure

```text
[service-name]/
├── Cargo.toml
├── ... (top-level files as above)
└── src/
    ├── main.rs
    ├── lib.rs
    ├── config.rs
    ├── app.rs
    ├── telemetry.rs
    ├── error.rs
    ├── health.rs
    ├── shared/
    │   └── mod.rs
    └── [capability]/
        ├── mod.rs
        ├── api.rs           # HTTP handlers + routes
        ├── application.rs   # use cases / orchestration
        ├── domain.rs        # types and rules
        └── persistence.rs   # repo against the DB
```

Prefer capability-oriented structure when the service has multiple workflows, meaningful domain boundaries, or is likely to grow beyond simple CRUD.

For larger services or when sharing types across binaries, consider a Cargo workspace with a `crates/` directory carrying one crate per capability plus a thin top-level binary. Only introduce a workspace when at least two capabilities justify the split — premature workspace fragmentation is a documented anti-pattern.
