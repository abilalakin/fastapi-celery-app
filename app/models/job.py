from sqlalchemy import Column, String, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models import Base

    
class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    status = Column(String, index=True, nullable=False)
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())