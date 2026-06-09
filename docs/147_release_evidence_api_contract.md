# Release Evidence API Contract

## Overview

The release evidence API exposes read-only evidence artifacts for public launch and demo recording readiness.

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/release-evidence/readiness` | Return release evidence readiness summary |
| GET | `/release-evidence/manifest` | Return evidence asset manifest |
| GET | `/release-evidence/validation-snapshot` | Return test, smoke, benchmark, and repo validation summary |
| GET | `/release-evidence/demo-recording-plan` | Return demo recording storyboard and checklist |
| GET | `/release-evidence/proof-bundle` | Return public proof bundle |
| GET | `/release-evidence/public-report` | Return consolidated public evidence report |

## Design constraints

All endpoints are read-only and deterministic. They do not trigger live provider calls, live connector execution, external telemetry, external GitHub calls, or production writes.
