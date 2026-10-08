# ATS Backend - 自动化测试管理平台后端服务

## 项目简介

企业级自动化测试管理平台的后端服务，基于 FastAPI 构建，提供完整的测试管理 API。

## 技术栈

- **框架**: FastAPI
- **数据库**: MySQL
- **缓存**: Redis
- **消息队列**: RabbitMQ + Celery
- **文件存储**: MinIO/S3
- **认证**: JWT + RBAC

## 快速开始

### 使用 uv 安装依赖

```bash
# 安装 uv (如果还没有安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装项目依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate
```

### 环境配置

复制 `.env.example` 为 `.env` 并配置环境变量：

```bash
cp .env.example .env
```

### 数据库迁移

```bash
# 初始化数据库
alembic upgrade head
```

### 创建管理员用户

初始化 PostgreSQL 专用 schema 后，在尚无任何用户时显式创建第一位管理员：

```bash
# 在 backend/ 目录运行；替换用户名和邮箱，密码由隐藏终端提示输入两次
uv run python scripts/create_admin.py --username your-login --email you@example.com
```

密码没有默认值，至少 16 个字符、最多 72 个 UTF-8 字节，并须满足脚本的强度检查。
不要把密码写进命令参数、代码、`.env`、日志或持久部署配置。无交互终端时，只能由
受保护的机制为这一次进程注入 `ADMIN_PASSWORD`，不从可回显的标准输入读取密码。
已有任何用户都会拒绝执行，不重置密码、不启用已有账号、不追加管理员授权。
该安全引导命令支持 PostgreSQL 和隔离测试用 SQLite；MySQL 会明确拒绝且不写入。
角色、权限和用户在同一个事务中写入，失败则回滚。
完整输入要求、一次性环境变量示例和验证方式见 [管理员引导说明](../docs/ADMIN_BOOTSTRAP.md)。

### 运行服务

```bash
# 开发模式
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 或使用 uv
uv run uvicorn main:app --reload
```

### 运行 Celery Worker

```bash
celery -A core.celery_app worker --loglevel=info
```

## 项目结构

```
backend/
├── main.py                 # FastAPI应用入口
├── config.py              # 配置文件
├── database.py            # 数据库连接
├── models/                # 数据模型
├── schemas/               # Pydantic模式
├── api/                   # API路由
├── services/              # 业务逻辑
├── core/                  # 核心功能
├── utils/                 # 工具函数
├── tests/                 # 测试文件
└── alembic/               # 数据库迁移
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 开发

```bash
# 代码格式化
uv run black .
uv run isort .

# 类型检查
uv run mypy .

# 运行测试
uv run pytest
```

