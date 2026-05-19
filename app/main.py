from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.audit_routes import router

from app.database import engine
from app.database import Base

from app.models.login_event import LoginEvent

from app.routes.dashboard_routes import router as dashboard_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)

app.include_router(dashboard_router)