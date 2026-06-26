def grade_policy_decision(actual: dict, expected: dict) -> dict:
    expected_decision = expected.get("expected_policy_decision")
    if not expected_decision:
        return {"passed": True, "reason": "No expected policy decision specified."}
    actual_decision = actual.get("governance", {}).get("policy_decision")
    return {
        "passed": actual_decision == expected_decision,
        "expected": expected_decision,
        "actual": actual_decision,
    }
