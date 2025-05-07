# Paladin with Wisdom Layer
from datetime import datetime

violation_log = []
future_threats = []
wisdom_log = []


def scan(input_text: str) -> dict:
    issues = []
    flagged = False
    lowered = input_text.lower()

    if any(word in lowered for word in ["password", "token", "key"]):
        issues.append("Potential credential exposure")
        flagged = True
    if "delete all" in lowered:
        issues.append("Destructive command blocked")
        flagged = True
    if any(w in lowered for w in ["kill", "spy", "exploit"]):
        issues.append("Malicious intent detected")
        flagged = True

    entry = {
        "input": input_text,
        "issues": issues,
        "timestamp": datetime.utcnow().isoformat(),
        "resolved": not flagged,
        "needs_review": flagged
    }
    violation_log.append(entry)
    if flagged:
        wisdom_log.append({"type": "threat", "detail": entry})

    return {"allowed": not flagged, "issues": issues, "timestamp": entry["timestamp"]}


def forecast_threats(modules: list) -> dict:
    risks = []
    for name in modules:
        if "llm" in name or "panel" in name:
            risks.append(f"Unmoderated model access risk in: {name}")
        if "memory" in name and "log" not in name:
            risks.append(f"Memory exposure or overwrite risk in: {name}")
        if "orchestrator" in name:
            risks.append(f"Central execution logic needs validation in: {name}")

    future_threats.extend(risks)
    wisdom_log.append({"type": "forecast", "timestamp": datetime.utcnow().isoformat(), "predictions": risks})
    return {"predicted_threats": risks, "timestamp": datetime.utcnow().isoformat()}


def learn_from_feedback(entry_id: int, outcome: str) -> dict:
    if 0 <= entry_id < len(wisdom_log):
        wisdom_log[entry_id]["feedback"] = outcome
        wisdom_log[entry_id]["timestamp_feedback"] = datetime.utcnow().isoformat()
        return {"message": "Feedback recorded", "entry": wisdom_log[entry_id]}
    return {"error": "Invalid entry ID"}


def wisdom_summary(_: str = None) -> dict:
    return {
        "total_wisdom_entries": len(wisdom_log),
        "last_3": wisdom_log[-3:] if wisdom_log else [],
        "summary": "Paladin is building reflective memory of system threats and decisions."
    }


def run(payload: dict) -> dict:
    action = payload.get("action")
    if action == "scan":
        return scan(payload.get("input", ""))
    elif action == "weekly_summary":
        return weekly_summary()
    elif action == "forecast":
        return forecast_threats(payload.get("modules", []))
    elif action == "learn":
        return learn_from_feedback(payload.get("entry_id", -1), payload.get("outcome", ""))
    elif action == "wisdom":
        return wisdom_summary()
    return {"error": "Unknown action"}