from app.database import SessionLocal
from app.models.login_event import LoginEvent


def create_login_event_data(event):

    db = SessionLocal()

    new_event = LoginEvent(
        username=event.username,
        ip_address=event.ip_address,
        status=event.status
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    db.close()

    return {
        "id": new_event.id,
        "username": new_event.username,
        "ip_address": new_event.ip_address,
        "status": new_event.status,
        "timestamp": new_event.timestamp
    }


def get_all_login_events():

    db = SessionLocal()
    events = db.query(LoginEvent).order_by(LoginEvent.id.desc()).all()
    db.close()

    return events


def get_failed_login_events():

    db = SessionLocal()

    events = db.query(LoginEvent).filter(
        LoginEvent.status.ilike("FAILED")
    ).all()

    db.close()

    return events


def get_suspicious_users_data():

    db = SessionLocal()

    failed_events = db.query(LoginEvent).filter(
        LoginEvent.status.ilike("FAILED")
    ).all()

    db.close()

    failed_counts = {}

    for event in failed_events:
        username = event.username

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


def get_suspicious_ips_data():

    db = SessionLocal()

    failed_events = db.query(LoginEvent).filter(
        LoginEvent.status.ilike("FAILED")
    ).all()

    db.close()

    ip_counts = {}

    for event in failed_events:
        ip = event.ip_address

        if ip not in ip_counts:
            ip_counts[ip] = 0

        ip_counts[ip] += 1

    suspicious_ips = []

    for ip, count in ip_counts.items():
        if count >= 3:
            suspicious_ips.append({
                "ip_address": ip,
                "failed_attempts": count,
                "risk": "HIGH"
            })

    return suspicious_ips


def get_risk_summary_data():

    db = SessionLocal()

    total_events = db.query(LoginEvent).count()

    failed_logins = db.query(LoginEvent).filter(
        LoginEvent.status.ilike("FAILED")
    ).count()

    db.close()

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