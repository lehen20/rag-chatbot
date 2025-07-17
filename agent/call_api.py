import requests
from backend.schemas import ComplaintCreate, ComplaintStatusRequest

BASE_URL = "http://localhost:8000/complaints"

def register_complaint(data: dict) -> str:
    validated = ComplaintCreate(**data)
    res = requests.post(f"{BASE_URL}/register", json=validated.dict())
    return res.json()

def get_complaint_status(data: dict) -> str:
    validated = ComplaintStatusRequest(**data)
    params = {k: v for k, v in validated.dict().items() if v}
    res = requests.get(f"{BASE_URL}/status", params=params)
    return res.json()
