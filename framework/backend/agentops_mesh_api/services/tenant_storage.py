from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agentops_mesh_api.models.schemas import (
    StorageDataset,
    StorageMigrationPlanRequest,
    StorageMigrationPlanResponse,
    StorageMode,
    StoragePostureResponse,
    TenantDatasetListResponse,
    TenantRecordListResponse,
    TenantRecordUpsertRequest,
    TenantRecordUpsertResponse,
    TenantScopedDatasetRecord,
)

DATASET_FILENAMES: dict[StorageDataset, str] = {
    StorageDataset.agents: "agents.json",
    StorageDataset.evidence: "evidence.json",
    StorageDataset.runtime_traces: "runtime_traces.json",
    StorageDataset.tool_sandbox_runs: "tool_sandbox_runs.json",
    StorageDataset.procurement_cases: "procurement_cases.json",
    StorageDataset.governance_decisions: "governance_decisions.json",
    StorageDataset.access_decisions: "access_decisions.json",
    StorageDataset.policy_decisions: "policy_decisions.json",
}


class TenantScopedStorageService:
    """Tenant-scoped local JSON storage boundary for v1.2.

    The implementation remains intentionally simple but changes the persistence
    contract: records are now addressed through tenant + dataset boundaries.
    Production deployments should replace this local adapter with SQLite/Postgres
    repositories while preserving this service contract.
    """

    def __init__(self, root_dir: Path | None = None) -> None:
        if root_dir is None:
            root_dir = Path(__file__).resolve().parents[2] / "data" / "tenants"
        self.root_dir = root_dir
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def posture(self) -> StoragePostureResponse:
        datasets: list[TenantScopedDatasetRecord] = []
        tenant_ids = self._tenant_ids()
        for tenant_id in tenant_ids:
            datasets.extend(self.datasets_for_tenant(tenant_id).datasets)

        missing = [d for d in datasets if d.record_count == 0]
        findings = [
            "Tenant-scoped local JSON adapter is active.",
            "This mode is suitable for local demos, test fixtures, and open-source inspection.",
        ]
        if missing:
            findings.append(f"{len(missing)} tenant dataset files are empty; seed only datasets required for the active demo.")
        findings.append("Production use requires database transactions, backups, encryption, retention policy, and identity-provider integration.")

        return StoragePostureResponse(
            version="1.2.0",
            storage_mode=StorageMode.tenant_scoped_local_json,
            tenant_count=len(tenant_ids),
            dataset_count=len(datasets),
            total_records=sum(item.record_count for item in datasets),
            datasets=datasets,
            findings=findings,
            recommended_migrations=[
                "Add SQLite adapter for local developer workflows.",
                "Add Postgres repository implementation before production pilots.",
                "Add migration scripts and storage write audit events.",
            ],
            required_controls=[
                "tenant_id_on_all_records",
                "deny_cross_tenant_reads_by_default",
                "storage_write_audit_required",
                "backup_and_restore_test_required_before_pilot",
            ],
        )

    def datasets_for_tenant(self, tenant_id: str) -> TenantDatasetListResponse:
        safe_tenant = self._safe_segment(tenant_id)
        tenant_dir = self.root_dir / safe_tenant
        tenant_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc).isoformat()
        records: list[TenantScopedDatasetRecord] = []
        for dataset, filename in DATASET_FILENAMES.items():
            data = self._read_dataset(safe_tenant, dataset)
            records.append(
                TenantScopedDatasetRecord(
                    tenant_id=safe_tenant,
                    dataset=dataset,
                    filename=filename,
                    record_count=len(data),
                    isolation_status="tenant_scoped",
                    controls=["tenant_path_boundary", "local_json_inspection", "record_level_tenant_hint_recommended"],
                    last_inspected_at=now,
                )
            )
        return TenantDatasetListResponse(tenant_id=safe_tenant, datasets=records)

    def list_records(self, tenant_id: str, dataset: StorageDataset, limit: int = 100) -> TenantRecordListResponse:
        safe_tenant = self._safe_segment(tenant_id)
        records = self._read_dataset(safe_tenant, dataset)
        limit = max(1, min(limit, 1000))
        return TenantRecordListResponse(tenant_id=safe_tenant, dataset=dataset, records=records[:limit])

    def upsert_record(
        self,
        tenant_id: str,
        dataset: StorageDataset,
        request: TenantRecordUpsertRequest,
    ) -> TenantRecordUpsertResponse:
        safe_tenant = self._safe_segment(tenant_id)
        records = self._read_dataset(safe_tenant, dataset)
        record = dict(request.record)
        record.setdefault("tenant_id", safe_tenant)
        record_id = str(record.get(request.record_id_field) or "").strip()
        if not record_id:
            raise ValueError(f"record must include non-empty identifier field '{request.record_id_field}'")
        replaced = False
        for index, existing in enumerate(records):
            if str(existing.get(request.record_id_field, "")) == record_id:
                records[index] = record
                replaced = True
                break
        if not replaced:
            records.append(record)
        self._write_dataset(safe_tenant, dataset, records)
        return TenantRecordUpsertResponse(
            tenant_id=safe_tenant,
            dataset=dataset,
            status="updated" if replaced else "created",
            storage_path=str(self._dataset_path(safe_tenant, dataset).relative_to(self.root_dir.parent)),
            record_count=len(records),
            record_id_field=request.record_id_field,
            record_id=record_id,
            audit_summary=f"Tenant-scoped record {record_id!r} {('updated' if replaced else 'created')} in dataset {dataset.value!r} for tenant {safe_tenant!r}.",
        )

    def migration_plan(self, request: StorageMigrationPlanRequest) -> StorageMigrationPlanResponse:
        tenants = request.tenants or self._tenant_ids()
        datasets = request.datasets or list(DATASET_FILENAMES.keys())
        blockers: list[str] = []
        if request.source_mode == request.target_mode:
            blockers.append("source_mode_and_target_mode_are_identical")
        if request.target_mode == StorageMode.shared_local_json:
            blockers.append("migration_target_would_reduce_tenant_isolation")
        if not tenants:
            blockers.append("no_tenants_selected")
        if not datasets:
            blockers.append("no_datasets_selected")

        phases = [
            "Freeze write traffic or enable dual-write capture during migration window.",
            "Export tenant-scoped JSON datasets with checksums.",
            "Create target database schemas/tables with tenant_id, created_at, updated_at, schema_version, and audit columns.",
            "Run dry-run import and compare record counts per tenant/dataset.",
            "Run API smoke tests against migrated repository implementation.",
            "Enable read traffic, then controlled write traffic, then retire JSON adapter for selected tenants.",
        ]
        required_controls = [
            "tenant_id_not_nullable",
            "cross_tenant_query_tests",
            "migration_backup_available",
            "row_count_and_checksum_validation",
            "storage_write_audit_enabled",
        ]
        validation_checks = [
            f"Validate {len(tenants)} tenant(s) across {len(datasets)} dataset(s).",
            "Compare source and target record counts by tenant and dataset.",
            "Verify denied cross-tenant reads using API tests.",
            "Verify rollback/export path before pilot approval.",
        ]
        backout_plan = []
        if request.include_backout_plan:
            backout_plan = [
                "Stop target writes.",
                "Export target records for forensic review.",
                "Restore tenant-scoped JSON backup.",
                "Run storage posture and API smoke tests.",
                "Record migration decision in audit event history.",
            ]
        return StorageMigrationPlanResponse(
            source_mode=request.source_mode,
            target_mode=request.target_mode,
            migration_ready=not blockers,
            phases=phases,
            blockers=blockers,
            required_controls=required_controls,
            validation_checks=validation_checks,
            backout_plan=backout_plan,
        )

    def _tenant_ids(self) -> list[str]:
        return sorted(path.name for path in self.root_dir.iterdir() if path.is_dir())

    def _dataset_path(self, tenant_id: str, dataset: StorageDataset) -> Path:
        filename = DATASET_FILENAMES[dataset]
        tenant_dir = self.root_dir / self._safe_segment(tenant_id)
        tenant_dir.mkdir(parents=True, exist_ok=True)
        return tenant_dir / filename

    def _read_dataset(self, tenant_id: str, dataset: StorageDataset) -> list[dict[str, Any]]:
        path = self._dataset_path(tenant_id, dataset)
        if not path.exists():
            path.write_text("[]\n", encoding="utf-8")
        data = json.loads(path.read_text(encoding="utf-8") or "[]")
        if not isinstance(data, list):
            raise ValueError(f"{path} must contain a JSON array")
        return data

    def _write_dataset(self, tenant_id: str, dataset: StorageDataset, records: list[dict[str, Any]]) -> None:
        path = self._dataset_path(tenant_id, dataset)
        path.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _safe_segment(self, value: str) -> str:
        cleaned = value.strip()
        if not cleaned or "/" in cleaned or "\\" in cleaned or ".." in cleaned:
            raise ValueError("tenant_id must be a safe path segment")
        return cleaned
