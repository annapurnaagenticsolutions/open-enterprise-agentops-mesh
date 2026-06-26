from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AdapterOperationType(str, Enum):
    SAFE_READ = "safe_read"
    IDEMPOTENT_WRITE = "idempotent_write"
    NON_IDEMPOTENT_WRITE = "non_idempotent_write"
    HIGH_RISK_WRITE = "high_risk_write"


class AdapterStatus(str, Enum):
    SUCCESS = "success"
    TRANSIENT_FAILURE = "transient_failure"
    TERMINAL_FAILURE = "terminal_failure"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"


class AdapterResult(BaseModel):
    adapter: str
    operation: str
    operation_type: AdapterOperationType
    status: AdapterStatus
    idempotency_key: str | None = None
    duration_ms: int = 0
    retry_count: int = 0
    error_code: str | None = None
    error_message: str | None = None
    result: dict[str, Any] = Field(default_factory=dict)
