from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from app.models.patient_health_plan import AssignmentStatus


class PatientHealthPlanBase(BaseModel):
    patient_id: int
    health_plan_id: int
    start_date: date
    end_date: Optional[date] = None
    custom_instructions: Optional[str] = None
    custom_objectives: Optional[str] = None
    notes: Optional[str] = None


class PatientHealthPlanCreate(PatientHealthPlanBase):
    pass


class PatientHealthPlanUpdate(BaseModel):
    status: Optional[AssignmentStatus] = None
    end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    custom_instructions: Optional[str] = None
    custom_objectives: Optional[str] = None
    notes: Optional[str] = None
    completion_percentage: Optional[int] = None
    last_check_date: Optional[date] = None


class PatientHealthPlanResponse(PatientHealthPlanBase):
    id: int
    assigned_by: int
    status: AssignmentStatus
    actual_end_date: Optional[date]
    completion_percentage: int
    last_check_date: Optional[date]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PatientHealthPlanSearchParams(BaseModel):
    patient_id: Optional[int] = None
    health_plan_id: Optional[int] = None
    assigned_by: Optional[int] = None
    status: Optional[AssignmentStatus] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None