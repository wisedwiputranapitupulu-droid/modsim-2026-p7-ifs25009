from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base


class Slogan(Base):
    __tablename__ = "slogans"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    language = Column(String(10))  # "id" atau "en"
    request_id = Column(Integer, ForeignKey("slogan_requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
