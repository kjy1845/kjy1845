from sqlalchemy import Column, Integer, DateTime, Date, Text, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class AssignmentStatus(enum.Enum):
    ASSIGNED = "assigned"      # 已分配
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"    # 已完成
    PAUSED = "paused"         # 已暂停
    CANCELLED = "cancelled"    # 已取消


class PatientHealthPlan(Base):
    __tablename__ = "patient_health_plans"

    id = Column(Integer, primary_key=True, index=True)
    
    # 关联信息
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    health_plan_id = Column(Integer, ForeignKey("health_plans.id"), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # 分配医生
    
    # 执行信息
    status = Column(Enum(AssignmentStatus), nullable=False, default=AssignmentStatus.ASSIGNED)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    actual_end_date = Column(Date)  # 实际结束日期
    
    # 个性化调整
    custom_instructions = Column(Text)  # 个性化指导
    custom_objectives = Column(Text)    # 个性化目标
    notes = Column(Text)               # 备注
    
    # 进度跟踪
    completion_percentage = Column(Integer, default=0)  # 完成百分比
    last_check_date = Column(Date)      # 最后检查日期
    
    # 系统信息
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    patient = relationship("Patient", backref="health_plans")
    health_plan = relationship("HealthPlan", backref="patient_assignments")
    assigned_doctor = relationship("User", backref="assigned_plans")

    def __repr__(self):
        return f"<PatientHealthPlan(id={self.id}, patient_id={self.patient_id}, plan_id={self.health_plan_id})>"