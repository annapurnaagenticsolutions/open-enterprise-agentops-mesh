from pydantic import BaseModel

from app.kernel.events.models import CanonicalEvent


class BlastRadiusScore(BaseModel):
    score: int
    level: str
    factors: dict[str, int]


ENV_WEIGHTS = {
    "ci": 5,
    "dev": 10,
    "test": 15,
    "qa": 20,
    "staging": 30,
    "prod": 45,
    "production": 45,
}

CRITICALITY_WEIGHTS = {
    "tier_4": 5,
    "tier_3": 10,
    "tier_2": 20,
    "tier_1": 35,
}

ACTION_WEIGHTS = {
    "comment_on_ticket": 3,
    "create_merge_request": 15,
    "rerun_pipeline": 12,
    "auto_merge": 45,
    "merge_pr": 45,
    "rollback_deployment": 50,
    "update_secret": 50,
    "apply_terraform": 55,
}


def calculate_blast_radius(event: CanonicalEvent, proposed_actions: list[dict]) -> BlastRadiusScore:
    env_weight = ENV_WEIGHTS.get(event.environment, 20)
    criticality_weight = CRITICALITY_WEIGHTS.get(event.service.criticality, 10)

    action_weight = 0
    for action in proposed_actions:
        action_weight = max(action_weight, ACTION_WEIGHTS.get(action.get("type", "unknown"), 25))

    reversibility_weight = 5
    if action_weight >= 45:
        reversibility_weight = 20

    factors = {
        "environment": env_weight,
        "service_criticality": criticality_weight,
        "action_type": action_weight,
        "reversibility": reversibility_weight,
    }
    score = sum(factors.values())
    if score < 30:
        level = "low"
    elif score < 70:
        level = "medium"
    else:
        level = "high"

    return BlastRadiusScore(score=score, level=level, factors=factors)
