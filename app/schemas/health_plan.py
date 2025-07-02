from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.health_plan import PlanType, PlanStatus


class HealthPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    plan_type: PlanType
    objectives: Optional[str] = None
    instructions: str
    duration_days: Optional[int] = None
    frequency: Optional[str] = None
    target_conditions: Optional[str] = None
    contraindications: Optional[str] = None
    age_range_min: Optional[int] = None
    age_range_max: Optional[int] = None
    is_template: bool = False
    is_public: bool = False


class HealthPlanCreate(HealthPlanBase):
    pass


class HealthPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    plan_type: Optional[PlanType] = None
    status: Optional[PlanStatus] = None
    objectives: Optional[str] = None
    instructions: Optional[str] = None
    duration_days: Optional[int] = None
    frequency: Optional[str] = None
    target_conditions: Optional[str] = None
    contraindications: Optional[str] = None
    age_range_min: Optional[int] = None
    age_range_max: Optional[int] = None
    is_template: Optional[bool] = None
    is_public: Optional[bool] = None


class HealthPlanResponse(HealthPlanBase):
    id: int
    status: PlanStatus
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class HealthPlanSearchParams(BaseModel):
    title: Optional[str] = None
    plan_type: Optional[PlanType] = None
    status: Optional[PlanStatus] = None
    is_template: Optional[bool] = None
    is_public: Optional[bool] = None
    created_by: Optional[int] = None