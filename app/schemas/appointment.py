from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.appointment import AppointmentType, AppointmentStatus


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_type: AppointmentType
    scheduled_start: datetime
    scheduled_end: datetime
    title: str
    description: Optional[str] = None
    reason: Optional[str] = None
    chief_complaint: Optional[str] = None
    location: Optional[str] = None
    room_number: Optional[str] = None
    estimated_cost: Optional[str] = None
    patient_health_plan_id: Optional[int] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_type: Optional[AppointmentType] = None
    status: Optional[AppointmentStatus] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    title: Optional[str] = None
    description: Optional[str] = None
    reason: Optional[str] = None
    chief_complaint: Optional[str] = None
    location: Optional[str] = None
    room_number: Optional[str] = None
    estimated_cost: Optional[str] = None
    actual_cost: Optional[str] = None
    reminder_sent: Optional[bool] = None
    reminder_time: Optional[datetime] = None
    doctor_notes: Optional[str] = None
    patient_notes: Optional[str] = None
    cancellation_reason: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    id: int
    status: AppointmentStatus
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    actual_cost: Optional[str]
    reminder_sent: bool
    reminder_time: Optional[datetime]
    doctor_notes: Optional[str]
    patient_notes: Optional[str]
    cancellation_reason: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class AppointmentSearchParams(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    appointment_type: Optional[AppointmentType] = None
    status: Optional[AppointmentStatus] = None
    scheduled_start_from: Optional[datetime] = None
    scheduled_start_to: Optional[datetime] = None
    patient_health_plan_id: Optional[int] = None