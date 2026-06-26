# v1.2 Forward Roadmap

Recommended next release:

## v1.2 — Persistence Upgrade and Tenant-Scoped Storage

The project should now move from local JSON to a cleaner storage abstraction.

Suggested scope:

1. Storage repository interfaces.
2. SQLite starter implementation.
3. Optional Postgres-ready schema.
4. Tenant ID on agent registry, evidence vault, trace ledger, tool runs, and procurement cases.
5. Migration notes from local JSON.
6. Storage tests.
7. Security-aware query filtering.

Why v1.2 should focus on storage:

- v1.1 created tenant boundaries.
- Tenant boundaries are weak unless storage can enforce tenant scoping.
- Before real connectors or live model providers, the control plane needs reliable persistence.

Do not add live ERP, payment, email, or production connectors before tenant-scoped storage and authentication are stronger.
