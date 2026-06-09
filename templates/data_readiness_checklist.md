# Agentic Data Readiness Checklist

## Data-source inventory

- [ ] All data sources are listed
- [ ] Each source has an owner
- [ ] Each source has a sensitivity classification
- [ ] Each source has freshness metadata
- [ ] Each source has a version or update timestamp
- [ ] Draft, approved, expired, and archived content are distinguishable

## Access control

- [ ] User roles are defined
- [ ] Source-level access rules are defined
- [ ] Field-level restrictions are defined where needed
- [ ] Retrieval layer enforces access rules
- [ ] Tool layer enforces access rules
- [ ] Agent output does not expose unauthorized data

## Data quality

- [ ] Known missing fields are documented
- [ ] Duplicate records are identified
- [ ] Conflicting sources are handled
- [ ] Standard identifiers exist for key entities
- [ ] Data-quality owner is assigned

## Retrieval readiness

- [ ] Chunking strategy is defined
- [ ] Metadata strategy is defined
- [ ] Retrieval tests exist
- [ ] Citation policy exists
- [ ] Retrieval freshness is checked
- [ ] Deprecated sources are excluded or flagged

## Knowledge graph readiness

- [ ] Key entities are defined
- [ ] Relationships are defined
- [ ] Domain ontology exists or is planned
- [ ] Business rules are represented where needed
- [ ] Entity-resolution strategy exists

## Auditability

- [ ] Agent answer links to source evidence
- [ ] Retrieval events are logged
- [ ] Tool calls are logged
- [ ] Human approvals are logged
- [ ] Final output is stored with trace

## Data readiness score

| Dimension | Score 0-5 | Notes |
|---|---:|---|
| Source inventory |  |  |
| Ownership |  |  |
| Freshness |  |  |
| Access control |  |  |
| Data quality |  |  |
| Retrieval quality |  |  |
| Knowledge graph readiness |  |  |
| Auditability |  |  |

Total score:

Readiness decision:

- [ ] Not ready
- [ ] Prototype only
- [ ] Controlled pilot
- [ ] Production ready
