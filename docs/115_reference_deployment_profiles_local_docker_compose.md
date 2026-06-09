# v2.3 Reference Deployment Profiles and Local Docker Compose

v2.3 adds deployment guidance without crossing into production infrastructure automation. The goal is to make the project easier to run, review, demo, and validate while preserving the control-plane safety boundary.

## Why this release matters

A public open-source AgentOps control plane must be easy to try. Until now, the framework had strong governance, evaluation, audit, policy, and benchmark capabilities, but the deployment story was still mostly implied. v2.3 makes the runtime path explicit through reference profiles.

## Profiles introduced

| Profile | Purpose | Live connectors | Live providers |
|---|---|---:|---:|
| `local-dev` | Python/FastAPI local contributor mode | Disabled | Disabled |
| `docker-compose-local` | Repeatable local demo mode | Disabled | Disabled |
| `public-github-pages-demo` | Static public industry presence | Not applicable | Not applicable |
| `enterprise-reference-non-prod` | Architecture planning profile for pilots | Disabled | Disabled |

## Boundary

v2.3 does not deploy cloud infrastructure, create production credentials, enable live connectors, call live model providers, or store raw secrets. It only defines reference deployment profiles and local execution scaffolding.

## Recommended usage

Use `local-dev` for contributor onboarding, `docker-compose-local` for repeatable demos, `public-github-pages-demo` for industry presence, and `enterprise-reference-non-prod` for architecture-board discussions.
