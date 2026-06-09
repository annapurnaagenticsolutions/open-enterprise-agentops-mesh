# GitHub Pages Finalization Guide

## Recommended Pages source

Use the repository `site/` directory as the GitHub Pages source.

Recommended entry point:

```text
site/index.html
```

Recommended supporting pages:

```text
site/control_plane_console.html
site/interactive_demo_path.html
site/public_launch_console.html
site/release_evidence_console.html
site/launch_candidate_console.html
site/api_catalog.html
site/contributor_console.html
site/community_intake_console.html
site/benchmark_console.html
site/deployment_console.html
```

## Public flow

Recommended top-level story:

```text
Problem
→ Why enterprise agents fail
→ AgentOps control plane
→ Procurement demo journey
→ Governance/policy/audit evidence
→ Open-source adoption path
→ Contributor/community intake
```

## Publication checklist

Before enabling Pages:

- Validate no fake secrets or raw credentials are present.
- Validate all static demo pages load locally.
- Validate `README.md` matches the public product narrative.
- Validate the API smoke test passes.
- Validate release evidence and launch-candidate reports pass.
- Confirm Self-Healing DevOps is excluded from this track.

## Boundary language

Every public page should preserve this boundary:

> This project is a deterministic open-source AgentOps control-plane reference implementation. Live connector execution and live model-provider execution are disabled by design in the public launch candidate.
