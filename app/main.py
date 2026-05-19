from fastapi import FastAPI

from app.routes.audit_routes import router

from app.database import engine
from app.database import Base

from app.models.login_event import LoginEvent

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)