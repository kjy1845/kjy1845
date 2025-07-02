from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.utils.deps import get_current_active_doctor
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import (
    PatientCreate, PatientUpdate, PatientResponse, PatientSearchParams
)

router = APIRouter()


@router.post("/", response_model=PatientResponse)
def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """创建新患者"""
    # 检查患者编号是否已存在
    if db.query(Patient).filter(Patient.patient_id == patient_data.patient_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="患者编号已存在"
        )
    
    # 检查身份证号是否已存在（如果提供了身份证号）
    if patient_data.id_card and db.query(Patient).filter(Patient.id_card == patient_data.id_card).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="身份证号已存在"
        )
    
    db_patient = Patient(**patient_data.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    return db_patient


@router.get("/", response_model=List[PatientResponse])
def get_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: Optional[str] = Query(None),
    patient_id: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    id_card: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取患者列表"""
    query = db.query(Patient)
    
    # 应用过滤条件
    if name:
        query = query.filter(Patient.name.ilike(f"%{name}%"))
    if patient_id:
        query = query.filter(Patient.patient_id.ilike(f"%{patient_id}%"))
    if phone:
        query = query.filter(Patient.phone.ilike(f"%{phone}%"))
    if id_card:
        query = query.filter(Patient.id_card.ilike(f"%{id_card}%"))
    if is_active is not None:
        query = query.filter(Patient.is_active == is_active)
    
    patients = query.offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """获取单个患者信息"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """更新患者信息"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    # 检查身份证号冲突（如果要更新身份证号）
    if patient_data.id_card and patient_data.id_card != patient.id_card:
        existing = db.query(Patient).filter(
            Patient.id_card == patient_data.id_card,
            Patient.id != patient_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="身份证号已存在"
            )
    
    # 更新患者信息
    update_data = patient_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)
    
    db.commit()
    db.refresh(patient)
    
    return patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """删除患者（软删除）"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
    patient.is_active = False
    db.commit()
    
    return {"message": "患者已删除"}


@router.get("/search/", response_model=List[PatientResponse])
def search_patients(
    query: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    """搜索患者（按姓名、患者编号、电话或身份证号）"""
    patients = db.query(Patient).filter(
        or_(
            Patient.name.ilike(f"%{query}%"),
            Patient.patient_id.ilike(f"%{query}%"),
            Patient.phone.ilike(f"%{query}%"),
            Patient.id_card.ilike(f"%{query}%")
        ),
        Patient.is_active == True
    ).limit(limit).all()
    
    return patients