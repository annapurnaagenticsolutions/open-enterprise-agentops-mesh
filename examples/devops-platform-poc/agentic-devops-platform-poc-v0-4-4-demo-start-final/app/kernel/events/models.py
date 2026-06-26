from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class TrustLevel(str, Enum):
    SIGNED_WEBHOOK = "signed_webhook"
    API_POLL = "api_poll"
    MANUAL_UPLOAD = "manual_upload"
    SYNTHETIC_TEST = "synthetic_test"


class ServiceContext(BaseModel):
    name: str | None = None
    criticality: str = "tier_3"
    owner_team: str | None = None


class ExecutionContext(BaseModel):
    environment: str = "ci"
    branch: str | None = None
    commit_sha: str | None = None
    build_id: str | None = None
    pipeline_id: str | None = None
    attempt: int = 1


class PayloadReference(BaseModel):
    raw_payload_ref: str | None = None
    summary: str | None = None


class EventValidation(BaseModel):
    is_valid: bool = True
    validation_errors: list[str] = Field(default_factory=list)


class CanonicalEvent(BaseModel):
    # CanonicalEventV1. Kept as CanonicalEvent for backward compatibility with v0.1 imports.
    schema_version: str = "devops.event.v1"
    event_id: str = Field(default_factory=lambda: f"evt_{uuid4().hex[:12]}")
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid4().hex[:12]}")
    idempotency_key: str | None = None

    source_tool: str
    source_event_type: str = "pipeline_failed"
    normalized_event_type: str = "pipeline.failed"
    event_type: str = "pipeline_failed"

    trust_level: TrustLevel = TrustLevel.SYNTHETIC_TEST
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    occurred_at: datetime | None = None

    service: ServiceContext = Field(default_factory=ServiceContext)
    execution_context: ExecutionContext = Field(default_factory=ExecutionContext)
    payload: PayloadReference = Field(default_factory=PayloadReference)
    validation: EventValidation = Field(default_factory=EventValidation)

    severity: str = "medium"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def service_name(self) -> str | None:
        return self.service.name

    @property
    def environment(self) -> str:
        return self.execution_context.environment

    @property
    def branch(self) -> str | None:
        return self.execution_context.branch

    @property
    def commit_sha(self) -> str | None:
        return self.execution_context.commit_sha

    @property
    def build_id(self) -> str | None:
        return self.execution_context.build_id

    @property
    def pipeline_id(self) -> str | None:
        return self.execution_context.pipeline_id

    @property
    def repository(self) -> str | None:
        return self.metadata.get("repository")

    @property
    def raw_payload_ref(self) -> str | None:
        return self.payload.raw_payload_ref
