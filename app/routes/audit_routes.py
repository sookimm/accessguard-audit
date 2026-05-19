from fastapi import APIRouter
from pydantic import BaseModel

from app.services.audit_service import (
    create_login_event_data,
    get_all_login_events,
    get_failed_login_events,
    get_suspicious_users_data,
    get_risk_summary_data,
)

router = APIRouter()


class LoginEventRequest(BaseModel):
    username: str
    ip_address: str
    status: str


@router.get("/")
def root():
    return {"message": "AccessGuard Audit API is running"}


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "accessguard-audit"
    }


@router.post("/login-events")
def create_login_event(event: LoginEventRequest):
    return create_login_event_data(event)


@router.get("/login-events")
def get_login_events():
    return get_all_login_events()


@router.get("/audit/failed-logins")
def get_failed_logins():
    return get_failed_login_events()


@router.get("/audit/suspicious-users")
def get_suspicious_users():
    return get_suspicious_users_data()


@router.get("/audit/risk-summary")
def get_risk_summary():
    return get_risk_summary_data()