from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.extensions import Base


class SloganRequest(Base):
    __tablename__ = "slogan_requests"

    id = Column(Integer, primary_key=True)
    entity_name = Column(String(200))
    description = Column(String(500))
    core_values = Column(String(300))
    language = Column(String(20), default="id")  # "id", "en", atau "both"
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
