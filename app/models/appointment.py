from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class AppointmentType(enum.Enum):
    CONSULTATION = "consultation"    # 门诊咨询
    FOLLOW_UP = "follow_up"         # 复查
    EXAMINATION = "examination"      # 检查
    TREATMENT = "treatment"         # 治疗
    EMERGENCY = "emergency"         # 急诊


class AppointmentStatus(enum.Enum):
    SCHEDULED = "scheduled"         # 已预约
    CONFIRMED = "confirmed"         # 已确认
    IN_PROGRESS = "in_progress"     # 进行中
    COMPLETED = "completed"         # 已完成
    CANCELLED = "cancelled"         # 已取消
    NO_SHOW = "no_show"            # 爽约


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    
    # 关联信息
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    patient_health_plan_id = Column(Integer, ForeignKey("patient_health_plans.id"))  # 关联的健康方案
    
    # 预约信息
    appointment_type = Column(Enum(AppointmentType), nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.SCHEDULED)
    
    # 时间信息
    scheduled_start = Column(DateTime(timezone=True), nullable=False)
    scheduled_end = Column(DateTime(timezone=True), nullable=False)
    actual_start = Column(DateTime(timezone=True))
    actual_end = Column(DateTime(timezone=True))
    
    # 预约详情
    title = Column(String(200), nullable=False)
    description = Column(Text)
    reason = Column(Text)              # 预约原因
    chief_complaint = Column(Text)     # 主诉
    
    # 地点信息
    location = Column(String(100))     # 地点
    room_number = Column(String(20))   # 房间号
    
    # 费用信息
    estimated_cost = Column(String(50))  # 预估费用
    actual_cost = Column(String(50))     # 实际费用
    
    # 提醒设置
    reminder_sent = Column(Boolean, default=False)  # 是否已发送提醒
    reminder_time = Column(DateTime(timezone=True))  # 提醒时间
    
    # 备注
    doctor_notes = Column(Text)        # 医生备注
    patient_notes = Column(Text)       # 患者备注
    cancellation_reason = Column(Text) # 取消原因
    
    # 系统信息
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    patient = relationship("Patient", backref="appointments")
    doctor = relationship("User", backref="appointments")
    patient_health_plan = relationship("PatientHealthPlan", backref="appointments")

    def __repr__(self):
        return f"<Appointment(id={self.id}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, status='{self.status}')>"