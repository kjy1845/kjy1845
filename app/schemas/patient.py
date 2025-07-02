from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
from app.models.patient import Gender


class PatientBase(BaseModel):
    name: str
    gender: Gender
    birth_date: date
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    id_card: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None


class PatientCreate(PatientBase):
    patient_id: str


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    id_card: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    current_medications: Optional[str] = None
    is_active: Optional[bool] = None


class PatientResponse(PatientBase):
    id: int
    patient_id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PatientSearchParams(BaseModel):
    name: Optional[str] = None
    patient_id: Optional[str] = None
    phone: Optional[str] = None
    id_card: Optional[str] = None
    is_active: Optional[bool] = True