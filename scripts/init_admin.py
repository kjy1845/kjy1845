"""
初始化管理员用户脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.core.database import Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

def create_admin_user():
    """创建默认管理员用户"""
    db: Session = SessionLocal()
    
    try:
        # 检查是否已存在管理员用户
        admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if admin_user:
            print("管理员用户已存在!")
            return
        
        # 创建管理员用户
        admin_data = {
            "username": "admin",
            "email": "admin@health.com",
            "hashed_password": get_password_hash("admin123"),
            "full_name": "系统管理员",
            "role": UserRole.ADMIN,
            "is_active": True,
            "is_verified": True
        }
        
        admin_user = User(**admin_data)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"管理员用户创建成功!")
        print(f"用户名: admin")
        print(f"密码: admin123")
        print(f"邮箱: admin@health.com")
        print(f"请在生产环境中修改默认密码!")
        
    except Exception as e:
        print(f"创建管理员用户失败: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_doctor():
    """创建示例医生用户"""
    db: Session = SessionLocal()
    
    try:
        # 检查是否已存在示例医生
        doctor = db.query(User).filter(User.username == "doctor1").first()
        if doctor:
            print("示例医生用户已存在!")
            return
        
        # 创建示例医生
        doctor_data = {
            "username": "doctor1",
            "email": "doctor1@health.com",
            "hashed_password": get_password_hash("doctor123"),
            "full_name": "张医生",
            "role": UserRole.DOCTOR,
            "specialty": "内科",
            "license_number": "110000123456",
            "department": "内科",
            "is_active": True,
            "is_verified": True
        }
        
        doctor = User(**doctor_data)
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        
        print(f"示例医生用户创建成功!")
        print(f"用户名: doctor1")
        print(f"密码: doctor123")
        print(f"邮箱: doctor1@health.com")
        
    except Exception as e:
        print(f"创建示例医生用户失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("正在初始化用户...")
    create_admin_user()
    create_sample_doctor()
    print("用户初始化完成!")