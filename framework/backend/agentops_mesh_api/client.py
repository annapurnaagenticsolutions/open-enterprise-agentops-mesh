"""AgentOps Mesh Python SDK — typed client library.

Usage:
    from agentops_mesh import MeshClient

    mesh = MeshClient("http://localhost:8000")
    result = mesh.governance.run(request)
    mesh.registry.register(agent_record)
    mesh.policy.check(action="tool:Execute", agent_id="Bot")
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any


class MeshError(Exception):
    """SDK error wrapper."""


@dataclass
class GovernanceResult:
    overall_decision: str
    current_stage: str
    readiness_score: float
    certification_level: str
    risk_level: str
    risk_score: int
    gate_results: list[dict[str, Any]] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    production_readiness_report: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.overall_decision not in ("blocked", "remediate_before_pilot")

    @property
    def pilot_ready(self) -> bool:
        return self.production_readiness_report.get("pilot_ready", False)

    @property
    def production_ready(self) -> bool:
        return self.production_readiness_report.get("production_ready", False)


@dataclass
class PolicyResult:
    decision: str
    reasons: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def allowed(self) -> bool:
        return self.decision == "allow"


class GovernanceAPI:
    """Governance workflow API client."""

    def __init__(self, client: "MeshClient") -> None:
        self._client = client

    def run(self, request: dict[str, Any]) -> GovernanceResult:
        """Submit a governance workflow request."""
        result = self._client._post("/governance/run", request)
        return GovernanceResult(
            overall_decision=result.get("overall_decision", ""),
            current_stage=result.get("current_stage", ""),
            readiness_score=result.get("readiness_score", 0.0),
            certification_level=result.get("certification_level", ""),
            risk_level=result.get("risk_level", ""),
            risk_score=result.get("risk_score", 0),
            gate_results=result.get("gate_results", []),
            next_actions=result.get("next_actions", []),
            production_readiness_report=result.get("production_readiness_report", {}),
            raw=result,
        )

    def from_axon(self, axon_file: str, **overrides: Any) -> GovernanceResult:
        """Compile an .ax file and submit it for governance."""
        from axon.codegen.governance import generate_governance_submission
        from axon.parser import parse
        from axon.validator import validate

        source = open(axon_file, "r", encoding="utf-8").read()
        declarations = parse(source)
        diagnostics = validate(declarations)
        errors = [d for d in diagnostics if d.severity == "error"]
        if errors:
            raise MeshError(f"AXON validation failed: {'; '.join(str(e) for e in errors)}")

        request = generate_governance_submission(
            declarations,
            source_filename=axon_file,
            **overrides,
        )
        return self.run(request)


class RegistryAPI:
    """Agent registry API client."""

    def __init__(self, client: "MeshClient") -> None:
        self._client = client

    def list(self) -> list[dict[str, Any]]:
        """List all registered agents."""
        result = self._client._get("/registry/agents")
        return result.get("agents", [])

    def get(self, agent_id: str) -> dict[str, Any]:
        """Get a specific agent by ID."""
        return self._client._get(f"/registry/agents/{agent_id}")

    def register(self, record: dict[str, Any]) -> dict[str, Any]:
        """Register or update an agent."""
        return self._client._post("/registry/agents", record)

    def add_version(self, agent_id: str, version: dict[str, Any]) -> dict[str, Any]:
        """Add a new version to an existing agent."""
        return self._client._post(f"/registry/agents/{agent_id}/versions", version)


class PolicyAPI:
    """Policy guardrail API client."""

    def __init__(self, client: "MeshClient") -> None:
        self._client = client

    def check(
        self,
        *,
        agent_id: str,
        action: str,
        resource: str = "",
        context: dict[str, Any] | None = None,
    ) -> PolicyResult:
        """Check a policy against an action."""
        request = {
            "agent_id": agent_id,
            "action": action,
            "resource": resource,
            "context": context or {},
        }
        result = self._client._post("/policy/check", request)
        return PolicyResult(
            decision=result.get("decision", ""),
            reasons=result.get("reasons", []),
            raw=result,
        )


class TraceAPI:
    """Trace ledger API client."""

    def __init__(self, client: "MeshClient") -> None:
        self._client = client

    def list(self, agent: str | None = None) -> list[dict[str, Any]]:
        """List trace events, optionally filtered by agent."""
        path = f"/traces?agent={agent}" if agent else "/traces"
        result = self._client._get(path)
        return result.get("traces", [])

    def summary(self) -> dict[str, Any]:
        """Get observability summary."""
        return self._client._get("/observability/summary")


class ApprovalAPI:
    """Approval workflow API client."""

    def __init__(self, client: "MeshClient") -> None:
        self._client = client

    def list(self) -> list[dict[str, Any]]:
        """List pending approvals."""
        result = self._client._get("/approvals")
        return result.get("approvals", [])

    def decide(
        self,
        approval_id: str,
        decision: str,
        decided_by: str,
        comment: str = "",
    ) -> dict[str, Any]:
        """Make an approval decision."""
        return self._client._post("/approvals/decide", {
            "approval_id": approval_id,
            "decision": decision,
            "decided_by": decided_by,
            "comment": comment,
        })


class MeshClient:
    """Typed client for AgentOps Mesh API.

    Args:
        base_url: Mesh API base URL (e.g. http://localhost:8000)
    """

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.base_url = base_url.rstrip("/")
        self.governance = GovernanceAPI(self)
        self.registry = RegistryAPI(self)
        self.policy = PolicyAPI(self)
        self.trace = TraceAPI(self)
        self.approval = ApprovalAPI(self)

    def health(self) -> dict[str, Any]:
        """Check Mesh API health."""
        return self._get("/health")

    def weights(self) -> dict[str, float]:
        """Get evaluation weights."""
        return self._get("/weights").get("weights", {})

    def evaluate(self, request: dict[str, Any]) -> dict[str, Any]:
        """Evaluate an agent without running the full governance workflow."""
        return self._post("/evaluate", request)

    def classify_risk(self, request: dict[str, Any]) -> dict[str, Any]:
        """Classify risk for an agent."""
        return self._post("/classify-risk", request)

    def _get(self, path: str) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise MeshError(f"HTTP {e.code}: {body}") from e
        except urllib.error.URLError as e:
            raise MeshError(f"Cannot connect to Mesh at {self.base_url}: {e.reason}") from e

    def _post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise MeshError(f"HTTP {e.code}: {body}") from e
        except urllib.error.URLError as e:
            raise MeshError(f"Cannot connect to Mesh at {self.base_url}: {e.reason}") from e
