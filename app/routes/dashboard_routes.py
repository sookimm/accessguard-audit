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
def dashboard(request: Request):

    context = {
        "request": request,
        "events": get_all_login_events(),
        "suspicious_users": get_suspicious_users_data(),
        "suspicious_ips": get_suspicious_ips_data(),
        "risk_summary": get_risk_summary_data(),
    }

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=context
    )