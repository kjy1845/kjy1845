# 健康管理系统后台

一个完整的健康管理系统后台API，基于FastAPI构建，提供患者管理、健康方案管理、健康记录跟踪等功能。

## 主要功能

### 🏥 核心模块

- **用户管理**: 支持管理员、医生、护士等不同角色
- **患者管理**: 完整的患者信息管理，包括基本信息、健康档案
- **健康方案管理**: 创建和管理各类健康方案（饮食、运动、用药等）
- **健康记录**: 记录患者的生命体征、检验结果、用药记录等
- **预约管理**: 医患预约系统
- **方案分配**: 为患者分配个性化健康方案

### � 安全特性

- JWT身份验证
- 基于角色的权限控制
- 密码哈希加密
- CORS支持

### � 数据管理

- PostgreSQL数据库
- SQLAlchemy ORM
- Alembic数据库迁移
- 自动化数据验证

## 系统架构

```
app/
├── core/           # 核心配置
│   ├── config.py   # 应用配置
│   ├── database.py # 数据库连接
│   └── security.py # 安全认证
├── models/         # 数据库模型
│   ├── user.py     # 用户模型
│   ├── patient.py  # 患者模型
│   ├── health_plan.py # 健康方案模型
│   └── ...
├── schemas/        # Pydantic模型
├── api/           # API路由
│   ├── auth.py    # 认证API
│   ├── patients.py # 患者管理API
│   └── ...
├── utils/         # 工具函数
└── main.py        # 主应用
```

## 数据库模型

### 核心实体

1. **User** - 用户（管理员、医生、护士）
2. **Patient** - 患者
3. **HealthPlan** - 健康方案
4. **PatientHealthPlan** - 患者健康方案关联
5. **HealthRecord** - 健康记录
6. **Appointment** - 预约

### 关系图

```
User (医生) ---> HealthPlan (创建健康方案)
User (医生) ---> PatientHealthPlan (分配方案给患者)
Patient ---> PatientHealthPlan (被分配健康方案)
Patient ---> HealthRecord (健康记录)
Patient ---> Appointment (预约)
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- PostgreSQL 12+
- Redis (可选)

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 环境配置

复制环境变量示例文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接等信息：

```env
DATABASE_URL=postgresql://user:password@localhost:5432/health_management
SECRET_KEY=your-secret-key-here
```

### 4. 数据库初始化

```bash
# 初始化Alembic
alembic init alembic

# 创建第一个迁移
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

### 5. 创建初始用户

```bash
python scripts/init_admin.py
```

默认创建的用户：
- 管理员: `admin` / `admin123`
- 示例医生: `doctor1` / `doctor123`

### 6. 启动服务

#### 开发环境
```bash
python scripts/run_dev.py
```

#### 生产环境
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

服务启动后可访问：
- API文档: http://localhost:8000/docs
- 交互式文档: http://localhost:8000/redoc

## API接口

### 认证

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册

### 患者管理

- `GET /api/patients/` - 获取患者列表
- `POST /api/patients/` - 创建新患者
- `GET /api/patients/{id}` - 获取患者详情
- `PUT /api/patients/{id}` - 更新患者信息
- `DELETE /api/patients/{id}` - 删除患者

### 健康方案

- `GET /api/health-plans/` - 获取健康方案列表
- `POST /api/health-plans/` - 创建健康方案
- `GET /api/health-plans/{id}` - 获取方案详情
- `PUT /api/health-plans/{id}` - 更新方案
- `DELETE /api/health-plans/{id}` - 删除方案

### 方案分配

- `POST /api/patient-health-plans/` - 为患者分配方案
- `GET /api/patient-health-plans/` - 获取分配列表
- `PUT /api/patient-health-plans/{id}` - 更新分配信息

## 使用示例

### 1. 用户登录

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 2. 创建患者

```bash
curl -X POST "http://localhost:8000/api/patients/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P001",
    "name": "张三",
    "gender": "male",
    "birth_date": "1990-01-01",
    "phone": "13800138000"
  }'
```

### 3. 创建健康方案

```bash
curl -X POST "http://localhost:8000/api/health-plans/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "糖尿病饮食方案",
    "plan_type": "diet",
    "instructions": "低糖低脂饮食，少食多餐...",
    "duration_days": 30
  }'
```

## 开发指南

### 代码结构

- 遵循FastAPI最佳实践
- 使用Pydantic进行数据验证
- SQLAlchemy ORM进行数据库操作
- 清晰的分层架构

### 添加新功能

1. 在 `models/` 中定义数据模型
2. 在 `schemas/` 中定义Pydantic模型
3. 在 `api/` 中创建路由
4. 在 `main.py` 中注册路由

### 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "Add new table"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 部署

### Docker部署

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置

- 使用强密码和随机SECRET_KEY
- 配置HTTPS
- 设置适当的CORS策略
- 使用生产级数据库
- 配置日志记录
- 设置监控和健康检查

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件

---

*健康管理系统 - 专业的医疗健康管理解决方案*
