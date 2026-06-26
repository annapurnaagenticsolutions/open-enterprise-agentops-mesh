from typing import Any
from uuid import uuid4

from app.kernel.events.models import (
    CanonicalEvent,
    EventValidation,
    ExecutionContext,
    PayloadReference,
    ServiceContext,
    TrustLevel,
)


REQUIRED_FIELDS = ["source_tool", "event_type"]


def _validation_errors(raw_event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if not raw_event.get(field):
            errors.append(f"Missing required field: {field}")
    if not (raw_event.get("build_id") or raw_event.get("pipeline_id")):
        errors.append("At least one of build_id or pipeline_id is required.")
    return errors


def normalize_pipeline_event(raw_event: dict[str, Any]) -> CanonicalEvent:
    validation_errors = _validation_errors(raw_event)

    source_tool = raw_event.get("source_tool", "unknown")
    source_event_type = raw_event.get("event_type", "pipeline_failed")
    normalized_event_type = raw_event.get("normalized_event_type", "pipeline.failed")

    repository = raw_event.get("repository")
    service_name = raw_event.get("service_name") or repository
    environment = raw_event.get("environment", "ci")
    branch = raw_event.get("branch")
    commit_sha = raw_event.get("commit_sha")
    build_id = raw_event.get("build_id")
    pipeline_id = raw_event.get("pipeline_id")
    attempt = int(raw_event.get("attempt", 1))

    idempotency_key = raw_event.get("idempotency_key")
    if not idempotency_key:
        idempotency_key = f"{source_tool}:{normalized_event_type}:{build_id or pipeline_id}:attempt_{attempt}"

    metadata = dict(raw_event.get("metadata", {}))
    if repository:
        metadata["repository"] = repository

    trust_value = raw_event.get("trust_level", "synthetic_test")

    return CanonicalEvent(
        schema_version=raw_event.get("schema_version", "devops.event.v1"),
        event_id=raw_event.get("event_id") or f"evt_{uuid4().hex[:12]}",
        correlation_id=raw_event.get("correlation_id") or f"corr_{uuid4().hex[:12]}",
        idempotency_key=idempotency_key,
        source_tool=source_tool,
        source_event_type=source_event_type,
        normalized_event_type=normalized_event_type,
        event_type=source_event_type,
        trust_level=TrustLevel(trust_value),
        service=ServiceContext(
            name=service_name,
            criticality=raw_event.get("service_criticality", metadata.get("service_criticality", "tier_3")),
            owner_team=raw_event.get("owner_team", metadata.get("owner_team")),
        ),
        execution_context=ExecutionContext(
            environment=environment,
            branch=branch,
            commit_sha=commit_sha,
            build_id=build_id,
            pipeline_id=pipeline_id,
            attempt=attempt,
        ),
        payload=PayloadReference(
            raw_payload_ref=raw_event.get("raw_payload_ref"),
            summary=raw_event.get("payload_summary"),
        ),
        validation=EventValidation(
            is_valid=not validation_errors,
            validation_errors=validation_errors,
        ),
        severity=raw_event.get("severity", "medium"),
        metadata=metadata,
    )
