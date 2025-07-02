from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.deps import get_current_active_doctor
from app.models.health_plan import HealthPlan
from app.models.user import User
from app.schemas.health_plan import (
    HealthPlanCreate, HealthPlanUpdate, HealthPlanResponse, HealthPlanSearchParams
)

router = APIRouter()


@router.post("/", response_model=HealthPlanResponse)
def create_health_plan(
    plan_data: HealthPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """创建新的健康方案"""
    db_plan = HealthPlan(
        **plan_data.model_dump(),
        created_by=current_user.id
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan


@router.get("/", response_model=List[HealthPlanResponse])
def get_health_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    title: Optional[str] = Query(None),
    plan_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    is_template: Optional[bool] = Query(None),
    is_public: Optional[bool] = Query(None),
    created_by: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取健康方案列表"""
    query = db.query(HealthPlan)
    
    # 应用过滤条件
    if title:
        query = query.filter(HealthPlan.title.ilike(f"%{title}%"))
    if plan_type:
        query = query.filter(HealthPlan.plan_type == plan_type)
    if status:
        query = query.filter(HealthPlan.status == status)
    if is_template is not None:
        query = query.filter(HealthPlan.is_template == is_template)
    if is_public is not None:
        query = query.filter(HealthPlan.is_public == is_public)
    if created_by:
        query = query.filter(HealthPlan.created_by == created_by)
    
    # 非管理员只能看到公开的方案或自己创建的方案
    from app.models.user import UserRole
    if current_user.role != UserRole.ADMIN:
        query = query.filter(
            (HealthPlan.is_public == True) | 
            (HealthPlan.created_by == current_user.id)
        )
    
    plans = query.offset(skip).limit(limit).all()
    return plans


@router.get("/{plan_id}", response_model=HealthPlanResponse)
def get_health_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取单个健康方案信息"""
    plan = db.query(HealthPlan).filter(HealthPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康方案不存在"
        )
    
    # 权限检查：非管理员只能查看公开的方案或自己创建的方案
    from app.models.user import UserRole
    if (current_user.role != UserRole.ADMIN and 
        not plan.is_public and 
        plan.created_by != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    return plan


@router.put("/{plan_id}", response_model=HealthPlanResponse)
def update_health_plan(
    plan_id: int,
    plan_data: HealthPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """更新健康方案"""
    plan = db.query(HealthPlan).filter(HealthPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康方案不存在"
        )
    
    # 权限检查：只有管理员或创建者可以修改
    from app.models.user import UserRole
    if current_user.role != UserRole.ADMIN and plan.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足：只能修改自己创建的方案"
        )
    
    # 更新方案信息
    update_data = plan_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    db.commit()
    db.refresh(plan)
    
    return plan


@router.delete("/{plan_id}")
def delete_health_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """删除健康方案"""
    plan = db.query(HealthPlan).filter(HealthPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康方案不存在"
        )
    
    # 权限检查：只有管理员或创建者可以删除
    from app.models.user import UserRole
    if current_user.role != UserRole.ADMIN and plan.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足：只能删除自己创建的方案"
        )
    
    # 检查是否有患者正在使用此方案
    from app.models.patient_health_plan import PatientHealthPlan, AssignmentStatus
    active_assignments = db.query(PatientHealthPlan).filter(
        PatientHealthPlan.health_plan_id == plan_id,
        PatientHealthPlan.status.in_([
            AssignmentStatus.ASSIGNED,
            AssignmentStatus.IN_PROGRESS
        ])
    ).first()
    
    if active_assignments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法删除：该方案正在被患者使用"
        )
    
    db.delete(plan)
    db.commit()
    
    return {"message": "健康方案已删除"}


@router.get("/templates/", response_model=List[HealthPlanResponse])
def get_health_plan_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    plan_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取健康方案模板列表"""
    query = db.query(HealthPlan).filter(HealthPlan.is_template == True)
    
    if plan_type:
        query = query.filter(HealthPlan.plan_type == plan_type)
    
    # 非管理员只能看到公开的模板
    from app.models.user import UserRole
    if current_user.role != UserRole.ADMIN:
        query = query.filter(HealthPlan.is_public == True)
    
    templates = query.offset(skip).limit(limit).all()
    return templates