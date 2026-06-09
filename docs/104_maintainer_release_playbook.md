# Maintainer Release Playbook

## Release sequence

1. Define the release charter.
2. Confirm the production boundary.
3. Implement changes in docs, backend, site, schemas, and tests.
4. Run backend tests.
5. Run API smoke checks.
6. Run public repo validation.
7. Update release scorecard.
8. Update README and docs index.
9. Package and tag the release.

## Required commands

```bash
cd framework/backend
pytest
cd ../..
python scripts/smoke_test_api.py
python scripts/validate_public_repo.py
python scripts/export_openapi_lite.py
```

## Release scorecard dimensions

- install confidence
- test status
- docs clarity
- API discoverability
- contributor readiness
- security boundary clarity
- live-execution boundary clarity
- public demo readiness

## v2.1 decision

v2.1 is release-ready if tests pass, smoke checks pass, public repo validation passes, and live-execution boundaries remain explicit.
