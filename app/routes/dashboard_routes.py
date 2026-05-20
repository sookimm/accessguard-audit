from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.audit_service import (
    get_all_login_events,
    get_suspicious_users_data,
    get_suspicious_ips_data,
    get_risk_summary_data,
)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard")
def dashboard(
    request: Request,
    status: str = None,
    username: str = None,
    ip_address: str = None
):
    has_filter = bool(status or username or ip_address)

    context = {
        "request": request,

        "recent_events": get_all_login_events()[:10],

        "filtered_events": get_all_login_events(
            status=status,
            username=username,
            ip_address=ip_address
        ) if has_filter else [],

        "suspicious_users": get_suspicious_users_data(),
        "suspicious_ips": get_suspicious_ips_data(),
        "risk_summary": get_risk_summary_data(),

        "selected_status": status or "",
        "selected_username": username or "",
        "selected_ip": ip_address or "",
        "has_filter": has_filter,
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=context
    )