from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.deps import get_current_active_doctor
from app.models.patient_health_plan import PatientHealthPlan
from app.models.patient import Patient
from app.models.health_plan import HealthPlan
from app.models.user import User
from app.schemas.patient_health_plan import (
    PatientHealthPlanCreate, PatientHealthPlanUpdate, PatientHealthPlanResponse
)

router = APIRouter()


@router.post("/", response_model=PatientHealthPlanResponse)
def assign_health_plan_to_patient(
    assignment_data: PatientHealthPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """为患者分配健康方案"""
    # 验证患者存在
    patient = db.query(Patient).filter(Patient.id == assignment_data.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    # 验证健康方案存在
    health_plan = db.query(HealthPlan).filter(HealthPlan.id == assignment_data.health_plan_id).first()
    if not health_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康方案不存在"
        )
    
    # 检查是否已经分配了相同的方案
    existing = db.query(PatientHealthPlan).filter(
        PatientHealthPlan.patient_id == assignment_data.patient_id,
        PatientHealthPlan.health_plan_id == assignment_data.health_plan_id,
        PatientHealthPlan.status.in_(["assigned", "in_progress"])
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该患者已被分配此健康方案"
        )
    
    # 创建分配记录
    db_assignment = PatientHealthPlan(
        **assignment_data.model_dump(),
        assigned_by=current_user.id
    )
    
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    
    return db_assignment


@router.get("/", response_model=List[PatientHealthPlanResponse])
def get_patient_health_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    patient_id: Optional[int] = Query(None),
    health_plan_id: Optional[int] = Query(None),
    assigned_by: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取患者健康方案分配列表"""
    query = db.query(PatientHealthPlan)
    
    # 应用过滤条件
    if patient_id:
        query = query.filter(PatientHealthPlan.patient_id == patient_id)
    if health_plan_id:
        query = query.filter(PatientHealthPlan.health_plan_id == health_plan_id)
    if assigned_by:
        query = query.filter(PatientHealthPlan.assigned_by == assigned_by)
    if status:
        query = query.filter(PatientHealthPlan.status == status)
    
    assignments = query.offset(skip).limit(limit).all()
    return assignments


@router.get("/{assignment_id}", response_model=PatientHealthPlanResponse)
def get_patient_health_plan(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取单个患者健康方案分配信息"""
    assignment = db.query(PatientHealthPlan).filter(PatientHealthPlan.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分配记录不存在"
        )
    
    return assignment


@router.put("/{assignment_id}", response_model=PatientHealthPlanResponse)
def update_patient_health_plan(
    assignment_id: int,
    assignment_data: PatientHealthPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """更新患者健康方案分配信息"""
    assignment = db.query(PatientHealthPlan).filter(PatientHealthPlan.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分配记录不存在"
        )
    
    # 更新分配信息
    update_data = assignment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)
    
    db.commit()
    db.refresh(assignment)
    
    return assignment


@router.delete("/{assignment_id}")
def cancel_patient_health_plan(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """取消患者健康方案分配"""
    assignment = db.query(PatientHealthPlan).filter(PatientHealthPlan.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分配记录不存在"
        )
    
    # 设置状态为已取消
    from app.models.patient_health_plan import AssignmentStatus
    assignment.status = AssignmentStatus.CANCELLED
    
    db.commit()
    
    return {"message": "健康方案分配已取消"}


@router.get("/patient/{patient_id}", response_model=List[PatientHealthPlanResponse])
def get_health_plans_by_patient(
    patient_id: int,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取指定患者的所有健康方案"""
    # 验证患者存在
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    query = db.query(PatientHealthPlan).filter(PatientHealthPlan.patient_id == patient_id)
    
    if status:
        query = query.filter(PatientHealthPlan.status == status)
    
    assignments = query.all()
    return assignments