from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

login_events = []


class LoginEventRequest(BaseModel):
    username: str
    ip_address: str
    status: str


@app.get("/")
def root():
    return {"message": "AccessGuard Audit API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "accessguard-audit"
    }


@app.post("/login-events")
def create_login_event(event: LoginEventRequest):
    new_event = {
        "id": len(login_events) + 1,
        "username": event.username,
        "ip_address": event.ip_address,
        "status": event.status,
        "timestamp": datetime.now().isoformat()
    }

    login_events.append(new_event)

    return new_event


@app.get("/login-events")
def get_login_events():
    return login_events

@app.get("/audit/failed-logins")
def get_failed_logins():
    failed_events = []

    for event in login_events:
        if event["status"].upper() == "FAILED":
            failed_events.append(event)

    return failed_events


@app.get("/audit/suspicious-users")
def get_suspicious_users():

    failed_counts = {}

    for event in login_events:

        if event["status"].upper() == "FAILED":

            username = event["username"]

            if username not in failed_counts:
                failed_counts[username] = 0

            failed_counts[username] += 1

    suspicious_users = []

    for username, count in failed_counts.items():

        if count >= 3:

            suspicious_users.append({
                "username": username,
                "failed_attempts": count,
                "risk": "HIGH"
            })

    return suspicious_users


@app.get("/audit/risk-summary")
def get_risk_summary():

    total_events = len(login_events)

    failed_logins = 0

    for event in login_events:

        if event["status"].upper() == "FAILED":
            failed_logins += 1

    risk_level = "LOW"

    if failed_logins >= 3:
        risk_level = "HIGH"

    elif failed_logins >= 1:
        risk_level = "MEDIUM"

    return {
        "total_events": total_events,
        "failed_logins": failed_logins,
        "risk_level": risk_level
    }