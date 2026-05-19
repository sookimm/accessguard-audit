from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class LoginEvent(Base):
    __tablename__ = "login_events"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)