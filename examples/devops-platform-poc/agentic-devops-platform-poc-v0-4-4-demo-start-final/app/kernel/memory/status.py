from enum import Enum


class MemoryPromotionStatus(str, Enum):
    NOT_ELIGIBLE = "not_eligible"
    ACCEPTED_PENDING_VALIDATION = "accepted_pending_validation"
    VALIDATED_PROMOTED = "validated_promoted"
    REJECTED_STORED = "rejected_stored"
    VALIDATION_FAILED_STORED = "validation_failed_stored"
    DEPRECATED = "deprecated"
