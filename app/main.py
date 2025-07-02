from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, patients, health_plans, patient_health_plans

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="健康管理系统后台API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(patients.router, prefix="/api/patients", tags=["患者管理"])
app.include_router(health_plans.router, prefix="/api/health-plans", tags=["健康方案"])
app.include_router(patient_health_plans.router, prefix="/api/patient-health-plans", tags=["患者健康方案"])

@app.get("/")
def read_root():
    """健康检查端点"""
    return {
        "message": "健康管理系统后台API",
        "version": settings.app_version,
        "status": "运行中"
    }

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "健康"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )