# -*- coding: utf-8 -*-
"""数据库连接和会话管理"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import make_url
from config import settings

# 创建数据库引擎
# MySQL需要添加charset参数以确保UTF-8支持，并设置时区为北京时间
database_url = make_url(settings.DATABASE_URL)
if database_url.drivername in {"postgres", "postgresql"}:
    database_url = database_url.set(drivername="postgresql+psycopg")
connect_args = {}
if database_url.get_backend_name() == "mysql":
    connect_args = {
        "charset": "utf8mb4",
        "init_command": "SET time_zone='+08:00'"
    }

if database_url.get_backend_name() == "postgresql":
    if settings.ENVIRONMENT != "test" and not settings.DATABASE_SCHEMA:
        raise ValueError("PostgreSQL controller requires a dedicated DATABASE_SCHEMA")
    connect_args = {"connect_timeout": settings.DATABASE_CONNECT_TIMEOUT,
                    "prepare_threshold": None, "options": "-c timezone=Asia/Shanghai"}
    if settings.DATABASE_SCHEMA:
        if settings.DATABASE_SCHEMA in {"public", "auth", "storage", "pg_catalog", "information_schema", "realtime", "vault", "extensions", "supabase_migrations", "graphql", "graphql_public", "net"} or settings.DATABASE_SCHEMA.startswith(("pg_", "supabase_")):
            raise ValueError("DATABASE_SCHEMA must be a dedicated ATS schema")
        connect_args["options"] += f" -c search_path={settings.DATABASE_SCHEMA}"

if database_url.get_backend_name() == "sqlite":
    connect_args = {"check_same_thread": False}

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    echo=False,  # 关闭SQL语句输出到控制台
    connect_args=connect_args
)

if database_url.get_backend_name() == "postgresql":
    @event.listens_for(engine, "connect")
    def configure_postgres_session(connection, _record):
        # Session poolers can filter startup options. Set the original ATS
        # timezone contract over SQL, outside a transaction so rollback cannot
        # revert it. Transaction poolers are not supported by this controller.
        previous = connection.autocommit
        connection.autocommit = True
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET SESSION TIME ZONE 'Asia/Shanghai'")
                if settings.DATABASE_SCHEMA:
                    cursor.execute(f'SET SESSION search_path TO "{settings.DATABASE_SCHEMA}"')
        finally:
            connection.autocommit = previous

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

