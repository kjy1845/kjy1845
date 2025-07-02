"""
生成示例数据脚本
"""
import sys
import os
from datetime import date, datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.patient import Patient, Gender
from app.models.health_plan import HealthPlan, PlanType, PlanStatus
from app.models.patient_health_plan import PatientHealthPlan, AssignmentStatus
from app.models.user import User, UserRole

def create_sample_patients():
    """创建示例患者数据"""
    db: Session = SessionLocal()
    
    try:
        # 检查是否已有示例患者
        if db.query(Patient).first():
            print("示例患者数据已存在!")
            return
        
        patients_data = [
            {
                "patient_id": "P001",
                "name": "张三",
                "gender": Gender.MALE,
                "birth_date": date(1985, 3, 15),
                "phone": "13800138001",
                "email": "zhangsan@example.com",
                "id_card": "110101198503150001",
                "height": 175.0,
                "weight": 70.5,
                "blood_type": "A+",
                "allergies": "花粉过敏",
                "medical_history": "高血压病史"
            },
            {
                "patient_id": "P002",
                "name": "李四",
                "gender": Gender.FEMALE,
                "birth_date": date(1990, 7, 20),
                "phone": "13800138002",
                "email": "lisi@example.com",
                "id_card": "110101199007200002",
                "height": 165.0,
                "weight": 55.0,
                "blood_type": "B+",
                "allergies": "海鲜过敏",
                "medical_history": "糖尿病家族史"
            },
            {
                "patient_id": "P003",
                "name": "王五",
                "gender": Gender.MALE,
                "birth_date": date(1975, 12, 8),
                "phone": "13800138003",
                "email": "wangwu@example.com",
                "id_card": "110101197512080003",
                "height": 180.0,
                "weight": 85.0,
                "blood_type": "O+",
                "medical_history": "冠心病"
            }
        ]
        
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            db.add(patient)
        
        db.commit()
        print("示例患者数据创建成功!")
        
    except Exception as e:
        print(f"创建示例患者数据失败: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_health_plans():
    """创建示例健康方案"""
    db: Session = SessionLocal()
    
    try:
        # 获取医生用户ID
        doctor = db.query(User).filter(User.role == UserRole.DOCTOR).first()
        if not doctor:
            print("未找到医生用户，请先创建医生用户!")
            return
        
        # 检查是否已有示例健康方案
        if db.query(HealthPlan).first():
            print("示例健康方案已存在!")
            return
        
        health_plans_data = [
            {
                "title": "糖尿病饮食管理方案",
                "description": "专为糖尿病患者设计的饮食管理方案",
                "plan_type": PlanType.DIET,
                "status": PlanStatus.ACTIVE,
                "objectives": "控制血糖水平，维持健康体重",
                "instructions": "1. 控制总热量摄入\n2. 少食多餐，定时定量\n3. 选择低升糖指数食物\n4. 多吃蔬菜和全谷物\n5. 限制糖分和饱和脂肪",
                "duration_days": 90,
                "frequency": "每日3餐+2次加餐",
                "target_conditions": "2型糖尿病",
                "contraindications": "1型糖尿病",
                "age_range_min": 18,
                "age_range_max": 70,
                "created_by": doctor.id,
                "is_template": True,
                "is_public": True
            },
            {
                "title": "高血压运动康复方案",
                "description": "适合高血压患者的运动康复计划",
                "plan_type": PlanType.EXERCISE,
                "status": PlanStatus.ACTIVE,
                "objectives": "降低血压，改善心血管功能",
                "instructions": "1. 有氧运动为主\n2. 每次30-45分钟\n3. 强度为中等强度\n4. 避免剧烈运动\n5. 运动前后测量血压",
                "duration_days": 60,
                "frequency": "每周3-4次",
                "target_conditions": "高血压",
                "contraindications": "严重心脏病，血压控制不佳",
                "age_range_min": 30,
                "age_range_max": 75,
                "created_by": doctor.id,
                "is_template": True,
                "is_public": True
            },
            {
                "title": "冠心病用药指导方案",
                "description": "冠心病患者的用药管理方案",
                "plan_type": PlanType.MEDICATION,
                "status": PlanStatus.ACTIVE,
                "objectives": "控制心绞痛，预防心肌梗死",
                "instructions": "1. 按时服用药物\n2. 注意药物副作用\n3. 定期复查心电图\n4. 监测血压和心率\n5. 避免突然停药",
                "duration_days": 180,
                "frequency": "每日2-3次",
                "target_conditions": "冠心病，心绞痛",
                "contraindications": "对药物过敏",
                "age_range_min": 40,
                "age_range_max": 80,
                "created_by": doctor.id,
                "is_template": True,
                "is_public": True
            }
        ]
        
        for plan_data in health_plans_data:
            health_plan = HealthPlan(**plan_data)
            db.add(health_plan)
        
        db.commit()
        print("示例健康方案创建成功!")
        
    except Exception as e:
        print(f"创建示例健康方案失败: {e}")
        db.rollback()
    finally:
        db.close()

def assign_plans_to_patients():
    """为患者分配健康方案"""
    db: Session = SessionLocal()
    
    try:
        # 获取医生
        doctor = db.query(User).filter(User.role == UserRole.DOCTOR).first()
        if not doctor:
            print("未找到医生用户!")
            return
        
        # 获取患者和健康方案
        patients = db.query(Patient).all()
        health_plans = db.query(HealthPlan).all()
        
        if not patients or not health_plans:
            print("请先创建患者和健康方案!")
            return
        
        # 检查是否已有分配记录
        if db.query(PatientHealthPlan).first():
            print("患者健康方案分配记录已存在!")
            return
        
        assignments = [
            # 张三 - 糖尿病饮食方案
            {
                "patient_id": patients[0].id,
                "health_plan_id": health_plans[0].id,
                "assigned_by": doctor.id,
                "status": AssignmentStatus.IN_PROGRESS,
                "start_date": date.today() - timedelta(days=10),
                "end_date": date.today() + timedelta(days=80),
                "custom_instructions": "严格控制碳水化合物摄入",
                "completion_percentage": 25,
                "last_check_date": date.today() - timedelta(days=3)
            },
            # 李四 - 糖尿病饮食方案
            {
                "patient_id": patients[1].id,
                "health_plan_id": health_plans[0].id,
                "assigned_by": doctor.id,
                "status": AssignmentStatus.ASSIGNED,
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=90),
                "custom_instructions": "注意监测血糖变化",
                "completion_percentage": 0
            },
            # 王五 - 冠心病用药方案
            {
                "patient_id": patients[2].id,
                "health_plan_id": health_plans[2].id,
                "assigned_by": doctor.id,
                "status": AssignmentStatus.IN_PROGRESS,
                "start_date": date.today() - timedelta(days=30),
                "end_date": date.today() + timedelta(days=150),
                "custom_instructions": "每日监测血压",
                "completion_percentage": 60,
                "last_check_date": date.today() - timedelta(days=1)
            }
        ]
        
        for assignment_data in assignments:
            assignment = PatientHealthPlan(**assignment_data)
            db.add(assignment)
        
        db.commit()
        print("患者健康方案分配成功!")
        
    except Exception as e:
        print(f"分配患者健康方案失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("正在生成示例数据...")
    create_sample_patients()
    create_sample_health_plans()
    assign_plans_to_patients()
    print("示例数据生成完成!")