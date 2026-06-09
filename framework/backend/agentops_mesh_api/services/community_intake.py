from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class CommunityIntakeService:
    """Local-first public feedback and community-intake service.

    This service is deterministic and file-backed. It models the intake workflow for
    open-source adoption without integrating with live GitHub, CRM, or community tools.
    """

    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = repo_root or Path(__file__).resolve().parents[4]
        self.community_dir = self.repo_root / "community"

    def _load(self, name: str) -> dict[str, Any]:
        path = self.community_dir / name
        return json.loads(path.read_text(encoding="utf-8"))

    def _write(self, name: str, payload: dict[str, Any]) -> None:
        path = self.community_dir / name
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def manifest(self) -> dict[str, Any]:
        return self._load("community_intake_manifest.json")

    def channels(self) -> dict[str, Any]:
        return self._load("feedback_channels.json")

    def use_case_submissions(self) -> dict[str, Any]:
        return self._load("use_case_submissions.json")

    def architecture_critiques(self) -> dict[str, Any]:
        return self._load("architecture_critiques.json")

    def roadmap_feedback(self) -> dict[str, Any]:
        return self._load("roadmap_feedback.json")

    def adoption_feedback(self) -> dict[str, Any]:
        return self._load("adoption_feedback.json")

    def triage_policy(self) -> dict[str, Any]:
        return self._load("community_triage_policy.json")

    def readiness(self) -> dict[str, Any]:
        manifest = self.manifest()
        submissions = self.use_case_submissions().get("submissions", [])
        critiques = self.architecture_critiques().get("critiques", [])
        roadmap = self.roadmap_feedback().get("themes", [])
        adoption = self.adoption_feedback().get("feedback", [])
        channels = self.channels().get("channels", [])
        return {
            "release": manifest["release"],
            "community_readiness_score": manifest["community_readiness_score"],
            "decision": manifest["decision"],
            "channel_count": len(channels),
            "use_case_submission_count": len(submissions),
            "architecture_critique_count": len(critiques),
            "roadmap_theme_count": len(roadmap),
            "adoption_feedback_count": len(adoption),
            "boundaries": manifest.get("boundaries", {}),
            "recommended_next_actions": [
                "Expose the community console from the public site navigation.",
                "Convert the highest-priority roadmap themes into GitHub issues after human review.",
                "Keep live providers and live connectors disabled until production gates are implemented.",
            ],
        }

    def intake_summary(self) -> dict[str, Any]:
        submissions = self.use_case_submissions().get("submissions", [])
        critiques = self.architecture_critiques().get("critiques", [])
        roadmap = self.roadmap_feedback().get("themes", [])
        triaged = sum(1 for item in submissions if item.get("status") in {"triaged", "accepted", "needs_evidence"})
        accepted_critiques = sum(1 for item in critiques if item.get("status") == "accepted")
        high_priority = [item for item in roadmap if item.get("priority") == "high"]
        return {
            "version": "2.5.0",
            "summary_type": "community_intake_summary",
            "triaged_use_cases": triaged,
            "accepted_architecture_critiques": accepted_critiques,
            "high_priority_roadmap_themes": [item["theme_id"] for item in high_priority],
            "dominant_signal": "guided public demo path and scenario expansion",
            "scope_guardrail": "Do not convert the project into a generic chatbot framework or live connector marketplace.",
        }

    def add_use_case_submission(self, record: dict[str, Any]) -> dict[str, Any]:
        required = {"title", "domain", "submitter_role", "business_problem", "agentops_relevance", "data_sensitivity", "expected_value", "status"}
        missing = sorted(required - record.keys())
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        payload = self.use_case_submissions()
        submissions = payload.setdefault("submissions", [])
        new_record = dict(record)
        new_record.setdefault("submission_id", f"uc-community-{len(submissions)+1:03d}")
        new_record.setdefault("triage_lane", self._default_use_case_lane(new_record))
        new_record.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        submissions.append(new_record)
        self._write("use_case_submissions.json", payload)
        return new_record

    def add_architecture_critique(self, record: dict[str, Any]) -> dict[str, Any]:
        required = {"title", "reviewer_role", "area", "finding", "severity", "recommendation", "status"}
        missing = sorted(required - record.keys())
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        payload = self.architecture_critiques()
        critiques = payload.setdefault("critiques", [])
        new_record = dict(record)
        new_record.setdefault("critique_id", f"arch-community-{len(critiques)+1:03d}")
        new_record.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        critiques.append(new_record)
        self._write("architecture_critiques.json", payload)
        return new_record

    @staticmethod
    def _default_use_case_lane(record: dict[str, Any]) -> str:
        text = " ".join(str(record.get(key, "")).lower() for key in ("domain", "business_problem", "agentops_relevance"))
        if any(term in text for term in ["policy", "audit", "governance", "approval", "risk"]):
            return "core_control_plane"
        return "accelerator_candidate"
