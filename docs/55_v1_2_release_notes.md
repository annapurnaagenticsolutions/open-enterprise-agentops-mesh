# v1.2 Release Notes — Persistence Upgrade and Tenant-Scoped Storage

## Added

- Tenant-scoped local JSON storage adapter.
- Storage posture summary endpoint.
- Tenant dataset inspection endpoint.
- Tenant record list endpoint.
- Tenant record upsert endpoint.
- Storage migration planning endpoint.
- Storage schemas, sample tenant data, and static storage console.
- Tests for tenant isolation, upsert behavior, posture summary, and migration plan generation.

## Design intent

v1.2 does not replace all previous services with database-backed repositories. Instead, it establishes the storage boundary and tenant-scoped persistence pattern. Existing shared-local services can now be migrated one by one behind this contract.

## Validation

The backend test suite was updated to include storage tests and API smoke coverage.

## Not included

- Postgres implementation.
- Alembic migrations.
- Object storage for evidence files.
- Encryption at rest.
- OAuth/OIDC/SAML.
- Live connector-side effects.

## Next recommended release

v1.3 should add **Audit Event Bus and Decision History Consolidation** so every storage write, policy decision, governance gate, runtime execution, and sandbox action becomes one normalized audit event stream.
