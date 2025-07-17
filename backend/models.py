import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False)
    complaint_text = Column(Text, nullable=False)
    status = Column(String, default="In Progress")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
