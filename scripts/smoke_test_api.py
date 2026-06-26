"""Run a minimal API smoke test using FastAPI TestClient.

Usage from project root:
    python scripts/smoke_test_api.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "framework" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402
from agentops_mesh_api.main import app  # noqa: E402

client = TestClient(app)


def assert_ok(name: str, response) -> None:
    if response.status_code != 200:
        raise AssertionError(f"{name} failed: {response.status_code} {response.text}")


def main() -> None:
    checks = []
    checks.append(("health", client.get("/health")))
    checks.append(("weights", client.get("/weights")))
    checks.append(("registry", client.get("/registry/agents")))
    checks.append(("evidence", client.get("/evidence")))
    checks.append(("providers", client.get("/runtime/providers")))
    checks.append(("observability", client.get("/observability/summary")))
    checks.append(("connectors", client.get("/connectors")))
    checks.append(("procurement scenarios", client.get("/accelerators/procurement/scenarios")))
    checks.append(("security roles", client.get("/security/roles")))
    checks.append(("security tenants", client.get("/security/tenants")))
    checks.append(("security capabilities", client.get("/security/capabilities")))
    checks.append(("security posture", client.get("/security/posture")))
    checks.append(("storage posture", client.get("/storage/posture")))
    checks.append(("audit summary", client.get("/audit/summary")))
    checks.append(("audit events", client.get("/audit/events")))
    checks.append(("approvals", client.get("/approvals")))
    checks.append(("approvals readiness", client.get("/approvals/readiness")))
    checks.append(("identity providers", client.get("/identity/providers")))
    checks.append(("service identities", client.get("/identity/service-identities")))
    checks.append(("secret references", client.get("/secrets/references")))
    checks.append(("identity secrets posture", client.get("/security/identity-secrets-posture")))
    checks.append(("connector contracts", client.get("/connector-contracts")))
    checks.append(("connector dry-run runs", client.get("/connectors/dry-run/runs")))
    checks.append(("live connector readiness", client.get("/live-connectors/readiness")))
    checks.append(("live connector profiles", client.get("/live-connectors/profiles")))
    checks.append(("live connector evaluations", client.get("/live-connectors/evaluations")))
    checks.append(("provider gateway posture", client.get("/provider-gateway/posture")))
    checks.append(("provider gateway profiles", client.get("/provider-gateway/profiles")))
    checks.append(("provider gateway decisions", client.get("/provider-gateway/decisions")))
    checks.append(("model safety posture", client.get("/model-safety/posture")))
    checks.append(("model safety risk profiles", client.get("/model-safety/risk-profiles")))
    checks.append(("model safety reviews", client.get("/model-safety/reviews")))
    checks.append(("control plane capabilities", client.get("/control-plane/capabilities")))
    checks.append(("control plane api surface", client.get("/control-plane/api-surface")))
    checks.append(("openapi lite", client.get("/control-plane/openapi-lite")))
    checks.append(("contributor readiness", client.get("/control-plane/contributor-readiness")))
    checks.append(("benchmark posture", client.get("/benchmarks/posture")))
    checks.append(("benchmark scenarios", client.get("/benchmarks/scenarios")))
    checks.append(("benchmark suites", client.get("/benchmarks/suites")))
    checks.append(("benchmark summary", client.get("/benchmarks/summary")))
    checks.append(("deployment posture", client.get("/deployment/posture")))
    checks.append(("deployment profiles", client.get("/deployment/profiles")))
    checks.append(("deployment docker compose", client.get("/deployment/docker-compose")))
    checks.append(("deployment environment matrix", client.get("/deployment/environment-matrix")))
    checks.append(("deployment local dev profile", client.get("/deployment/profiles/local-dev")))
    checks.append(("deployment compose profile", client.get("/deployment/profiles/docker-compose-local")))

    checks.append(("launch readiness", client.get("/launch/readiness")))
    checks.append(("launch assets", client.get("/launch/assets")))
    checks.append(("launch storyboard", client.get("/launch/storyboard")))
    checks.append(("launch messaging", client.get("/launch/messaging")))
    checks.append(("launch linkedin drafts", client.get("/launch/linkedin-drafts")))
    checks.append(("launch publication checklist", client.get("/launch/publication-checklist")))

    checks.append(("community readiness", client.get("/community/readiness")))
    checks.append(("community intake channels", client.get("/community/intake/channels")))
    checks.append(("community intake summary", client.get("/community/intake-summary")))
    checks.append(("community use case submissions", client.get("/community/use-case-submissions")))
    checks.append(("community architecture critiques", client.get("/community/architecture-critiques")))
    checks.append(("community roadmap feedback", client.get("/community/roadmap-feedback")))
    checks.append(("community adoption feedback", client.get("/community/adoption-feedback")))


    checks.append(("public site readiness", client.get("/public-site/readiness")))
    checks.append(("public site navigation", client.get("/public-site/navigation")))
    checks.append(("public site demo paths", client.get("/public-site/demo-paths")))
    checks.append(("public site personas", client.get("/public-site/personas")))
    checks.append(("public site ux copy", client.get("/public-site/ux-copy")))
    checks.append(("public site page inventory", client.get("/public-site/page-inventory")))
    checks.append(("public site interactive report", client.get("/public-site/interactive-report")))


    checks.append(("release evidence readiness", client.get("/release-evidence/readiness")))
    checks.append(("release evidence manifest", client.get("/release-evidence/manifest")))
    checks.append(("release evidence validation snapshot", client.get("/release-evidence/validation-snapshot")))
    checks.append(("release evidence demo recording plan", client.get("/release-evidence/demo-recording-plan")))
    checks.append(("release evidence proof bundle", client.get("/release-evidence/proof-bundle")))
    checks.append(("release evidence public report", client.get("/release-evidence/public-report")))

    checks.append(("launch candidate readiness", client.get("/launch-candidate/readiness")))
    checks.append(("launch candidate manifest", client.get("/launch-candidate/manifest")))
    checks.append(("launch candidate github pages", client.get("/launch-candidate/github-pages")))
    checks.append(("launch candidate publication sequence", client.get("/launch-candidate/publication-sequence")))
    checks.append(("launch candidate checklist", client.get("/launch-candidate/checklist")))
    checks.append(("launch candidate evidence", client.get("/launch-candidate/evidence")))
    checks.append(("launch candidate social copy", client.get("/launch-candidate/social-copy")))
    checks.append(("launch candidate public report", client.get("/launch-candidate/public-report")))

    for name, response in checks:
        assert_ok(name, response)

    print(f"{len(checks)} API smoke checks passed")


if __name__ == "__main__":
    main()
