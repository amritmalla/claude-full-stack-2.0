# Package Structure

Use the package structure that matches the service size and capability shape.

## Baseline Layered Structure

```text
com.example.[service]
├── config
├── controller
├── service
├── repository
├── domain
├── dto
├── mapper
├── exception
├── validation
├── security
├── observability
└── util
```

## Capability-Oriented Structure

```text
com.example.[service]
├── [capability]
│   ├── api
│   ├── application
│   ├── domain
│   └── persistence
├── config
├── security
├── observability
└── shared
```

Prefer capability-oriented structure when the service has multiple workflows, meaningful domain boundaries, or is likely to grow beyond simple CRUD.
