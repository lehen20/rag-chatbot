from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from random import choice

from database import SessionLocal
from models import Complaint
from schemas import (
    ComplaintCreate,
    ComplaintRegisterResponse,
    ComplaintStatusResponse
)

complaint_router = APIRouter(prefix="/complaints", tags=["Complaints"])

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: Register a complaint
@complaint_router.post("/register", response_model=ComplaintRegisterResponse)
def register_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    new_complaint = Complaint(
        name=complaint.name,
        mobile_number=complaint.mobile_number,
        complaint_text=complaint.complaint_text
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    return ComplaintRegisterResponse(complaint_id=new_complaint.complaint_id)

# GET: Get status of complaint
@complaint_router.get("/status", response_model=ComplaintStatusResponse)
def get_complaint_status(
    name: str = Query(None),
    mobile_number: str = Query(None),
    complaint_id: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Complaint)

    if complaint_id:
        complaint = query.filter(Complaint.complaint_id == complaint_id).first()
    elif name and mobile_number:
        complaint = query.filter(
            Complaint.name == name,
            Complaint.mobile_number == mobile_number
        ).order_by(Complaint.created_at.desc()).first()
    else:
        raise HTTPException(status_code=400, detail="Provide complaint_id or (name and mobile_number)")

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    if complaint.status == "In Progress":
        complaint.status = choice(["In Progress", "Resolved"])
        db.commit()

    return ComplaintStatusResponse(
        complaint_id=complaint.complaint_id,
        status=complaint.status,
        updated_at=complaint.updated_at,
        created_at=complaint.created_at
    )
