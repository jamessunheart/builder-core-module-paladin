# paladin module: evolving security and ethics AI
from datetime import datetime

violation_log = []

def scan(input_text: str) -> dict:
    """
    Check input for alignment with security, privacy, and constructive intent.
    """
    issues = []
    flagged = False
    if any(word in input_text.lower() for word in ["password", "token", "key"]):
        issues.append("Potential credential exposure")
        flagged = True
    if "delete all" in input_text.lower():
        issues.append("Destructive command blocked")
        flagged = True
    if any(w in input_text.lower() for w in ["kill", "spy", "exploit"]):
        issues.append("Malicious intent detected")
        flagged = True

    if flagged:
        violation_log.append({
            "input": input_text,
            "issues": issues,
            "timestamp": datetime.utcnow().isoformat()
        })

    return {
        "allowed": not flagged,
        "issues": issues,
        "timestamp": datetime.utcnow().isoformat()
    }

def weekly_summary(_: str = None) -> dict:
    """
    Summarize violations over the past week.
    """
    return {
        "total_violations": len(violation_log),
        "recent_flags": violation_log[-5:] if violation_log else [],
        "summary": "No threats detected." if not violation_log else f"{len(violation_log)} issues reviewed."
    }

def run(payload: dict) -> dict:
    action = payload.get("action")
    if action == "scan":
        return scan(payload.get("input", ""))
    elif action == "weekly_summary":
        return weekly_summary()
    return {"error": "Unknown action"}