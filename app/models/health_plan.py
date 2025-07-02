from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class PlanType(enum.Enum):
    DIET = "diet"              # 饮食方案
    EXERCISE = "exercise"      # 运动方案
    MEDICATION = "medication"  # 用药方案
    LIFESTYLE = "lifestyle"    # 生活方式方案
    REHABILITATION = "rehabilitation"  # 康复方案


class PlanStatus(enum.Enum):
    DRAFT = "draft"      # 草稿
    ACTIVE = "active"    # 激活
    PAUSED = "paused"    # 暂停
    COMPLETED = "completed"  # 完成
    CANCELLED = "cancelled"  # 取消


class HealthPlan(Base):
    __tablename__ = "health_plans"

    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False)
    description = Column(Text)
    plan_type = Column(Enum(PlanType), nullable=False)
    status = Column(Enum(PlanStatus), nullable=False, default=PlanStatus.DRAFT)
    
    # 方案内容
    objectives = Column(Text)  # 目标
    instructions = Column(Text, nullable=False)  # 详细指导
    duration_days = Column(Integer)  # 持续天数
    frequency = Column(String(100))  # 频率描述
    
    # 适用条件
    target_conditions = Column(Text)  # 适用病症
    contraindications = Column(Text)  # 禁忌症
    age_range_min = Column(Integer)   # 最小年龄
    age_range_max = Column(Integer)   # 最大年龄
    
    # 创建者信息
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 系统信息
    is_template = Column(Boolean, default=False)  # 是否为模板
    is_public = Column(Boolean, default=False)    # 是否公开
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    creator = relationship("User", backref="created_health_plans")

    def __repr__(self):
        return f"<HealthPlan(id={self.id}, title='{self.title}', type='{self.plan_type}')>"