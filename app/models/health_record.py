from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class RecordType(enum.Enum):
    VITAL_SIGNS = "vital_signs"      # 生命体征
    LAB_RESULT = "lab_result"        # 检验结果
    EXAMINATION = "examination"       # 体检记录
    MEDICATION = "medication"        # 用药记录
    SYMPTOM = "symptom"             # 症状记录
    PROGRESS = "progress"           # 进展记录


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    
    # 关联信息
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # 记录者
    patient_health_plan_id = Column(Integer, ForeignKey("patient_health_plans.id"))  # 关联的健康方案
    
    # 记录信息
    record_type = Column(Enum(RecordType), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # 生命体征数据
    systolic_pressure = Column(Float)    # 收缩压
    diastolic_pressure = Column(Float)   # 舒张压
    heart_rate = Column(Float)           # 心率
    temperature = Column(Float)          # 体温
    respiratory_rate = Column(Float)     # 呼吸频率
    blood_glucose = Column(Float)        # 血糖
    weight = Column(Float)              # 体重
    height = Column(Float)              # 身高
    
    # 检验结果
    test_name = Column(String(100))      # 检验项目名称
    test_value = Column(String(100))     # 检验值
    test_unit = Column(String(20))       # 单位
    reference_range = Column(String(100)) # 参考范围
    
    # 其他数据
    severity_level = Column(Integer)     # 严重程度 (1-5)
    medication_name = Column(String(100)) # 药物名称
    dosage = Column(String(50))         # 剂量
    frequency = Column(String(50))      # 频次
    
    # 时间信息
    record_date = Column(DateTime(timezone=True), nullable=False)  # 记录时间
    event_date = Column(DateTime(timezone=True))  # 事件发生时间
    
    # 系统信息
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    patient = relationship("Patient", backref="health_records")
    recorder = relationship("User", backref="recorded_health_records")
    patient_health_plan = relationship("PatientHealthPlan", backref="health_records")

    def __repr__(self):
        return f"<HealthRecord(id={self.id}, patient_id={self.patient_id}, type='{self.record_type}')>"