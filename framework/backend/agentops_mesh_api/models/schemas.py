from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field, field_validator


class SensitivityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ImpactLevel(str, Enum):
    none = "none"
    low = "low"
    medium = "medium"
    high = "high"


class ReversibilityLevel(str, Enum):
    easy = "easy"
    moderate = "moderate"
    hard = "hard"


class TargetEnvironment(str, Enum):
    sandbox = "sandbox"
    pilot = "pilot"
    production = "production"


class GateStatus(str, Enum):
    pass_ = "pass"
    caution = "caution"
    fail = "fail"


class RiskFactors(BaseModel):
    data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    external_action: bool = False
    financial_impact: ImpactLevel = ImpactLevel.none
    reversibility: ReversibilityLevel = ReversibilityLevel.easy
    customer_or_employee_impact: ImpactLevel = ImpactLevel.none


class EvaluationScores(BaseModel):
    business_value: float = Field(ge=0, le=100)
    task_suitability: float = Field(ge=0, le=100)
    data_readiness: float = Field(ge=0, le=100)
    governance_readiness: float = Field(ge=0, le=100)
    evaluation_coverage: float = Field(ge=0, le=100)
    safety_security: float = Field(ge=0, le=100)
    human_in_loop: float = Field(ge=0, le=100)
    operational_readiness: float = Field(ge=0, le=100)
    open_architecture_fit: float = Field(ge=0, le=100)


class AgentEvaluationRequest(BaseModel):
    use_case_id: str
    name: str
    domain: str
    description: str = ""
    autonomy_level: int = Field(ge=0, le=5)
    risk_factors: RiskFactors
    scores: EvaluationScores

    @field_validator("use_case_id", "name", "domain")
    @classmethod
    def must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class GovernanceWorkflowRequest(AgentEvaluationRequest):
    business_owner: str
    technical_owner: str
    target_environment: TargetEnvironment = TargetEnvironment.pilot
    submitted_artifacts: List[str] = Field(default_factory=list)

    @field_validator("business_owner", "technical_owner")
    @classmethod
    def owners_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("owner cannot be empty")
        return value.strip()


class DimensionResult(BaseModel):
    dimension: str
    raw_score: float
    weight: float
    weighted_score: float


class RiskClassificationResponse(BaseModel):
    risk_level: str
    risk_score: int
    required_controls: List[str]


class EvaluationResponse(BaseModel):
    use_case_id: str
    name: str
    domain: str
    total_score: float
    certification_level: str
    decision: str
    risk_level: str
    required_controls: List[str]
    dimension_results: List[DimensionResult]
    blockers: List[str]
    recommendations: List[str]


class GovernanceGateResult(BaseModel):
    gate_id: str
    gate_name: str
    status: GateStatus
    score: float
    decision: str
    reasons: List[str]
    recommendations: List[str]
    required_artifacts: List[str] = Field(default_factory=list)
    hard_blocking: bool = False


class ProductionReadinessReport(BaseModel):
    summary: str
    pilot_ready: bool
    production_ready: bool
    required_before_pilot: List[str]
    required_before_production: List[str]
    suggested_pilot_guardrails: List[str]


class GovernanceWorkflowResponse(BaseModel):
    use_case_id: str
    name: str
    domain: str
    target_environment: TargetEnvironment
    overall_decision: str
    current_stage: str
    readiness_score: float
    certification_level: str
    risk_level: str
    risk_score: int
    required_controls: List[str]
    gate_results: List[GovernanceGateResult]
    next_actions: List[str]
    production_readiness_report: ProductionReadinessReport


class AgentLifecycleStatus(str, Enum):
    proposed = "proposed"
    intake_review = "intake_review"
    pilot_candidate = "pilot_candidate"
    pilot = "pilot"
    production_candidate = "production_candidate"
    production = "production"
    suspended = "suspended"
    retired = "retired"


class ReviewStatus(str, Enum):
    draft = "draft"
    submitted = "submitted"
    approved = "approved"
    rejected = "rejected"
    needs_update = "needs_update"


class EvidenceType(str, Enum):
    use_case_canvas = "use_case_canvas"
    data_inventory = "data_inventory"
    evaluation_report = "evaluation_report"
    governance_checklist = "governance_checklist"
    risk_assessment = "risk_assessment"
    security_review = "security_review"
    human_approval_record = "human_approval_record"
    monitoring_plan = "monitoring_plan"
    production_runbook = "production_runbook"
    incident_report = "incident_report"
    business_case = "business_case"


class AgentVersionRecord(BaseModel):
    version: str
    change_summary: str
    evaluation_score: float | None = Field(default=None, ge=0, le=100)
    changed_by: str
    changed_at: str = ""
    model_changes: List[str] = Field(default_factory=list)
    governance_changes: List[str] = Field(default_factory=list)

    @field_validator("version", "change_summary", "changed_by")
    @classmethod
    def version_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class AgentRegistryRecord(BaseModel):
    agent_id: str
    name: str
    domain: str
    business_process: str
    description: str = ""
    business_owner: str
    technical_owner: str
    status: AgentLifecycleStatus = AgentLifecycleStatus.proposed
    autonomy_level: int = Field(ge=0, le=5)
    risk_level: str = "Medium"
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    model_strategy: Dict[str, object] = Field(default_factory=dict)
    data_sources: List[str] = Field(default_factory=list)
    tool_scopes: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    linked_evidence_ids: List[str] = Field(default_factory=list)
    versions: List[AgentVersionRecord] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    @field_validator("agent_id", "name", "domain", "business_process", "business_owner", "technical_owner")
    @classmethod
    def registry_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("risk_level")
    @classmethod
    def risk_level_must_be_allowed(cls, value: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if value not in allowed:
            raise ValueError(f"risk_level must be one of {sorted(allowed)}")
        return value


class EvidenceRecord(BaseModel):
    evidence_id: str
    agent_id: str
    artifact_type: EvidenceType
    title: str
    summary: str = ""
    source_uri: str = ""
    owner: str
    review_status: ReviewStatus = ReviewStatus.draft
    created_at: str = ""
    tags: List[str] = Field(default_factory=list)

    @field_validator("evidence_id", "agent_id", "title", "owner")
    @classmethod
    def evidence_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class AgentRegistryListResponse(BaseModel):
    agents: List[AgentRegistryRecord]


class EvidenceListResponse(BaseModel):
    evidence: List[EvidenceRecord]


class GovernanceDecisionRecord(BaseModel):
    decision_id: str
    agent_id: str
    gate_id: str
    decision: str
    rationale: str = ""
    required_actions: List[str] = Field(default_factory=list)
    linked_evidence_ids: List[str] = Field(default_factory=list)
    decided_by: str
    decided_at: str = ""


class WeightsResponse(BaseModel):
    weights: Dict[str, int]


class PolicyDecision(str, Enum):
    allow = "allow"
    allow_with_controls = "allow_with_controls"
    require_approval = "require_approval"
    deny = "deny"


class PolicySeverity(str, Enum):
    info = "info"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class PolicyCheckRequest(BaseModel):
    agent_id: str
    actor_role: str
    action: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    autonomy_level: int = Field(ge=0, le=5)
    risk_level: str = "Medium"
    data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    requested_tools: List[str] = Field(default_factory=list)
    requested_data_sources: List[str] = Field(default_factory=list)
    output_destination: str = "internal"
    financial_impact: ImpactLevel = ImpactLevel.none
    has_human_approval: bool = False
    evidence_ids: List[str] = Field(default_factory=list)
    purpose: str = ""
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("agent_id", "actor_role", "action")
    @classmethod
    def policy_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("risk_level")
    @classmethod
    def policy_risk_level_must_be_allowed(cls, value: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if value not in allowed:
            raise ValueError(f"risk_level must be one of {sorted(allowed)}")
        return value


class PolicyViolation(BaseModel):
    policy_id: str
    policy_name: str
    category: str
    severity: PolicySeverity
    decision: PolicyDecision
    rationale: str
    required_controls: List[str] = Field(default_factory=list)
    required_evidence: List[str] = Field(default_factory=list)


class PolicyCheckResponse(BaseModel):
    agent_id: str
    decision: PolicyDecision
    allowed: bool
    severity: PolicySeverity
    required_controls: List[str]
    required_evidence: List[str]
    violations: List[PolicyViolation]
    audit_summary: str
    next_actions: List[str]



class RuntimeExecutionDecision(str, Enum):
    executed = "executed"
    executed_with_controls = "executed_with_controls"
    blocked_pending_approval = "blocked_pending_approval"
    blocked = "blocked"


class ProviderModelInfo(BaseModel):
    model_id: str
    display_name: str
    context_window: int = Field(ge=1)
    supports_tools: bool = False
    recommended_for: List[str] = Field(default_factory=list)


class ProviderInfo(BaseModel):
    provider_id: str
    display_name: str
    provider_type: str
    deployment_mode: str
    data_residency: str
    cost_tier: str
    allowed_environments: List[str]
    capabilities: List[str]
    models: List[ProviderModelInfo]
    restrictions: List[str] = Field(default_factory=list)


class ProviderRegistryResponse(BaseModel):
    version: str
    providers: List[ProviderInfo]


class RuntimeExecutionRequest(BaseModel):
    agent_id: str
    actor_role: str
    action: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    autonomy_level: int = Field(ge=0, le=5)
    risk_level: str = "Medium"
    data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    requested_tools: List[str] = Field(default_factory=list)
    requested_data_sources: List[str] = Field(default_factory=list)
    output_destination: str = "internal"
    financial_impact: ImpactLevel = ImpactLevel.none
    has_human_approval: bool = False
    evidence_ids: List[str] = Field(default_factory=list)
    purpose: str = ""
    prompt: str
    system_prompt: str = ""
    preferred_provider: str | None = None
    preferred_model: str | None = None
    max_budget_usd: float | None = Field(default=None, ge=0)
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("agent_id", "actor_role", "action", "prompt")
    @classmethod
    def runtime_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("risk_level")
    @classmethod
    def runtime_risk_level_must_be_allowed(cls, value: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if value not in allowed:
            raise ValueError(f"risk_level must be one of {sorted(allowed)}")
        return value


class RuntimeTraceStep(BaseModel):
    stage: str
    status: str
    summary: str
    details: Dict[str, object] = Field(default_factory=dict)


class RuntimeExecutionResponse(BaseModel):
    request_id: str
    agent_id: str
    execution_decision: RuntimeExecutionDecision
    allowed: bool
    policy_decision: PolicyDecision
    provider_name: str | None = None
    model_name: str | None = None
    response_text: str = ""
    blocked_reason: str = ""
    required_controls: List[str] = Field(default_factory=list)
    required_evidence: List[str] = Field(default_factory=list)
    token_estimate: int = 0
    estimated_cost_usd: float = 0.0
    audit_trace: List[RuntimeTraceStep]
    next_actions: List[str] = Field(default_factory=list)



class TraceLedgerRecord(BaseModel):
    request_id: str
    agent_id: str
    action: str
    target_environment: TargetEnvironment
    execution_decision: RuntimeExecutionDecision
    allowed: bool
    policy_decision: PolicyDecision
    provider_name: str | None = None
    model_name: str | None = None
    token_estimate: int = Field(default=0, ge=0)
    estimated_cost_usd: float = Field(default=0.0, ge=0)
    blocked_reason: str = ""
    required_controls: List[str] = Field(default_factory=list)
    required_evidence: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    audit_trace: List[RuntimeTraceStep] = Field(default_factory=list)
    created_at: str = ""
    tags: List[str] = Field(default_factory=list)

    @field_validator("request_id", "agent_id", "action")
    @classmethod
    def trace_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class TraceLedgerListResponse(BaseModel):
    traces: List[TraceLedgerRecord]


class ObservabilitySummaryResponse(BaseModel):
    total_traces: int
    executed_count: int
    executed_with_controls_count: int
    blocked_count: int
    blocked_pending_approval_count: int
    total_token_estimate: int
    total_estimated_cost_usd: float
    agents_observed: List[str]
    provider_usage: Dict[str, int]
    policy_decisions: Dict[str, int]
    recent_blocked_actions: List[TraceLedgerRecord] = Field(default_factory=list)


class AgentRuntimeReportResponse(BaseModel):
    agent_id: str
    total_runs: int
    allowed_runs: int
    blocked_runs: int
    total_token_estimate: int
    total_estimated_cost_usd: float
    latest_decision: str = "none"
    recent_traces: List[TraceLedgerRecord] = Field(default_factory=list)



class ToolRiskLevel(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Critical = "Critical"


class SideEffectClass(str, Enum):
    read_only = "read_only"
    draft_only = "draft_only"
    reversible_write = "reversible_write"
    irreversible_action = "irreversible_action"
    system_of_record_update = "system_of_record_update"


class ConnectorToolInfo(BaseModel):
    tool_id: str
    display_name: str
    description: str = ""
    risk_level: ToolRiskLevel = ToolRiskLevel.Medium
    side_effect_class: SideEffectClass = SideEffectClass.read_only
    requires_human_approval: bool = False
    allowed_environments: List[str]
    required_controls: List[str] = Field(default_factory=list)


class ConnectorInfo(BaseModel):
    connector_id: str
    display_name: str
    connector_type: str
    deployment_mode: str = "mock_local"
    allowed_environments: List[str]
    data_classes: List[str] = Field(default_factory=list)
    restrictions: List[str] = Field(default_factory=list)
    tools: List[ConnectorToolInfo] = Field(default_factory=list)


class ConnectorRegistryResponse(BaseModel):
    version: str
    connectors: List[ConnectorInfo]


class ToolSandboxDecision(str, Enum):
    dry_run_allowed = "dry_run_allowed"
    simulated_execution_allowed = "simulated_execution_allowed"
    blocked_pending_approval = "blocked_pending_approval"
    blocked = "blocked"


class ToolSandboxExecutionRequest(BaseModel):
    agent_id: str
    actor_role: str
    connector_id: str
    tool_id: str
    action: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    autonomy_level: int = Field(ge=0, le=5)
    risk_level: str = "Medium"
    data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    requested_data_sources: List[str] = Field(default_factory=list)
    payload: Dict[str, object] = Field(default_factory=dict)
    dry_run: bool = True
    simulate_side_effects: bool = False
    has_human_approval: bool = False
    evidence_ids: List[str] = Field(default_factory=list)
    purpose: str = ""
    output_destination: str = "internal"
    financial_impact: ImpactLevel = ImpactLevel.none
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("agent_id", "actor_role", "connector_id", "tool_id", "action")
    @classmethod
    def tool_request_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("risk_level")
    @classmethod
    def tool_risk_level_must_be_allowed(cls, value: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if value not in allowed:
            raise ValueError(f"risk_level must be one of {sorted(allowed)}")
        return value


class ToolSandboxExecutionResponse(BaseModel):
    request_id: str
    agent_id: str
    connector_id: str
    tool_id: str
    decision: ToolSandboxDecision
    allowed: bool
    side_effects_permitted: bool = False
    policy_decision: PolicyDecision
    simulated_result: str = ""
    blocked_reason: str = ""
    required_controls: List[str] = Field(default_factory=list)
    required_evidence: List[str] = Field(default_factory=list)
    audit_trace: List[RuntimeTraceStep] = Field(default_factory=list)
    tool_metadata: Dict[str, object] = Field(default_factory=dict)
    next_actions: List[str] = Field(default_factory=list)


class ToolSandboxRunRecord(ToolSandboxExecutionResponse):
    action: str
    target_environment: TargetEnvironment
    dry_run: bool
    simulate_side_effects: bool
    created_at: str = ""


class ToolSandboxRunListResponse(BaseModel):
    runs: List[ToolSandboxRunRecord]



class ProcurementRequestedAction(str, Enum):
    compare_po_invoice = "compare_po_invoice"
    draft_vendor_exception = "draft_vendor_exception"


class ProcurementValidationStatus(str, Enum):
    pass_ = "pass"
    caution = "caution"
    fail = "fail"


class ProcurementControlPlaneRequest(BaseModel):
    agent_id: str
    actor_role: str
    case_id: str
    target_environment: TargetEnvironment = TargetEnvironment.pilot
    autonomy_level: int = Field(ge=0, le=5)
    has_human_approval: bool = False
    evidence_ids: List[str] = Field(default_factory=list)
    po_number: str
    invoice_number: str
    challan_number: str = ""
    vendor_id: str
    vendor_name: str
    invoice_amount: float = Field(ge=0)
    po_amount: float = Field(ge=0)
    currency: str = "INR"
    invoice_quantity: float = Field(ge=0)
    challan_quantity: float = Field(ge=0)
    received_quantity: float = Field(ge=0)
    vendor_tax_id_match: bool = True
    po_vendor_match: bool = True
    goods_receipt_available: bool = True
    contract_terms_available: bool = True
    requested_action: ProcurementRequestedAction = ProcurementRequestedAction.compare_po_invoice
    create_exception_draft: bool = False
    dry_run: bool = True
    notes: str = ""
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("agent_id", "actor_role", "case_id", "po_number", "invoice_number", "vendor_id", "vendor_name")
    @classmethod
    def procurement_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ProcurementValidationResult(BaseModel):
    status: ProcurementValidationStatus
    discrepancy_count: int
    discrepancy_summary: List[str]
    amount_variance: float
    amount_variance_percent: float
    quantity_variance: float
    suggested_action: str
    controls_triggered: List[str] = Field(default_factory=list)


class ProcurementReadinessReport(BaseModel):
    lifecycle_outcome: str
    overall_decision: str
    business_value_summary: str
    risk_summary: str
    blockers: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    required_evidence: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    linked_trace_ids: List[str] = Field(default_factory=list)


class ProcurementCaseRecord(BaseModel):
    case_id: str
    agent_id: str
    po_number: str
    invoice_number: str
    vendor_id: str
    validation_status: ProcurementValidationStatus
    lifecycle_outcome: str
    governance_decision: str
    policy_decision: PolicyDecision
    runtime_request_id: str = ""
    tool_request_ids: List[str] = Field(default_factory=list)
    amount_variance: float = 0.0
    discrepancy_count: int = 0
    created_at: str = ""
    tags: List[str] = Field(default_factory=list)


class ProcurementControlPlaneResponse(BaseModel):
    case_id: str
    agent_id: str
    validation_result: ProcurementValidationResult
    governance_result: GovernanceWorkflowResponse
    policy_result: PolicyCheckResponse
    runtime_result: RuntimeExecutionResponse
    tool_results: List[ToolSandboxExecutionResponse]
    readiness_report: ProcurementReadinessReport
    case_record: ProcurementCaseRecord


class ProcurementCaseListResponse(BaseModel):
    cases: List[ProcurementCaseRecord]


class ProcurementScenarioListResponse(BaseModel):
    scenarios: List[Dict[str, object]]



class TenantStatus(str, Enum):
    active = "active"
    restricted = "restricted"
    suspended = "suspended"


class TenantIsolationMode(str, Enum):
    logical_local_json = "logical_local_json"
    shared_database = "shared_database"
    tenant_scoped_schema = "tenant_scoped_schema"
    dedicated_database = "dedicated_database"
    dedicated_runtime_recommended = "dedicated_runtime_recommended"


class AccessDecision(str, Enum):
    allow = "allow"
    allow_with_controls = "allow_with_controls"
    deny = "deny"


class SecurityRoleRecord(BaseModel):
    role_id: str
    display_name: str
    description: str = ""
    permissions: List[str] = Field(default_factory=list)
    risk_ceiling: str = "Medium"
    allowed_environments: List[str] = Field(default_factory=list)

    @field_validator("role_id", "display_name")
    @classmethod
    def role_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class TenantBoundaryRecord(BaseModel):
    tenant_id: str
    display_name: str
    status: TenantStatus = TenantStatus.active
    allowed_domains: List[str] = Field(default_factory=list)
    allowed_environments: List[str] = Field(default_factory=list)
    data_residency: str = "configurable"
    isolation_mode: str = "logical_local_json"
    max_autonomy_level: int = Field(default=2, ge=0, le=5)
    allowed_risk_levels: List[str] = Field(default_factory=lambda: ["Low", "Medium"])
    required_controls: List[str] = Field(default_factory=list)
    notes: str = ""

    @field_validator("tenant_id", "display_name")
    @classmethod
    def tenant_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class SecurityCapabilityRecord(BaseModel):
    capability_id: str
    display_name: str
    endpoint_patterns: List[str] = Field(default_factory=list)
    minimum_role_hint: str = ""
    side_effect: str = "none"

    @field_validator("capability_id", "display_name")
    @classmethod
    def capability_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class AccessCheckRequest(BaseModel):
    tenant_id: str
    actor_id: str
    actor_role: str
    capability: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    risk_level: str = "Medium"
    autonomy_level: int = Field(ge=0, le=5)
    agent_id: str = ""
    domain: str = ""
    requested_data_sources: List[str] = Field(default_factory=list)
    requested_tools: List[str] = Field(default_factory=list)
    purpose: str = ""
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "actor_id", "actor_role", "capability")
    @classmethod
    def access_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("risk_level")
    @classmethod
    def access_risk_level_must_be_allowed(cls, value: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if value not in allowed:
            raise ValueError(f"risk_level must be one of {sorted(allowed)}")
        return value


class AccessCheckResponse(BaseModel):
    tenant_id: str
    actor_id: str
    actor_role: str
    capability: str
    decision: AccessDecision
    allowed: bool
    required_controls: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    boundary_violations: List[str] = Field(default_factory=list)
    audit_summary: str
    next_actions: List[str] = Field(default_factory=list)


class RoleCatalogResponse(BaseModel):
    version: str
    roles: List[SecurityRoleRecord]


class TenantCatalogResponse(BaseModel):
    version: str
    tenants: List[TenantBoundaryRecord]


class CapabilityCatalogResponse(BaseModel):
    version: str
    capabilities: List[SecurityCapabilityRecord]


class SecurityPostureSummaryResponse(BaseModel):
    version: str
    tenant_count: int
    role_count: int
    capability_count: int
    production_capabilities: List[str]
    high_risk_roles: List[str]
    required_platform_controls: List[str]



class StorageMode(str, Enum):
    shared_local_json = "shared_local_json"
    tenant_scoped_local_json = "tenant_scoped_local_json"
    sqlite_ready = "sqlite_ready"
    postgres_ready = "postgres_ready"


class StorageDataset(str, Enum):
    agents = "agents"
    evidence = "evidence"
    runtime_traces = "runtime_traces"
    tool_sandbox_runs = "tool_sandbox_runs"
    procurement_cases = "procurement_cases"
    governance_decisions = "governance_decisions"
    access_decisions = "access_decisions"
    policy_decisions = "policy_decisions"


class TenantScopedDatasetRecord(BaseModel):
    tenant_id: str
    dataset: StorageDataset
    filename: str
    record_count: int = Field(ge=0)
    isolation_status: str = "tenant_scoped"
    controls: List[str] = Field(default_factory=list)
    last_inspected_at: str = ""


class StoragePostureResponse(BaseModel):
    version: str
    storage_mode: StorageMode
    tenant_count: int
    dataset_count: int
    total_records: int
    datasets: List[TenantScopedDatasetRecord]
    findings: List[str] = Field(default_factory=list)
    recommended_migrations: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)


class TenantDatasetListResponse(BaseModel):
    tenant_id: str
    datasets: List[TenantScopedDatasetRecord]


class TenantRecordListResponse(BaseModel):
    tenant_id: str
    dataset: StorageDataset
    records: List[Dict[str, object]]


class TenantRecordUpsertRequest(BaseModel):
    record_id_field: str = "id"
    record: Dict[str, object]

    @field_validator("record_id_field")
    @classmethod
    def record_id_field_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("record_id_field cannot be empty")
        return value.strip()


class TenantRecordUpsertResponse(BaseModel):
    tenant_id: str
    dataset: StorageDataset
    status: str
    storage_path: str
    record_count: int
    record_id_field: str
    record_id: str
    audit_summary: str


class StorageMigrationPlanRequest(BaseModel):
    source_mode: StorageMode = StorageMode.tenant_scoped_local_json
    target_mode: StorageMode = StorageMode.postgres_ready
    tenants: List[str] = Field(default_factory=list)
    datasets: List[StorageDataset] = Field(default_factory=list)
    include_backout_plan: bool = True


class StorageMigrationPlanResponse(BaseModel):
    source_mode: StorageMode
    target_mode: StorageMode
    migration_ready: bool
    phases: List[str]
    blockers: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    validation_checks: List[str] = Field(default_factory=list)
    backout_plan: List[str] = Field(default_factory=list)



class AuditEventType(str, Enum):
    identity_simulation = "identity_simulation"
    secret_access_decision = "secret_access_decision"
    governance_decision = "governance_decision"
    evaluation_decision = "evaluation_decision"
    policy_decision = "policy_decision"
    runtime_execution = "runtime_execution"
    tool_sandbox_execution = "tool_sandbox_execution"
    access_decision = "access_decision"
    storage_write = "storage_write"
    evidence_update = "evidence_update"
    agent_registry_update = "agent_registry_update"
    accelerator_case_decision = "accelerator_case_decision"
    manual_review = "manual_review"


class AuditDecisionOutcome(str, Enum):
    allow = "allow"
    allow_with_controls = "allow_with_controls"
    require_approval = "require_approval"
    deny = "deny"
    informational = "informational"


class AuditEventRecord(BaseModel):
    event_id: str = ""
    tenant_id: str
    actor_id: str
    actor_role: str
    agent_id: str = ""
    event_type: AuditEventType
    source_system: str
    capability: str = ""
    action: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    decision_outcome: AuditDecisionOutcome
    allowed: bool
    policy_decision: str | None = None
    risk_level: str = "Medium"
    autonomy_level: int = Field(default=0, ge=0, le=5)
    subject_type: str = ""
    subject_id: str = ""
    related_case_id: str = ""
    related_request_ids: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    rationale: str = ""
    required_controls: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    created_at: str = ""
    metadata: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "actor_id", "actor_role", "source_system", "action")
    @classmethod
    def audit_required_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("risk_level")
    @classmethod
    def audit_risk_level_must_be_allowed(cls, value: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if value not in allowed:
            raise ValueError(f"risk_level must be one of {sorted(allowed)}")
        return value


class AuditEventListResponse(BaseModel):
    events: List[AuditEventRecord]


class AuditEventIngestResponse(BaseModel):
    event: AuditEventRecord
    status: str
    audit_summary: str


class AuditSummaryResponse(BaseModel):
    version: str
    total_events: int
    tenant_count: int
    agent_count: int
    event_type_counts: Dict[str, int]
    decision_outcome_counts: Dict[str, int]
    approval_or_denial_count: int
    required_controls_observed: List[str]
    recent_blocked_events: List[AuditEventRecord] = Field(default_factory=list)
    findings: List[str] = Field(default_factory=list)


class DecisionHistoryResponse(BaseModel):
    subject_type: str
    subject_id: str
    total_events: int
    events: List[AuditEventRecord]
    summary: Dict[str, object]



class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    changes_requested = "changes_requested"
    cancelled = "cancelled"
    expired = "expired"


class ApprovalDecisionValue(str, Enum):
    approved = "approved"
    rejected = "rejected"
    changes_requested = "changes_requested"


class ApprovalRequestCreate(BaseModel):
    tenant_id: str
    requester_id: str
    requester_role: str
    agent_id: str
    connector_id: str
    tool_id: str
    action: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    risk_level: str = "Medium"
    autonomy_level: int = Field(ge=0, le=5)
    side_effect_class: str = "read_only"
    reason: str
    evidence_ids: List[str] = Field(default_factory=list)
    related_request_ids: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    payload_summary: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "requester_id", "requester_role", "agent_id", "connector_id", "tool_id", "action", "reason")
    @classmethod
    def approval_request_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("risk_level")
    @classmethod
    def approval_risk_level_must_be_allowed(cls, value: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if value not in allowed:
            raise ValueError(f"risk_level must be one of {sorted(allowed)}")
        return value


class ApprovalDecisionRequest(BaseModel):
    reviewer_id: str
    reviewer_role: str
    decision: ApprovalDecisionValue
    rationale: str
    conditions: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)

    @field_validator("reviewer_id", "reviewer_role", "rationale")
    @classmethod
    def approval_decision_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ApprovalRecord(BaseModel):
    approval_id: str
    tenant_id: str
    requester_id: str
    requester_role: str
    agent_id: str
    connector_id: str
    tool_id: str
    action: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    risk_level: str = "Medium"
    autonomy_level: int = Field(ge=0, le=5)
    side_effect_class: str = "read_only"
    status: ApprovalStatus = ApprovalStatus.pending
    reason: str = ""
    requested_at: str = ""
    reviewed_at: str = ""
    reviewer_id: str = ""
    reviewer_role: str = ""
    decision_rationale: str = ""
    conditions: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    related_request_ids: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    payload_summary: Dict[str, object] = Field(default_factory=dict)

    @field_validator("approval_id", "tenant_id", "requester_id", "requester_role", "agent_id", "connector_id", "tool_id", "action")
    @classmethod
    def approval_record_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ApprovalListResponse(BaseModel):
    approvals: List[ApprovalRecord]


class ApprovalRequestResponse(BaseModel):
    approval: ApprovalRecord
    audit_summary: str
    next_actions: List[str] = Field(default_factory=list)


class ApprovalDecisionResponse(BaseModel):
    approval: ApprovalRecord
    audit_summary: str
    next_actions: List[str] = Field(default_factory=list)


class ApprovalReadinessResponse(BaseModel):
    version: str
    total_approvals: int
    pending_count: int
    approved_count: int
    rejected_count: int
    changes_requested_count: int
    live_connector_status: str
    ready_controls: List[str] = Field(default_factory=list)
    remaining_controls: List[str] = Field(default_factory=list)
    findings: List[str] = Field(default_factory=list)



class PrincipalType(str, Enum):
    human_user = "human_user"
    service_account = "service_account"
    agent_runtime = "agent_runtime"
    connector_service = "connector_service"
    system = "system"


class IdentityTrustLevel(str, Enum):
    unauthenticated = "unauthenticated"
    local_simulated = "local_simulated"
    oidc_simulated = "oidc_simulated"
    enterprise_verified = "enterprise_verified"


class SecretAccessDecision(str, Enum):
    allow = "allow"
    allow_with_controls = "allow_with_controls"
    deny = "deny"


class IdentityProviderRecord(BaseModel):
    provider_id: str
    display_name: str
    issuer: str
    mode: str = "oidc_simulated"
    status: str = "enabled_simulation_only"
    trust_level: IdentityTrustLevel = IdentityTrustLevel.oidc_simulated
    allowed_tenants: List[str] = Field(default_factory=list)
    supported_flows: List[str] = Field(default_factory=list)
    required_claims: List[str] = Field(default_factory=list)
    notes: str = ""

    @field_validator("provider_id", "display_name", "issuer")
    @classmethod
    def identity_provider_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class IdentityProviderCatalogResponse(BaseModel):
    version: str
    providers: List[IdentityProviderRecord]


class ServiceIdentityRecord(BaseModel):
    identity_id: str
    tenant_id: str
    display_name: str
    principal_type: PrincipalType = PrincipalType.agent_runtime
    roles: List[str] = Field(default_factory=list)
    allowed_capabilities: List[str] = Field(default_factory=list)
    allowed_environments: List[str] = Field(default_factory=list)
    allowed_secret_refs: List[str] = Field(default_factory=list)
    allowed_connector_ids: List[str] = Field(default_factory=list)
    max_autonomy_level: int = Field(default=2, ge=0, le=5)
    required_controls: List[str] = Field(default_factory=list)

    @field_validator("identity_id", "tenant_id", "display_name")
    @classmethod
    def service_identity_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ServiceIdentityCatalogResponse(BaseModel):
    version: str
    identities: List[ServiceIdentityRecord]


class TokenSimulationRequest(BaseModel):
    tenant_id: str
    provider_id: str
    subject_id: str
    subject_type: PrincipalType = PrincipalType.human_user
    requested_roles: List[str] = Field(default_factory=list)
    requested_scopes: List[str] = Field(default_factory=list)
    audience: str = "agentops-control-plane"
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    claims: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "provider_id", "subject_id", "audience")
    @classmethod
    def token_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class TokenSimulationResponse(BaseModel):
    token_id: str
    tenant_id: str
    provider_id: str
    subject_id: str
    authenticated: bool
    trust_level: IdentityTrustLevel
    roles: List[str] = Field(default_factory=list)
    scopes: List[str] = Field(default_factory=list)
    claims_summary: Dict[str, object] = Field(default_factory=dict)
    expires_in_seconds: int = Field(default=0, ge=0)
    required_controls: List[str] = Field(default_factory=list)
    audit_summary: str


class SecretReferenceRecord(BaseModel):
    secret_ref: str
    tenant_id: str
    display_name: str
    secret_type: str
    sensitivity: str = "high"
    owner_team: str = ""
    allowed_identity_ids: List[str] = Field(default_factory=list)
    allowed_environments: List[str] = Field(default_factory=list)
    allowed_connector_ids: List[str] = Field(default_factory=list)
    rotation_policy: str = ""
    material_status: str = "not_stored_reference_only"
    required_controls: List[str] = Field(default_factory=list)

    @field_validator("secret_ref", "tenant_id", "display_name", "secret_type")
    @classmethod
    def secret_ref_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()

    @field_validator("sensitivity")
    @classmethod
    def secret_sensitivity_must_be_allowed(cls, value: str) -> str:
        allowed = {"low", "medium", "high", "critical"}
        if value not in allowed:
            raise ValueError(f"sensitivity must be one of {sorted(allowed)}")
        return value


class SecretReferenceCatalogResponse(BaseModel):
    version: str
    secrets: List[SecretReferenceRecord]


class SecretAccessRequest(BaseModel):
    tenant_id: str
    actor_id: str
    actor_role: str
    identity_id: str
    secret_ref: str
    connector_id: str = ""
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    purpose: str
    approval_id: str = ""
    evidence_ids: List[str] = Field(default_factory=list)
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "actor_id", "actor_role", "identity_id", "secret_ref", "purpose")
    @classmethod
    def secret_access_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class SecretAccessResponse(BaseModel):
    tenant_id: str
    identity_id: str
    secret_ref: str
    connector_id: str = ""
    decision: SecretAccessDecision
    allowed: bool
    required_controls: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    boundary_violations: List[str] = Field(default_factory=list)
    audit_summary: str
    next_actions: List[str] = Field(default_factory=list)


class IdentitySecretsPostureResponse(BaseModel):
    version: str
    mode: str
    identity_provider_count: int
    service_identity_count: int
    secret_reference_count: int
    critical_secret_reference_count: int
    raw_secret_storage: str
    live_iam_status: str
    live_connector_secret_status: str
    ready_controls: List[str] = Field(default_factory=list)
    remaining_controls: List[str] = Field(default_factory=list)
    findings: List[str] = Field(default_factory=list)



class ConnectorImplementationStatus(str, Enum):
    contract_only = "contract_only"
    dry_run_adapter = "dry_run_adapter"
    live_candidate = "live_candidate"
    live_enabled = "live_enabled"


class ConnectorDryRunDecision(str, Enum):
    dry_run_executed = "dry_run_executed"
    blocked_pending_approval = "blocked_pending_approval"
    blocked = "blocked"


class ConnectorOperationContract(BaseModel):
    operation_id: str
    display_name: str
    description: str = ""
    side_effect_class: SideEffectClass = SideEffectClass.read_only
    risk_level: ToolRiskLevel = ToolRiskLevel.Medium
    requires_human_approval: bool = False
    allowed_environments: List[str] = Field(default_factory=list)
    input_schema: Dict[str, object] = Field(default_factory=dict)
    output_schema: Dict[str, object] = Field(default_factory=dict)
    dry_run_behavior: str = ""
    rollback_contract: str = ""
    required_controls: List[str] = Field(default_factory=list)

    @field_validator("operation_id", "display_name")
    @classmethod
    def connector_operation_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ConnectorAdapterContract(BaseModel):
    adapter_id: str
    connector_id: str
    display_name: str
    domain: str = "enterprise"
    adapter_type: str = "business_system"
    implementation_status: ConnectorImplementationStatus = ConnectorImplementationStatus.dry_run_adapter
    live_execution_enabled: bool = False
    allowed_tenants: List[str] = Field(default_factory=list)
    allowed_environments: List[str] = Field(default_factory=list)
    required_identity_ids: List[str] = Field(default_factory=list)
    required_secret_refs: List[str] = Field(default_factory=list)
    global_controls: List[str] = Field(default_factory=list)
    operations: List[ConnectorOperationContract] = Field(default_factory=list)

    @field_validator("adapter_id", "connector_id", "display_name")
    @classmethod
    def connector_adapter_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ConnectorContractCatalogResponse(BaseModel):
    version: str
    contract_mode: str
    adapters: List[ConnectorAdapterContract]


class ConnectorContractValidationRequest(BaseModel):
    adapter: ConnectorAdapterContract


class ConnectorContractValidationResponse(BaseModel):
    adapter_id: str
    valid: bool
    readiness_stage: str
    findings: List[str] = Field(default_factory=list)
    required_before_live: List[str] = Field(default_factory=list)


class DryRunConnectorRequest(BaseModel):
    tenant_id: str
    agent_id: str
    actor_id: str
    actor_role: str
    identity_id: str
    secret_ref: str
    adapter_id: str
    connector_id: str
    operation_id: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    approval_id: str = ""
    evidence_ids: List[str] = Field(default_factory=list)
    payload: Dict[str, object] = Field(default_factory=dict)
    purpose: str
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "agent_id", "actor_id", "actor_role", "identity_id", "secret_ref", "adapter_id", "connector_id", "operation_id", "purpose")
    @classmethod
    def dry_run_request_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class DryRunConnectorResponse(BaseModel):
    run_id: str
    tenant_id: str
    agent_id: str
    adapter_id: str
    connector_id: str
    operation_id: str
    decision: ConnectorDryRunDecision
    allowed: bool
    simulated_result: Dict[str, object] = Field(default_factory=dict)
    required_controls: List[str] = Field(default_factory=list)
    boundary_violations: List[str] = Field(default_factory=list)
    audit_summary: str
    next_actions: List[str] = Field(default_factory=list)


class DryRunConnectorRunRecord(DryRunConnectorResponse):
    actor_id: str
    actor_role: str
    target_environment: TargetEnvironment
    approval_id: str = ""
    evidence_ids: List[str] = Field(default_factory=list)
    created_at: str = ""


class DryRunConnectorRunListResponse(BaseModel):
    runs: List[DryRunConnectorRunRecord]


class LiveConnectorGovernanceDecision(str, Enum):
    live_candidate_ready = "live_candidate_ready"
    not_ready = "not_ready"
    blocked = "blocked"


class LiveConnectorReadinessProfile(BaseModel):
    profile_id: str
    adapter_id: str
    connector_id: str
    display_name: str
    allowed_live_stages: List[str] = Field(default_factory=list)
    minimum_evidence_count: int = Field(default=1, ge=0)
    required_evidence_types: List[str] = Field(default_factory=list)
    required_approvals: List[str] = Field(default_factory=list)
    required_operational_capabilities: List[str] = Field(default_factory=list)
    required_security_capabilities: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    prohibited_conditions: List[str] = Field(default_factory=list)

    @field_validator("profile_id", "adapter_id", "connector_id", "display_name")
    @classmethod
    def live_profile_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class LiveConnectorProfileCatalogResponse(BaseModel):
    version: str
    live_execution_status: str
    profiles: List[LiveConnectorReadinessProfile]


class LiveConnectorReadinessResponse(BaseModel):
    version: str
    live_execution_status: str
    profile_count: int
    global_controls: List[str] = Field(default_factory=list)
    global_blockers: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)


class LiveConnectorEvaluationRequest(BaseModel):
    tenant_id: str
    agent_id: str
    actor_id: str
    actor_role: str
    adapter_id: str
    connector_id: str
    identity_id: str
    secret_ref: str
    target_environment: TargetEnvironment = TargetEnvironment.pilot
    requested_stage: str = "live_candidate"
    approval_id: str = ""
    approval_roles: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    evidence_types: List[str] = Field(default_factory=list)
    operational_capabilities: List[str] = Field(default_factory=list)
    security_capabilities: List[str] = Field(default_factory=list)
    real_iam_validation_ready: bool = False
    external_secret_manager_ready: bool = False
    immutable_audit_ready: bool = False
    rollback_test_passed: bool = False
    incident_runbook_available: bool = False
    live_execution_requested: bool = False
    purpose: str
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "agent_id", "actor_id", "actor_role", "adapter_id", "connector_id", "identity_id", "secret_ref", "purpose")
    @classmethod
    def live_connector_eval_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class LiveConnectorEvaluationResponse(BaseModel):
    evaluation_id: str
    tenant_id: str
    agent_id: str
    adapter_id: str
    connector_id: str
    decision: LiveConnectorGovernanceDecision
    eligible_for_live_candidate: bool
    live_execution_enabled: bool = False
    readiness_score: float = Field(ge=0, le=100)
    matched_profile_id: str = ""
    required_controls: List[str] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    audit_summary: str


class LiveConnectorEvaluationRecord(LiveConnectorEvaluationResponse):
    actor_id: str
    actor_role: str
    target_environment: TargetEnvironment
    requested_stage: str = "live_candidate"
    approval_id: str = ""
    evidence_ids: List[str] = Field(default_factory=list)
    created_at: str = ""


class LiveConnectorEvaluationListResponse(BaseModel):
    evaluations: List[LiveConnectorEvaluationRecord]


class ProviderGatewayDecision(str, Enum):
    route_approved = "route_approved"
    route_with_controls = "route_with_controls"
    route_requires_approval = "route_requires_approval"
    route_blocked = "route_blocked"


class ProviderTrustTier(str, Enum):
    internal = "internal"
    private_cloud = "private_cloud"
    approved_external_gateway = "approved_external_gateway"
    restricted_external = "restricted_external"
    local_developer = "local_developer"


class ProviderGatewayProfile(BaseModel):
    profile_id: str
    provider_id: str
    model_id: str
    display_name: str
    provider_trust_tier: ProviderTrustTier
    allowed_environments: List[str] = Field(default_factory=list)
    allowed_regions: List[str] = Field(default_factory=list)
    max_data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    supports_tool_use: bool = False
    capabilities: List[str] = Field(default_factory=list)
    allowed_fallbacks: List[str] = Field(default_factory=list)
    input_cost_per_1k_tokens: float = Field(default=0.0, ge=0)
    output_cost_per_1k_tokens: float = Field(default=0.0, ge=0)
    max_estimated_cost_usd: float = Field(default=0.0, ge=0)
    required_controls: List[str] = Field(default_factory=list)
    required_approval_roles: List[str] = Field(default_factory=list)
    notes: str = ""

    @field_validator("profile_id", "provider_id", "model_id", "display_name")
    @classmethod
    def provider_gateway_profile_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ProviderGatewayPostureResponse(BaseModel):
    version: str
    live_provider_execution_status: str
    profile_count: int
    global_controls: List[str] = Field(default_factory=list)
    cost_policy: Dict[str, object] = Field(default_factory=dict)
    next_actions: List[str] = Field(default_factory=list)


class ProviderGatewayProfileCatalogResponse(BaseModel):
    version: str
    live_provider_execution_status: str
    profiles: List[ProviderGatewayProfile]


class ProviderRouteRequest(BaseModel):
    tenant_id: str
    agent_id: str
    actor_id: str
    actor_role: str
    provider_id: str
    model_id: str
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    region: str
    estimated_input_tokens: int = Field(default=0, ge=0)
    estimated_output_tokens: int = Field(default=0, ge=0)
    requires_tool_use: bool = False
    required_capabilities: List[str] = Field(default_factory=list)
    approval_id: str = ""
    approval_roles: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    fallback_provider_id: str = ""
    fallback_model_id: str = ""
    live_provider_execution_requested: bool = False
    purpose: str
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "agent_id", "actor_id", "actor_role", "provider_id", "model_id", "region", "purpose")
    @classmethod
    def provider_route_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ProviderRouteResponse(BaseModel):
    route_id: str
    tenant_id: str
    agent_id: str
    provider_id: str
    model_id: str
    decision: ProviderGatewayDecision
    allowed: bool
    live_provider_execution_enabled: bool = False
    matched_profile_id: str = ""
    estimated_cost_usd: float = Field(ge=0)
    required_controls: List[str] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    selected_fallback: str = ""
    next_actions: List[str] = Field(default_factory=list)
    audit_summary: str


class ProviderRouteDecisionRecord(ProviderRouteResponse):
    actor_id: str
    actor_role: str
    target_environment: TargetEnvironment
    data_sensitivity: SensitivityLevel
    region: str
    approval_id: str = ""
    evidence_ids: List[str] = Field(default_factory=list)
    created_at: str = ""


class ProviderRouteDecisionListResponse(BaseModel):
    decisions: List[ProviderRouteDecisionRecord]


class ModelRiskTier(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    restricted = "restricted"


class ModelSafetyDecision(str, Enum):
    safety_approved = "safety_approved"
    safety_approved_with_controls = "safety_approved_with_controls"
    safety_requires_revision = "safety_requires_revision"
    safety_blocked = "safety_blocked"


class ModelRiskProfile(BaseModel):
    risk_profile_id: str
    provider_id: str
    model_id: str
    model_family: str = ""
    model_risk_tier: ModelRiskTier = ModelRiskTier.medium
    allowed_environments: List[str] = Field(default_factory=list)
    max_data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    allowed_output_types: List[str] = Field(default_factory=list)
    high_risk_domains: List[str] = Field(default_factory=list)
    disallowed_prompt_patterns: List[str] = Field(default_factory=list)
    disallowed_response_patterns: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    required_approval_roles: List[str] = Field(default_factory=list)

    @field_validator("risk_profile_id", "provider_id", "model_id")
    @classmethod
    def model_risk_profile_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class ModelSafetyPostureResponse(BaseModel):
    version: str
    live_provider_execution_status: str
    profile_count: int
    global_controls: List[str] = Field(default_factory=list)
    policy_mode: str
    next_actions: List[str] = Field(default_factory=list)


class ModelRiskProfileCatalogResponse(BaseModel):
    version: str
    live_provider_execution_status: str
    profiles: List[ModelRiskProfile]


class PromptResponseSafetyReviewRequest(BaseModel):
    tenant_id: str
    agent_id: str
    actor_id: str
    actor_role: str
    provider_id: str
    model_id: str
    route_id: str = ""
    target_environment: TargetEnvironment = TargetEnvironment.sandbox
    data_sensitivity: SensitivityLevel = SensitivityLevel.medium
    use_case_domain: str
    expected_output_type: str = "summary"
    prompt_text: str
    response_text: str = ""
    contains_pii: bool = False
    contains_credentials: bool = False
    contains_customer_data: bool = False
    contains_financial_data: bool = False
    external_user_visible: bool = False
    requested_tool_use: bool = False
    approval_id: str = ""
    approval_roles: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    safety_controls: List[str] = Field(default_factory=list)
    live_provider_execution_requested: bool = False
    purpose: str
    context: Dict[str, object] = Field(default_factory=dict)

    @field_validator("tenant_id", "agent_id", "actor_id", "actor_role", "provider_id", "model_id", "use_case_domain", "expected_output_type", "prompt_text", "purpose")
    @classmethod
    def safety_review_fields_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value cannot be empty")
        return value.strip()


class PromptResponseSafetyReviewResponse(BaseModel):
    review_id: str
    tenant_id: str
    agent_id: str
    provider_id: str
    model_id: str
    decision: ModelSafetyDecision
    allowed: bool
    live_provider_execution_enabled: bool = False
    matched_risk_profile_id: str = ""
    safety_score: float = Field(ge=0, le=100)
    risk_signals: List[str] = Field(default_factory=list)
    prompt_pattern_matches: List[str] = Field(default_factory=list)
    response_pattern_matches: List[str] = Field(default_factory=list)
    required_controls: List[str] = Field(default_factory=list)
    missing_controls: List[str] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    audit_summary: str


class PromptResponseSafetyReviewRecord(PromptResponseSafetyReviewResponse):
    actor_id: str
    actor_role: str
    target_environment: TargetEnvironment
    data_sensitivity: SensitivityLevel
    use_case_domain: str
    expected_output_type: str
    approval_id: str = ""
    evidence_ids: List[str] = Field(default_factory=list)
    created_at: str = ""


class PromptResponseSafetyReviewListResponse(BaseModel):
    reviews: List[PromptResponseSafetyReviewRecord]
