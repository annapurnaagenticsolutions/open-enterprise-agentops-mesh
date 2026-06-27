#!/usr/bin/env python3
"""meshctl — Command-line interface for AgentOps Mesh.

Usage:
    meshctl <command> [options]

Commands:
    govern submit    Submit a governance workflow request
    govern status    Check governance status for a use case
    registry list    List registered agents
    registry register  Register a new agent
    policy check     Check a policy against an action
    trace list       List trace events
    trace show       Show a specific trace event
    approval list    List pending approvals
    approval decide  Make an approval decision
    health           Check Mesh API health
    info             Show Mesh API info and capabilities
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Any, Sequence


class MeshctlError(Exception):
    """User-facing CLI error."""


def _api_request(base_url: str, method: str, path: str, body: dict | None = None) -> dict:
    """Make an HTTP request to the Mesh API."""
    url = f"{base_url.rstrip('/')}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            error_json = json.loads(error_body)
            detail = error_json.get("detail", error_body)
        except json.JSONDecodeError:
            detail = error_body
        raise MeshctlError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise MeshctlError(f"Cannot connect to Mesh at {base_url}: {e.reason}") from e


def cmd_health(args: argparse.Namespace) -> int:
    result = _api_request(args.mesh_url, "GET", "/health")
    print(json.dumps(result, indent=2) if args.json else f"Status: {result.get('status', 'unknown')}")
    print(f"  App: {result.get('app', 'N/A')}")
    print(f"  Version: {result.get('version', 'N/A')}")
    print(f"  Deterministic: {result.get('deterministic_mode', 'N/A')}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    result = _api_request(args.mesh_url, "GET", "/weights")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        weights = result.get("weights", {})
        print("AgentOps Mesh — Evaluation Weights:")
        for dim, weight in weights.items():
            print(f"  {dim}: {weight}")
    return 0


def cmd_govern_submit(args: argparse.Namespace) -> int:
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            request = json.load(f)
    elif args.axon_file:
        from axon.codegen.governance import generate_governance_submission
        from axon.parser import parse
        from axon.validator import validate

        source = open(args.axon_file, "r", encoding="utf-8").read()
        declarations = parse(source)
        diagnostics = validate(declarations)
        errors = [d for d in diagnostics if d.severity == "error"]
        if errors:
            for e in errors:
                print(f"error: {e}", file=sys.stderr)
            raise MeshctlError(f"AXON validation failed with {len(errors)} error(s)")

        request = generate_governance_submission(
            declarations,
            source_filename=args.axon_file,
            business_owner=args.business_owner or "TBD",
            technical_owner=args.technical_owner or "TBD",
            target_environment=args.target_environment or "pilot",
        )
    else:
        raise MeshctlError("Either --file (JSON) or --axon-file (.ax) is required")

    result = _api_request(args.mesh_url, "POST", "/governance/run", request)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Governance Decision: {result.get('overall_decision', 'N/A')}")
        print(f"  Use Case: {result.get('use_case_id', 'N/A')} — {result.get('name', 'N/A')}")
        print(f"  Readiness: {result.get('readiness_score', 'N/A')}")
        print(f"  Risk: {result.get('risk_level', 'N/A')} (score: {result.get('risk_score', 'N/A')})")
        print(f"  Stage: {result.get('current_stage', 'N/A')}")
        print()
        gates = result.get("gate_results", [])
        for gate in gates:
            status_icon = {"pass": "[OK]", "caution": "[~]", "fail": "[X]"}.get(gate.get("status", ""), "[?]")
            print(f"  {status_icon} {gate.get('gate_id', '')} {gate.get('gate_name', '')} — score: {gate.get('score', 'N/A')}")
        print()
        actions = result.get("next_actions", [])
        if actions:
            print("  Next Actions:")
            for a in actions[:5]:
                print(f"    - {a}")

    return 0 if result.get("overall_decision") != "blocked" else 1


def cmd_govern_status(args: argparse.Namespace) -> int:
    raise MeshctlError("govern status requires persistent storage (not yet implemented in deterministic mode)")


def cmd_registry_list(args: argparse.Namespace) -> int:
    result = _api_request(args.mesh_url, "GET", "/registry/agents")
    agents = result.get("agents", [])
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Registered Agents: {len(agents)}")
        for a in agents:
            print(f"  {a.get('agent_id', 'N/A')} — {a.get('name', 'N/A')} (v{a.get('version', 'N/A')})")
    return 0


def cmd_registry_register(args: argparse.Namespace) -> int:
    with open(args.file, "r", encoding="utf-8") as f:
        record = json.load(f)
    result = _api_request(args.mesh_url, "POST", "/registry/agents", record)
    print(json.dumps(result, indent=2) if args.json else f"Registered: {result.get('agent_id', 'N/A')}")
    return 0


def cmd_policy_check(args: argparse.Namespace) -> int:
    request = {
        "agent_id": args.agent_id,
        "action": args.action,
        "resource": args.resource or "",
        "context": json.loads(args.context) if args.context else {},
    }
    result = _api_request(args.mesh_url, "POST", "/policy/check", request)
    print(json.dumps(result, indent=2) if args.json else f"Policy: {result.get('decision', 'N/A')}")
    return 0 if result.get("decision") == "allow" else 1


def cmd_trace_list(args: argparse.Namespace) -> int:
    path = f"/traces?agent={args.agent}" if args.agent else "/traces"
    result = _api_request(args.mesh_url, "GET", path)
    traces = result.get("traces", [])
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Traces: {len(traces)}")
        for t in traces[:20]:
            print(f"  {t.get('event_id', 'N/A')} [{t.get('event_type', 'N/A')}] {t.get('agent_id', 'N/A')} — {t.get('timestamp', 'N/A')}")
    return 0


def cmd_approval_list(args: argparse.Namespace) -> int:
    result = _api_request(args.mesh_url, "GET", "/approvals")
    approvals = result.get("approvals", [])
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Approvals: {len(approvals)}")
        for a in approvals:
            print(f"  {a.get('approval_id', 'N/A')} — {a.get('status', 'N/A')} — {a.get('description', 'N/A')}")
    return 0


def cmd_approval_decide(args: argparse.Namespace) -> int:
    request = {
        "approval_id": args.approval_id,
        "decision": args.decision,
        "decided_by": args.decided_by,
        "comment": args.comment or "",
    }
    result = _api_request(args.mesh_url, "POST", "/approvals/decide", request)
    print(json.dumps(result, indent=2) if args.json else f"Decision: {result.get('status', 'N/A')}")
    return 0


def _make_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meshctl",
        description="AgentOps Mesh command-line interface",
    )
    parser.add_argument(
        "--mesh-url",
        default="http://localhost:8000",
        help="AgentOps Mesh API URL (default: http://localhost:8000)",
    )
    parser.add_argument("--json", action="store_true", help="output as JSON")

    subcommands = parser.add_subparsers(dest="command", required=True)

    # health
    subcommands.add_parser("health", help="check Mesh API health")

    # info
    subcommands.add_parser("info", help="show Mesh evaluation weights and capabilities")

    # govern
    govern = subcommands.add_parser("govern", help="governance workflow commands")
    govern_sub = govern.add_subparsers(dest="govern_command", required=True)

    govern_submit = govern_sub.add_parser("submit", help="submit a governance workflow request")
    govern_submit.add_argument("--file", help="path to JSON governance request file")
    govern_submit.add_argument("--axon-file", help="path to .ax file to compile and submit")
    govern_submit.add_argument("--business-owner", help="business owner name")
    govern_submit.add_argument("--technical-owner", help="technical owner name")
    govern_submit.add_argument("--target-environment", choices=["sandbox", "pilot", "production"], help="target environment")

    govern_status = govern_sub.add_parser("status", help="check governance status")
    govern_status.add_argument("use_case_id", help="use case ID to check")

    # registry
    registry = subcommands.add_parser("registry", help="agent registry commands")
    registry_sub = registry.add_subparsers(dest="registry_command", required=True)

    registry_list = registry_sub.add_parser("list", help="list registered agents")
    registry_register = registry_sub.add_parser("register", help="register a new agent")
    registry_register.add_argument("--file", required=True, help="path to agent record JSON")

    # policy
    policy = subcommands.add_parser("policy", help="policy guardrail commands")
    policy_sub = policy.add_subparsers(dest="policy_command", required=True)

    policy_check = policy_sub.add_parser("check", help="check a policy against an action")
    policy_check.add_argument("--agent-id", required=True, help="agent ID")
    policy_check.add_argument("--action", required=True, help="action to check")
    policy_check.add_argument("--resource", help="resource being accessed")
    policy_check.add_argument("--context", help="JSON context string")

    # trace
    trace = subcommands.add_parser("trace", help="trace ledger commands")
    trace_sub = trace.add_subparsers(dest="trace_command", required=True)

    trace_list = trace_sub.add_parser("list", help="list trace events")
    trace_list.add_argument("--agent", help="filter by agent ID")

    # approval
    approval = subcommands.add_parser("approval", help="approval workflow commands")
    approval_sub = approval.add_subparsers(dest="approval_command", required=True)

    approval_list = approval_sub.add_parser("list", help="list pending approvals")
    approval_decide = approval_sub.add_parser("decide", help="make an approval decision")
    approval_decide.add_argument("approval_id", help="approval ID")
    approval_decide.add_argument("--decision", required=True, choices=["approve", "reject"], help="decision")
    approval_decide.add_argument("--decided-by", required=True, help="decision maker name")
    approval_decide.add_argument("--comment", help="optional comment")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _make_arg_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "health":
            return cmd_health(args)
        if args.command == "info":
            return cmd_info(args)
        if args.command == "govern":
            if args.govern_command == "submit":
                return cmd_govern_submit(args)
            if args.govern_command == "status":
                return cmd_govern_status(args)
        if args.command == "registry":
            if args.registry_command == "list":
                return cmd_registry_list(args)
            if args.registry_command == "register":
                return cmd_registry_register(args)
        if args.command == "policy":
            if args.policy_command == "check":
                return cmd_policy_check(args)
        if args.command == "trace":
            if args.trace_command == "list":
                return cmd_trace_list(args)
        if args.command == "approval":
            if args.approval_command == "list":
                return cmd_approval_list(args)
            if args.approval_command == "decide":
                return cmd_approval_decide(args)

        parser.print_help()
        return 1
    except MeshctlError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
