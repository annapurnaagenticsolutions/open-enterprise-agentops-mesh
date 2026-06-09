# v2.8 Public Launch Candidate and GitHub Pages Finalization

v2.8 turns the project into a public launch candidate. It does not add live model-provider calls, live connector execution, raw secrets, production IAM, or production deployment. The release finalizes the public-facing GitHub Pages path, launch-candidate assets, publication sequence, and launch-readiness evidence.

## Why this release exists

The project is now technically broad enough. For industry presence, the next bottleneck is not another runtime feature. The bottleneck is public clarity:

- Can an executive understand the project in five minutes?
- Can an architect navigate the reference architecture quickly?
- Can a developer run the backend and inspect APIs locally?
- Can a contributor find the right intake path?
- Can the public site tell the AgentOps control-plane story without reading 150+ documents?

v2.8 answers those questions with a launch-candidate layer.

## Launch-candidate scope

v2.8 adds:

1. GitHub Pages finalization checklist.
2. Launch-candidate manifest.
3. Publication sequence model.
4. Final public checklist.
5. Release-candidate evidence summary.
6. Public launch copy assets.
7. Static launch-candidate console.
8. Read-only launch-candidate APIs.
9. Launch-candidate report generator.

## What v2.8 intentionally does not do

- No live connector execution.
- No live model-provider calls.
- No raw secrets.
- No real OIDC/SAML/JWT validation.
- No production database migration.
- No cloud deployment automation.
- No external GitHub API calls.

## Release decision

The project is ready to be treated as a **public launch candidate** once the local validation commands pass and the GitHub Pages source is configured to `/site`.
