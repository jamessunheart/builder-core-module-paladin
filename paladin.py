# paladin module: Proactive Guardian upgrade
from datetime import datetime

violation_log = []
future_threats = []


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
    return {
        "predicted_threats": risks,
        "timestamp": datetime.utcnow().isoformat()
    }

def weekly_summary(_: str = None) -> dict:
    return {
        "total_violations": len(violation_log),
        "recent_flags": violation_log[-5:] if violation_log else [],
        "future_warnings": future_threats[-5:] if future_threats else [],
        "summary": "No threats detected." if not violation_log and not future_threats else f"{len(violation_log)} issues logged, {len(future_threats)} forecasts generated."
    }

def run(payload: dict) -> dict:
    action = payload.get("action")
    if action == "scan":
        return scan(payload.get("input", ""))
    elif action == "weekly_summary":
        return weekly_summary()
    elif action == "forecast":
        return forecast_threats(payload.get("modules", []))
    return {"error": "Unknown action"}