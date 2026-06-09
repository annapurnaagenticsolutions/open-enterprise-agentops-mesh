# v1.6 Release Notes

v1.6 adds Connector Contract SDK and Dry-Run Connector Adapters.

## Added

- connector contract catalog
- connector operation model
- dry-run execution request/response models
- dry-run connector service
- dry-run run ledger
- adapter contract validation endpoint
- static connector SDK console
- tests for successful and blocked dry-run paths

## Still excluded

- live connector execution
- real ERP/ticketing/HR updates
- raw secret storage
- external vault integration
- production IAM integration
- production connector credentials

## Next release

v1.7 should add Live Connector Governance Pack, not live connector execution. The pack should define the checklist, evidence, and migration requirements for turning a dry-run adapter into a live candidate.
