# Contributing

## Contribution principles

This project values contributions that strengthen enterprise AgentOps discipline:

- governance clarity,
- evaluation quality,
- policy safety,
- runtime boundary enforcement,
- observability,
- connector sandboxing,
- business accelerator demonstrations.

## Before opening a pull request

1. Run backend tests.
2. Add or update documentation.
3. Avoid adding live side effects without sandbox controls.
4. Keep deterministic enforcement logic auditable.
5. Do not add Self-Healing DevOps to this track.

## Local validation

```bash
cd framework/backend
pip install -e .[dev]
pytest
```
