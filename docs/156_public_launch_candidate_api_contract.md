# Public Launch Candidate API Contract

v2.8 adds read-only launch-candidate endpoints.

## Endpoints

```text
GET /launch-candidate/readiness
GET /launch-candidate/manifest
GET /launch-candidate/github-pages
GET /launch-candidate/publication-sequence
GET /launch-candidate/checklist
GET /launch-candidate/evidence
GET /launch-candidate/social-copy
GET /launch-candidate/public-report
```

## Design principles

- Read-only.
- Deterministic.
- No external API calls.
- No GitHub API integration.
- No live provider calls.
- No live connector execution.

## Response intent

The endpoints expose enough structured data to support:

- public launch review,
- GitHub Pages publication readiness,
- social launch preparation,
- demo-readiness proof,
- maintainer release review.
