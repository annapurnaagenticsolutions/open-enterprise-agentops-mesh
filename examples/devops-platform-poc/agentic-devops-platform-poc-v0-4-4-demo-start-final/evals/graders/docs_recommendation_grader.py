def grade_docs_recommendation(actual: dict, expected: dict) -> dict:
    expected_status = expected.get("expected_docs_pr_status")
    expected_checklist = expected.get("expected_checklist_name")
    docs = actual.get("documentation", {})
    passed = True
    reasons = []

    if expected_status and docs.get("docs_pr_status") != expected_status:
        passed = False
        reasons.append(f"Expected docs_pr_status={expected_status}, got {docs.get('docs_pr_status')}.")

    if expected_checklist and docs.get("checklist_name") != expected_checklist:
        passed = False
        reasons.append(f"Expected checklist={expected_checklist}, got {docs.get('checklist_name')}.")

    return {"passed": passed, "reasons": reasons}
