login_events = []


def create_login_event_data(event):

    new_event = {
        "id": len(login_events) + 1,
        "username": event.username,
        "ip_address": event.ip_address,
        "status": event.status,
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }

    login_events.append(new_event)

    return new_event


def get_all_login_events():
    return login_events


def get_failed_login_events():

    failed_events = []

    for event in login_events:

        if event["status"].upper() == "FAILED":
            failed_events.append(event)

    return failed_events


def get_suspicious_users_data():

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


def get_risk_summary_data():

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