from agentops_mesh_api.models.schemas import RiskFactors, SensitivityLevel, ImpactLevel, ReversibilityLevel


class RiskClassifierService:
    def classify(self, autonomy_level: int, factors: RiskFactors) -> tuple[str, int, list[str]]:
        score = 0
        controls: list[str] = []

        score += autonomy_level * 8

        if factors.data_sensitivity == SensitivityLevel.medium:
            score += 10
            controls.append("Apply role-based data access and source-level permissions.")
        elif factors.data_sensitivity == SensitivityLevel.high:
            score += 20
            controls.append("Require sensitive-data handling, redaction, and explicit access controls.")

        if factors.external_action:
            score += 18
            controls.append("Require tool-action approval or reversible action guardrails.")

        if factors.financial_impact == ImpactLevel.low:
            score += 5
        elif factors.financial_impact == ImpactLevel.medium:
            score += 12
            controls.append("Require financial threshold controls and approval matrix.")
        elif factors.financial_impact == ImpactLevel.high:
            score += 22
            controls.append("Require human approval for financial decisions and exception handling.")

        if factors.reversibility == ReversibilityLevel.moderate:
            score += 8
            controls.append("Define rollback and exception-management procedure.")
        elif factors.reversibility == ReversibilityLevel.hard:
            score += 18
            controls.append("Block autonomous execution for hard-to-reverse actions.")

        if factors.customer_or_employee_impact == ImpactLevel.medium:
            score += 10
            controls.append("Require escalation route for customer or employee-impacting cases.")
        elif factors.customer_or_employee_impact == ImpactLevel.high:
            score += 20
            controls.append("Require human review for high-impact customer or employee outcomes.")

        if score >= 75:
            level = "Critical"
        elif score >= 55:
            level = "High"
        elif score >= 30:
            level = "Medium"
        else:
            level = "Low"

        if not controls:
            controls.append("Maintain standard monitoring, audit logging, and evaluation review.")

        return level, score, sorted(set(controls))
