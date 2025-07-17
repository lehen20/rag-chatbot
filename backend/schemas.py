from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    name: str
    mobile_number: str
    complaint_text: str

class ComplaintStatusRequest(BaseModel):
    name: Optional[str] = None
    mobile_number: Optional[str] = None
    complaint_id: Optional[str] = None

class ComplaintRegisterResponse(BaseModel):
    complaint_id: str

class ComplaintStatusResponse(BaseModel):
    complaint_id: str
    status: str
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
