from fastapi import FastAPI, HTTPException

from agentops_mesh_api.core.config import get_settings
from agentops_mesh_api.models.schemas import (
    AgentEvaluationRequest,
    AgentRegistryListResponse,
    AgentRegistryRecord,
    AgentVersionRecord,
    EvidenceListResponse,
    EvidenceRecord,
    EvaluationResponse,
    GovernanceWorkflowRequest,
    GovernanceWorkflowResponse,
    PolicyCheckRequest,
    PolicyCheckResponse,
    ProviderRegistryResponse,
    TraceLedgerListResponse,
    TraceLedgerRecord,
    ObservabilitySummaryResponse,
    AgentRuntimeReportResponse,
    ConnectorRegistryResponse,
    ToolSandboxExecutionRequest,
    ToolSandboxExecutionResponse,
    ToolSandboxRunListResponse,
    ProcurementControlPlaneRequest,
    ProcurementControlPlaneResponse,
    ProcurementCaseListResponse,
    ProcurementScenarioListResponse,
    RuntimeExecutionRequest,
    RuntimeExecutionResponse,
    RiskClassificationResponse,
    AccessCheckRequest,
    AccessCheckResponse,
    RoleCatalogResponse,
    TenantCatalogResponse,
    CapabilityCatalogResponse,
    SecurityPostureSummaryResponse,
    StorageDataset,
    StorageMigrationPlanRequest,
    StorageMigrationPlanResponse,
    StoragePostureResponse,
    TenantDatasetListResponse,
    TenantRecordListResponse,
    TenantRecordUpsertRequest,
    TenantRecordUpsertResponse,
    WeightsResponse,
    AuditEventRecord,
    AuditEventListResponse,
    AuditEventIngestResponse,
    AuditSummaryResponse,
    DecisionHistoryResponse,
    AuditEventType,
    AuditDecisionOutcome,
    ApprovalStatus,
    ApprovalRequestCreate,
    ApprovalDecisionRequest,
    ApprovalListResponse,
    ApprovalRequestResponse,
    ApprovalDecisionResponse,
    ApprovalReadinessResponse,
    ApprovalRecord,
    IdentityProviderCatalogResponse,
    ServiceIdentityCatalogResponse,
    TokenSimulationRequest,
    TokenSimulationResponse,
    SecretReferenceCatalogResponse,
    SecretAccessRequest,
    SecretAccessResponse,
    IdentitySecretsPostureResponse,
    ConnectorContractCatalogResponse,
    ConnectorAdapterContract,
    ConnectorContractValidationRequest,
    ConnectorContractValidationResponse,
    DryRunConnectorRequest,
    DryRunConnectorResponse,
    DryRunConnectorRunListResponse,
    LiveConnectorReadinessResponse,
    LiveConnectorProfileCatalogResponse,
    LiveConnectorReadinessProfile,
    LiveConnectorEvaluationRequest,
    LiveConnectorEvaluationResponse,
    LiveConnectorEvaluationListResponse,
    ProviderGatewayPostureResponse,
    ProviderGatewayProfileCatalogResponse,
    ProviderGatewayProfile,
    ProviderRouteRequest,
    ProviderRouteResponse,
    ProviderRouteDecisionListResponse,
    ModelSafetyPostureResponse,
    ModelRiskProfileCatalogResponse,
    ModelRiskProfile,
    PromptResponseSafetyReviewRequest,
    PromptResponseSafetyReviewResponse,
    PromptResponseSafetyReviewListResponse,
)
from agentops_mesh_api.services.evaluator import AgentEvaluatorService, EVALUATION_WEIGHTS
from agentops_mesh_api.services.governance_workflow import GovernanceWorkflowService
from agentops_mesh_api.services.agent_registry import AgentRegistryService
from agentops_mesh_api.services.evidence_vault import EvidenceVaultService
from agentops_mesh_api.services.risk_classifier import RiskClassifierService
from agentops_mesh_api.services.policy_guardrail import PolicyGuardrailService
from agentops_mesh_api.services.provider_registry import ProviderRegistryService
from agentops_mesh_api.services.runtime_enforcer import RuntimeEnforcementService
from agentops_mesh_api.services.trace_ledger import TraceLedgerService
from agentops_mesh_api.services.connector_registry import ConnectorRegistryService
from agentops_mesh_api.services.tool_sandbox import ToolSandboxService
from agentops_mesh_api.services.procurement_accelerator import ProcurementAcceleratorService
from agentops_mesh_api.services.security_rbac import SecurityRbacService
from agentops_mesh_api.services.tenant_storage import TenantScopedStorageService
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService
from agentops_mesh_api.services.approval_workflow import ApprovalWorkflowService
from agentops_mesh_api.services.identity_secrets_boundary import IdentitySecretsBoundaryService
from agentops_mesh_api.services.connector_contract_sdk import ConnectorContractSdkService
from agentops_mesh_api.services.live_connector_governance import LiveConnectorGovernanceService
from agentops_mesh_api.services.provider_gateway import ProviderGatewayService
from agentops_mesh_api.services.model_safety_review import ModelSafetyReviewService
from agentops_mesh_api.services.control_plane_summary import ControlPlaneSummaryService
from agentops_mesh_api.services.benchmark_harness import BenchmarkHarnessService
from agentops_mesh_api.services.deployment_profiles import DeploymentProfileService
from agentops_mesh_api.services.launch_assets import LaunchAssetService
from agentops_mesh_api.services.community_intake import CommunityIntakeService
from agentops_mesh_api.services.public_site_ux import PublicSiteUxService
from agentops_mesh_api.services.release_evidence import ReleaseEvidenceService
from agentops_mesh_api.services.launch_candidate import LaunchCandidateService

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
_evaluator = AgentEvaluatorService()
_risk_classifier = RiskClassifierService()
_governance_workflow = GovernanceWorkflowService()
_agent_registry = AgentRegistryService()
_evidence_vault = EvidenceVaultService()
_policy_guardrail = PolicyGuardrailService()
_provider_registry = ProviderRegistryService()
_trace_ledger = TraceLedgerService()
_runtime_enforcer = RuntimeEnforcementService(policy_service=_policy_guardrail, provider_registry=_provider_registry, trace_ledger=_trace_ledger)
_connector_registry = ConnectorRegistryService()
_tool_sandbox = ToolSandboxService(connector_registry=_connector_registry, policy_service=_policy_guardrail)
_security_rbac = SecurityRbacService()
_tenant_storage = TenantScopedStorageService()
_audit_event_bus = AuditEventBusService()
_approval_workflow = ApprovalWorkflowService(audit_bus=_audit_event_bus)
_identity_secrets_boundary = IdentitySecretsBoundaryService(audit_bus=_audit_event_bus)
_connector_contract_sdk = ConnectorContractSdkService(identity_boundary=_identity_secrets_boundary, audit_bus=_audit_event_bus)
_live_connector_governance = LiveConnectorGovernanceService(audit_bus=_audit_event_bus)
_provider_gateway = ProviderGatewayService(audit_bus=_audit_event_bus)
_model_safety_review = ModelSafetyReviewService(audit_bus=_audit_event_bus)
_control_plane_summary = ControlPlaneSummaryService()
_benchmark_harness = BenchmarkHarnessService()
_deployment_profiles = DeploymentProfileService()
_launch_assets = LaunchAssetService()
_community_intake = CommunityIntakeService()
_public_site_ux = PublicSiteUxService()
_release_evidence = ReleaseEvidenceService()
_launch_candidate = LaunchCandidateService()
_procurement_accelerator = ProcurementAcceleratorService(
    governance_service=_governance_workflow,
    policy_service=_policy_guardrail,
    runtime_service=_runtime_enforcer,
    tool_sandbox=_tool_sandbox,
)


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "deterministic_mode": settings.deterministic_mode,
    }


@app.get("/weights", response_model=WeightsResponse)
def get_weights() -> WeightsResponse:
    return WeightsResponse(weights=EVALUATION_WEIGHTS)


@app.post("/classify-risk", response_model=RiskClassificationResponse)
def classify_risk(request: AgentEvaluationRequest) -> RiskClassificationResponse:
    level, score, controls = _risk_classifier.classify(request.autonomy_level, request.risk_factors)
    return RiskClassificationResponse(risk_level=level, risk_score=score, required_controls=controls)


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: AgentEvaluationRequest) -> EvaluationResponse:
    return _evaluator.evaluate(request)


@app.post("/governance/run", response_model=GovernanceWorkflowResponse)
def run_governance_workflow(request: GovernanceWorkflowRequest) -> GovernanceWorkflowResponse:
    return _governance_workflow.run(request)



@app.get("/registry/agents", response_model=AgentRegistryListResponse)
def list_agents() -> AgentRegistryListResponse:
    return AgentRegistryListResponse(agents=_agent_registry.list_agents())


@app.post("/registry/agents", response_model=AgentRegistryRecord)
def upsert_agent(record: AgentRegistryRecord) -> AgentRegistryRecord:
    return _agent_registry.upsert_agent(record)


@app.get("/registry/agents/{agent_id}", response_model=AgentRegistryRecord)
def get_agent(agent_id: str) -> AgentRegistryRecord:
    try:
        return _agent_registry.get_agent(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/registry/agents/{agent_id}/versions", response_model=AgentRegistryRecord)
def add_agent_version(agent_id: str, version: AgentVersionRecord) -> AgentRegistryRecord:
    try:
        return _agent_registry.add_version(agent_id, version)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/registry/agents/{agent_id}/evidence", response_model=EvidenceListResponse)
def evidence_for_agent(agent_id: str) -> EvidenceListResponse:
    return EvidenceListResponse(evidence=_agent_registry.evidence_for_agent(agent_id))


@app.get("/evidence", response_model=EvidenceListResponse)
def list_evidence() -> EvidenceListResponse:
    return EvidenceListResponse(evidence=_evidence_vault.list_evidence())


@app.post("/evidence", response_model=EvidenceRecord)
def upsert_evidence(record: EvidenceRecord) -> EvidenceRecord:
    return _evidence_vault.upsert_evidence(record)


@app.get("/evidence/{evidence_id}", response_model=EvidenceRecord)
def get_evidence(evidence_id: str) -> EvidenceRecord:
    try:
        return _evidence_vault.get_evidence(evidence_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/policy/check", response_model=PolicyCheckResponse)
def check_policy(request: PolicyCheckRequest) -> PolicyCheckResponse:
    return _policy_guardrail.check(request)



@app.get("/runtime/providers", response_model=ProviderRegistryResponse)
def list_runtime_providers() -> ProviderRegistryResponse:
    return _provider_registry.list_providers()


@app.post("/runtime/execute", response_model=RuntimeExecutionResponse)
def execute_runtime(request: RuntimeExecutionRequest) -> RuntimeExecutionResponse:
    return _runtime_enforcer.execute(request)



@app.get("/observability/traces", response_model=TraceLedgerListResponse)
def list_traces(agent_id: str | None = None, decision: str | None = None, limit: int = 100) -> TraceLedgerListResponse:
    return TraceLedgerListResponse(traces=_trace_ledger.list_traces(agent_id=agent_id, decision=decision, limit=limit))


@app.get("/observability/traces/{request_id}", response_model=TraceLedgerRecord)
def get_trace(request_id: str) -> TraceLedgerRecord:
    try:
        return _trace_ledger.get_trace(request_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/observability/summary", response_model=ObservabilitySummaryResponse)
def observability_summary() -> ObservabilitySummaryResponse:
    return _trace_ledger.summary()


@app.get("/observability/agents/{agent_id}/report", response_model=AgentRuntimeReportResponse)
def agent_runtime_report(agent_id: str, limit: int = 20) -> AgentRuntimeReportResponse:
    return _trace_ledger.agent_report(agent_id, limit=limit)



@app.get("/connectors", response_model=ConnectorRegistryResponse)
def list_connectors() -> ConnectorRegistryResponse:
    return _connector_registry.list_connectors()


@app.post("/tools/sandbox/execute", response_model=ToolSandboxExecutionResponse)
def execute_tool_sandbox(request: ToolSandboxExecutionRequest) -> ToolSandboxExecutionResponse:
    return _tool_sandbox.execute(request)


@app.get("/tools/sandbox/runs", response_model=ToolSandboxRunListResponse)
def list_tool_sandbox_runs(limit: int = 100) -> ToolSandboxRunListResponse:
    return _tool_sandbox.list_runs(limit=limit)



@app.get("/security/roles", response_model=RoleCatalogResponse)
def list_security_roles() -> RoleCatalogResponse:
    return _security_rbac.list_roles()


@app.get("/security/tenants", response_model=TenantCatalogResponse)
def list_security_tenants() -> TenantCatalogResponse:
    return _security_rbac.list_tenants()


@app.get("/security/capabilities", response_model=CapabilityCatalogResponse)
def list_security_capabilities() -> CapabilityCatalogResponse:
    return _security_rbac.list_capabilities()


@app.get("/security/posture", response_model=SecurityPostureSummaryResponse)
def security_posture() -> SecurityPostureSummaryResponse:
    return _security_rbac.posture_summary()


@app.post("/security/access/check", response_model=AccessCheckResponse)
def check_security_access(request: AccessCheckRequest) -> AccessCheckResponse:
    return _security_rbac.check_access(request)


@app.get("/storage/posture", response_model=StoragePostureResponse)
def storage_posture() -> StoragePostureResponse:
    return _tenant_storage.posture()


@app.get("/storage/tenants/{tenant_id}/datasets", response_model=TenantDatasetListResponse)
def storage_tenant_datasets(tenant_id: str) -> TenantDatasetListResponse:
    try:
        return _tenant_storage.datasets_for_tenant(tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/storage/tenants/{tenant_id}/records/{dataset}", response_model=TenantRecordListResponse)
def storage_tenant_records(tenant_id: str, dataset: StorageDataset, limit: int = 100) -> TenantRecordListResponse:
    try:
        return _tenant_storage.list_records(tenant_id, dataset, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/storage/tenants/{tenant_id}/records/{dataset}", response_model=TenantRecordUpsertResponse)
def storage_upsert_tenant_record(tenant_id: str, dataset: StorageDataset, request: TenantRecordUpsertRequest) -> TenantRecordUpsertResponse:
    try:
        return _tenant_storage.upsert_record(tenant_id, dataset, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/storage/migration/plan", response_model=StorageMigrationPlanResponse)
def storage_migration_plan(request: StorageMigrationPlanRequest) -> StorageMigrationPlanResponse:
    return _tenant_storage.migration_plan(request)


@app.post("/accelerators/procurement/run", response_model=ProcurementControlPlaneResponse)
def run_procurement_accelerator(request: ProcurementControlPlaneRequest) -> ProcurementControlPlaneResponse:
    return _procurement_accelerator.run(request)


@app.get("/accelerators/procurement/cases", response_model=ProcurementCaseListResponse)
def list_procurement_cases(limit: int = 100) -> ProcurementCaseListResponse:
    return _procurement_accelerator.list_cases(limit=limit)


@app.get("/accelerators/procurement/scenarios", response_model=ProcurementScenarioListResponse)
def list_procurement_scenarios() -> ProcurementScenarioListResponse:
    return _procurement_accelerator.list_scenarios()


@app.get("/audit/events", response_model=AuditEventListResponse)
def list_audit_events(
    tenant_id: str | None = None,
    agent_id: str | None = None,
    event_type: AuditEventType | None = None,
    decision_outcome: AuditDecisionOutcome | None = None,
    subject_type: str | None = None,
    subject_id: str | None = None,
    limit: int = 100,
) -> AuditEventListResponse:
    return _audit_event_bus.list_events(
        tenant_id=tenant_id,
        agent_id=agent_id,
        event_type=event_type,
        decision_outcome=decision_outcome,
        subject_type=subject_type,
        subject_id=subject_id,
        limit=limit,
    )


@app.post("/audit/events", response_model=AuditEventIngestResponse)
def ingest_audit_event(event: AuditEventRecord) -> AuditEventIngestResponse:
    try:
        return _audit_event_bus.ingest(event)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/audit/events/{event_id}", response_model=AuditEventRecord)
def get_audit_event(event_id: str) -> AuditEventRecord:
    try:
        return _audit_event_bus.get_event(event_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/audit/summary", response_model=AuditSummaryResponse)
def audit_summary() -> AuditSummaryResponse:
    return _audit_event_bus.summary()


@app.get("/audit/decision-history/{subject_type}/{subject_id}", response_model=DecisionHistoryResponse)
def audit_decision_history(subject_type: str, subject_id: str, limit: int = 100) -> DecisionHistoryResponse:
    try:
        return _audit_event_bus.decision_history(subject_type, subject_id, limit=limit)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/approvals", response_model=ApprovalListResponse)
def list_approvals(
    tenant_id: str | None = None,
    agent_id: str | None = None,
    status: ApprovalStatus | None = None,
    limit: int = 100,
) -> ApprovalListResponse:
    return _approval_workflow.list_approvals(tenant_id=tenant_id, agent_id=agent_id, status=status, limit=limit)


@app.get("/approvals/readiness", response_model=ApprovalReadinessResponse)
def approval_readiness() -> ApprovalReadinessResponse:
    return _approval_workflow.readiness()


@app.post("/approvals/request", response_model=ApprovalRequestResponse)
def create_approval_request(request: ApprovalRequestCreate) -> ApprovalRequestResponse:
    return _approval_workflow.create_request(request)


@app.get("/approvals/{approval_id}", response_model=ApprovalRecord)
def get_approval(approval_id: str) -> ApprovalRecord:
    try:
        return _approval_workflow.get_approval(approval_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/approvals/{approval_id}/decide", response_model=ApprovalDecisionResponse)
def decide_approval(approval_id: str, decision: ApprovalDecisionRequest) -> ApprovalDecisionResponse:
    try:
        return _approval_workflow.decide(approval_id, decision)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc



@app.get("/identity/providers", response_model=IdentityProviderCatalogResponse)
def list_identity_providers() -> IdentityProviderCatalogResponse:
    return _identity_secrets_boundary.providers()


@app.get("/identity/service-identities", response_model=ServiceIdentityCatalogResponse)
def list_service_identities() -> ServiceIdentityCatalogResponse:
    return _identity_secrets_boundary.service_identities()


@app.post("/identity/token/simulate", response_model=TokenSimulationResponse)
def simulate_identity_token(request: TokenSimulationRequest) -> TokenSimulationResponse:
    try:
        return _identity_secrets_boundary.simulate_token(request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/secrets/references", response_model=SecretReferenceCatalogResponse)
def list_secret_references() -> SecretReferenceCatalogResponse:
    return _identity_secrets_boundary.secret_references()


@app.post("/secrets/access/check", response_model=SecretAccessResponse)
def check_secret_access(request: SecretAccessRequest) -> SecretAccessResponse:
    return _identity_secrets_boundary.check_secret_access(request)


@app.get("/security/identity-secrets-posture", response_model=IdentitySecretsPostureResponse)
def identity_secrets_posture() -> IdentitySecretsPostureResponse:
    return _identity_secrets_boundary.posture()



@app.get("/connector-contracts", response_model=ConnectorContractCatalogResponse)
def list_connector_contracts() -> ConnectorContractCatalogResponse:
    return _connector_contract_sdk.list_contracts()


@app.get("/connector-contracts/{adapter_id}", response_model=ConnectorAdapterContract)
def get_connector_contract(adapter_id: str) -> ConnectorAdapterContract:
    try:
        return _connector_contract_sdk.get_contract(adapter_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/connector-contracts/validate", response_model=ConnectorContractValidationResponse)
def validate_connector_contract(request: ConnectorContractValidationRequest) -> ConnectorContractValidationResponse:
    return _connector_contract_sdk.validate_contract(request)


@app.post("/connectors/dry-run/execute", response_model=DryRunConnectorResponse)
def execute_connector_dry_run(request: DryRunConnectorRequest) -> DryRunConnectorResponse:
    return _connector_contract_sdk.execute_dry_run(request)


@app.get("/connectors/dry-run/runs", response_model=DryRunConnectorRunListResponse)
def list_connector_dry_run_runs(limit: int = 100) -> DryRunConnectorRunListResponse:
    return _connector_contract_sdk.list_runs(limit=limit)



@app.get("/live-connectors/readiness", response_model=LiveConnectorReadinessResponse)
def live_connector_readiness() -> LiveConnectorReadinessResponse:
    return _live_connector_governance.readiness()


@app.get("/live-connectors/profiles", response_model=LiveConnectorProfileCatalogResponse)
def list_live_connector_profiles() -> LiveConnectorProfileCatalogResponse:
    return _live_connector_governance.profiles()


@app.get("/live-connectors/profiles/{profile_id}", response_model=LiveConnectorReadinessProfile)
def get_live_connector_profile(profile_id: str) -> LiveConnectorReadinessProfile:
    try:
        return _live_connector_governance.get_profile(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/live-connectors/evaluate", response_model=LiveConnectorEvaluationResponse)
def evaluate_live_connector(request: LiveConnectorEvaluationRequest) -> LiveConnectorEvaluationResponse:
    return _live_connector_governance.evaluate(request)


@app.get("/live-connectors/evaluations", response_model=LiveConnectorEvaluationListResponse)
def list_live_connector_evaluations(limit: int = 100) -> LiveConnectorEvaluationListResponse:
    return _live_connector_governance.list_evaluations(limit=limit)


@app.get("/provider-gateway/posture", response_model=ProviderGatewayPostureResponse)
def provider_gateway_posture() -> ProviderGatewayPostureResponse:
    return _provider_gateway.posture()


@app.get("/provider-gateway/profiles", response_model=ProviderGatewayProfileCatalogResponse)
def list_provider_gateway_profiles() -> ProviderGatewayProfileCatalogResponse:
    return _provider_gateway.profiles()


@app.get("/provider-gateway/profiles/{profile_id}", response_model=ProviderGatewayProfile)
def get_provider_gateway_profile(profile_id: str) -> ProviderGatewayProfile:
    try:
        return _provider_gateway.get_profile(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/provider-gateway/route", response_model=ProviderRouteResponse)
def route_provider_model(request: ProviderRouteRequest) -> ProviderRouteResponse:
    return _provider_gateway.route(request)


@app.get("/provider-gateway/decisions", response_model=ProviderRouteDecisionListResponse)
def list_provider_route_decisions(limit: int = 100) -> ProviderRouteDecisionListResponse:
    return _provider_gateway.list_decisions(limit=limit)


@app.get("/model-safety/posture", response_model=ModelSafetyPostureResponse)
def model_safety_posture() -> ModelSafetyPostureResponse:
    return _model_safety_review.posture()


@app.get("/model-safety/risk-profiles", response_model=ModelRiskProfileCatalogResponse)
def list_model_risk_profiles() -> ModelRiskProfileCatalogResponse:
    return _model_safety_review.risk_profiles()


@app.get("/model-safety/risk-profiles/{risk_profile_id}", response_model=ModelRiskProfile)
def get_model_risk_profile(risk_profile_id: str) -> ModelRiskProfile:
    try:
        return _model_safety_review.get_risk_profile(risk_profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/model-safety/review", response_model=PromptResponseSafetyReviewResponse)
def review_prompt_response_safety(request: PromptResponseSafetyReviewRequest) -> PromptResponseSafetyReviewResponse:
    return _model_safety_review.review(request)


@app.get("/model-safety/reviews", response_model=PromptResponseSafetyReviewListResponse)
def list_prompt_response_safety_reviews(limit: int = 100) -> PromptResponseSafetyReviewListResponse:
    return _model_safety_review.list_reviews(limit=limit)


@app.get("/control-plane/capabilities")
def control_plane_capabilities() -> dict:
    return _control_plane_summary.capabilities()


@app.get("/control-plane/demo-flow")
def control_plane_demo_flow() -> dict:
    return _control_plane_summary.demo_flow()


@app.get("/control-plane/api-surface")
def control_plane_api_surface() -> dict:
    return _control_plane_summary.api_surface()


@app.get("/control-plane/release-status")
def control_plane_release_status() -> dict:
    return _control_plane_summary.release_status()


@app.get("/control-plane/end-to-end-report")
def control_plane_end_to_end_report() -> dict:
    return _control_plane_summary.end_to_end_report()


@app.get("/control-plane/openapi-lite")
def control_plane_openapi_lite() -> dict:
    return _control_plane_summary.openapi_lite()


@app.get("/control-plane/contributor-readiness")
def control_plane_contributor_readiness() -> dict:
    return _control_plane_summary.contributor_readiness()



@app.get("/benchmarks/posture")
def benchmark_posture() -> dict:
    return _benchmark_harness.posture()


@app.get("/benchmarks/scenarios")
def list_benchmark_scenarios(domain: str | None = None, category: str | None = None, risk_level: str | None = None) -> dict:
    return _benchmark_harness.scenarios(domain=domain, category=category, risk_level=risk_level)


@app.get("/benchmarks/scenarios/{scenario_id}")
def get_benchmark_scenario(scenario_id: str) -> dict:
    try:
        return _benchmark_harness.get_scenario(scenario_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/benchmarks/suites")
def list_benchmark_suites() -> dict:
    return _benchmark_harness.suites()


@app.post("/benchmarks/run")
def run_benchmark(request: dict) -> dict:
    try:
        return _benchmark_harness.run(request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/benchmarks/runs")
def list_benchmark_runs(limit: int = 100) -> dict:
    return _benchmark_harness.runs(limit=limit)


@app.get("/benchmarks/summary")
def benchmark_summary() -> dict:
    return _benchmark_harness.summary()

@app.get("/deployment/posture")
def deployment_posture() -> dict:
    return _deployment_profiles.posture()


@app.get("/deployment/profiles")
def deployment_profiles() -> dict:
    return _deployment_profiles.profiles()


@app.get("/deployment/profiles/{profile_id}")
def deployment_profile(profile_id: str) -> dict:
    try:
        return _deployment_profiles.get_profile(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/deployment/validate")
def validate_deployment_profile(request: dict) -> dict:
    try:
        return _deployment_profiles.validate(request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/deployment/docker-compose")
def deployment_docker_compose() -> dict:
    return _deployment_profiles.docker_compose_profile()


@app.get("/deployment/environment-matrix")
def deployment_environment_matrix() -> dict:
    return _deployment_profiles.environment_matrix()



@app.get("/launch/readiness")
def launch_readiness() -> dict:
    return _launch_assets.readiness()


@app.get("/launch/assets")
def launch_assets() -> dict:
    return _launch_assets.manifest()


@app.get("/launch/storyboard")
def launch_storyboard() -> dict:
    return _launch_assets.storyboard()


@app.get("/launch/messaging")
def launch_messaging() -> dict:
    return _launch_assets.messaging()


@app.get("/launch/linkedin-drafts")
def launch_linkedin_drafts() -> dict:
    return _launch_assets.linkedin_drafts()


@app.get("/launch/publication-checklist")
def launch_publication_checklist() -> dict:
    return _launch_assets.publication_checklist()


@app.get("/community/readiness")
def community_readiness() -> dict:
    return _community_intake.readiness()


@app.get("/community/intake/channels")
def community_intake_channels() -> dict:
    return _community_intake.channels()


@app.get("/community/intake-summary")
def community_intake_summary() -> dict:
    return _community_intake.intake_summary()


@app.get("/community/use-case-submissions")
def community_use_case_submissions() -> dict:
    return _community_intake.use_case_submissions()


@app.post("/community/use-case-submissions")
def community_add_use_case_submission(record: dict) -> dict:
    try:
        return _community_intake.add_use_case_submission(record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/community/architecture-critiques")
def community_architecture_critiques() -> dict:
    return _community_intake.architecture_critiques()


@app.post("/community/architecture-critiques")
def community_add_architecture_critique(record: dict) -> dict:
    try:
        return _community_intake.add_architecture_critique(record)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/community/roadmap-feedback")
def community_roadmap_feedback() -> dict:
    return _community_intake.roadmap_feedback()


@app.get("/community/adoption-feedback")
def community_adoption_feedback() -> dict:
    return _community_intake.adoption_feedback()


@app.get("/public-site/readiness")
def public_site_readiness() -> dict:
    return _public_site_ux.readiness()


@app.get("/public-site/navigation")
def public_site_navigation() -> dict:
    return _public_site_ux.navigation()


@app.get("/public-site/demo-paths")
def public_site_demo_paths() -> dict:
    return _public_site_ux.demo_paths()


@app.get("/public-site/personas")
def public_site_personas() -> dict:
    return _public_site_ux.personas()


@app.get("/public-site/ux-copy")
def public_site_ux_copy() -> dict:
    return _public_site_ux.ux_copy()


@app.get("/public-site/page-inventory")
def public_site_page_inventory() -> dict:
    return _public_site_ux.page_inventory()


@app.get("/public-site/interactive-report")
def public_site_interactive_report() -> dict:
    return _public_site_ux.interactive_report()

@app.get("/release-evidence/readiness")
def release_evidence_readiness() -> dict:
    return _release_evidence.readiness()


@app.get("/release-evidence/manifest")
def release_evidence_manifest() -> dict:
    return _release_evidence.manifest()


@app.get("/release-evidence/validation-snapshot")
def release_evidence_validation_snapshot() -> dict:
    return _release_evidence.validation_snapshot()


@app.get("/release-evidence/demo-recording-plan")
def release_evidence_demo_recording_plan() -> dict:
    return _release_evidence.demo_recording_plan()


@app.get("/release-evidence/proof-bundle")
def release_evidence_proof_bundle() -> dict:
    return _release_evidence.proof_bundle()


@app.get("/release-evidence/public-report")
def release_evidence_public_report() -> dict:
    return _release_evidence.public_report()


@app.get("/launch-candidate/readiness")
def launch_candidate_readiness() -> dict:
    return _launch_candidate.readiness()


@app.get("/launch-candidate/manifest")
def launch_candidate_manifest() -> dict:
    return _launch_candidate.manifest()


@app.get("/launch-candidate/github-pages")
def launch_candidate_github_pages() -> dict:
    return _launch_candidate.github_pages()


@app.get("/launch-candidate/publication-sequence")
def launch_candidate_publication_sequence() -> dict:
    return _launch_candidate.publication_sequence()


@app.get("/launch-candidate/checklist")
def launch_candidate_checklist() -> dict:
    return _launch_candidate.checklist()


@app.get("/launch-candidate/evidence")
def launch_candidate_evidence() -> dict:
    return _launch_candidate.evidence()


@app.get("/launch-candidate/social-copy")
def launch_candidate_social_copy() -> dict:
    return _launch_candidate.social_copy()


@app.get("/launch-candidate/public-report")
def launch_candidate_public_report() -> dict:
    return _launch_candidate.public_report()
