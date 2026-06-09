# Unified Control Plane Navigation

## Why this is needed

The project now has many modules. Without a unified navigation model, the repository can look like a collection of features rather than a coherent control plane.

## Recommended navigation order

1. **Public overview** — `README.md`, `site/index.html`
2. **Control-plane console** — `site/control_plane_console.html`
3. **End-to-end demo flow** — `platform/end_to_end_demo_flow.json`
4. **Capability map** — `platform/control_plane_capability_map.json`
5. **API surface** — `platform/api_surface_summary.json`
6. **Backend docs** — FastAPI `/docs`
7. **Accelerator demo** — `site/procurement_accelerator.html`
8. **Release scorecard** — `release/v2_0_release_scorecard.json`

## Public repo reading path

For first-time visitors:

```text
README.md
→ site/index.html
→ site/control_plane_console.html
→ docs/92_v2_0_control_plane_architecture_stabilization.md
→ docs/94_end_to_end_demo_flow.md
→ framework/backend/README.md
→ scripts/run_control_plane_demo.py
```

## Maintainer guidance

Future features must be placed under one of the control-plane capability groups:

- evaluation
- governance
- registry/evidence
- policy
- runtime
- observability/audit
- security/identity/storage
- connectors
- provider gateway
- model safety
- accelerators
- platform stabilization

If a feature does not fit these groups, it should probably not be part of this repository.
