from dataclasses import dataclass


@dataclass(frozen=True)
class CertificationDecision:
    level: str
    decision: str


class CertificationService:
    def certify(self, total_score: float) -> CertificationDecision:
        if total_score < 40:
            return CertificationDecision("Not Ready", "Reject or redesign before prototype.")
        if total_score < 60:
            return CertificationDecision("Discovery Ready", "Use only for workshop, discovery, or constrained prototype.")
        if total_score < 75:
            return CertificationDecision("Pilot Ready", "Pilot with strict human oversight and limited scope.")
        if total_score < 90:
            return CertificationDecision("Controlled Production Ready", "Production possible with monitoring, controls, and audit.")
        return CertificationDecision("Enterprise Scale Ready", "Ready for broader scale with governance board approval.")
