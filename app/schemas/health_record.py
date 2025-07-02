from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.health_record import RecordType


class HealthRecordBase(BaseModel):
    patient_id: int
    record_type: RecordType
    title: str
    description: Optional[str] = None
    patient_health_plan_id: Optional[int] = None
    
    # 生命体征数据
    systolic_pressure: Optional[float] = None
    diastolic_pressure: Optional[float] = None
    heart_rate: Optional[float] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[float] = None
    blood_glucose: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    
    # 检验结果
    test_name: Optional[str] = None
    test_value: Optional[str] = None
    test_unit: Optional[str] = None
    reference_range: Optional[str] = None
    
    # 其他数据
    severity_level: Optional[int] = None
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    
    record_date: datetime
    event_date: Optional[datetime] = None


class HealthRecordCreate(HealthRecordBase):
    pass


class HealthRecordUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    systolic_pressure: Optional[float] = None
    diastolic_pressure: Optional[float] = None
    heart_rate: Optional[float] = None
    temperature: Optional[float] = None
    respiratory_rate: Optional[float] = None
    blood_glucose: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    test_name: Optional[str] = None
    test_value: Optional[str] = None
    test_unit: Optional[str] = None
    reference_range: Optional[str] = None
    severity_level: Optional[int] = None
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    record_date: Optional[datetime] = None
    event_date: Optional[datetime] = None


class HealthRecordResponse(HealthRecordBase):
    id: int
    recorded_by: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class HealthRecordSearchParams(BaseModel):
    patient_id: Optional[int] = None
    record_type: Optional[RecordType] = None
    recorded_by: Optional[int] = None
    patient_health_plan_id: Optional[int] = None
    record_date_from: Optional[datetime] = None
    record_date_to: Optional[datetime] = None