from sqlalchemy import Column, Integer, String, Date, Enum, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    patient_id = Column(String(20), unique=True, index=True, nullable=False)  # 患者编号
    name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    birth_date = Column(Date, nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    id_card = Column(String(18), unique=True)  # 身份证号
    
    # 联系信息
    address = Column(Text)
    emergency_contact = Column(String(100))  # 紧急联系人
    emergency_phone = Column(String(20))     # 紧急联系电话
    
    # 健康信息
    height = Column(Float)  # 身高(cm)
    weight = Column(Float)  # 体重(kg)
    blood_type = Column(String(10))  # 血型
    allergies = Column(Text)  # 过敏史
    medical_history = Column(Text)  # 病史
    current_medications = Column(Text)  # 当前用药
    
    # 系统信息
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Patient(id={self.id}, patient_id='{self.patient_id}', name='{self.name}')>"