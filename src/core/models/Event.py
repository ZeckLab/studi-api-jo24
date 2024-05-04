from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime, Text, Boolean
from src.core.config.database import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_title = Column(String(255), index=True, nullable=False, unique=True)
    event_description = Column(Text, nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_capacity = Column(Integer, CheckConstraint("event_capacity > 0"), nullable=False)
    event_visible = Column(Boolean, server_default="false")