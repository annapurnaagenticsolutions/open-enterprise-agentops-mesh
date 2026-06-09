# Contributor Workflow and Quality Gates

## Contribution principles

- Prefer deterministic logic over hidden LLM behavior in control-plane decisions.
- Preserve live-execution boundaries unless a release charter explicitly changes them.
- Keep public examples safe: no secrets, no real customer data, no irreversible actions.
- Add tests for every backend service change.
- Update site/data and documentation when a public surface changes.

## Local quality gate

```bash
cd framework/backend
pytest
cd ../..
python scripts/smoke_test_api.py
python scripts/validate_public_repo.py
```

## Pull request checklist

- [ ] Capability boundary is clear.
- [ ] Tests added or updated.
- [ ] Static site data updated if needed.
- [ ] Docs updated if behavior changed.
- [ ] No raw secrets or live credentials.
- [ ] No accidental live connector/provider execution.
- [ ] Public README remains understandable.

## Review levels

| Change type | Required review depth |
|---|---|
| Documentation typo | Light review |
| Static site copy/data | Basic review |
| Deterministic service logic | Code + test review |
| Security/identity/policy change | Security boundary review |
| Connector/provider change | Architecture + safety review |
| Live execution proposal | Release-charter review; not allowed by default |
