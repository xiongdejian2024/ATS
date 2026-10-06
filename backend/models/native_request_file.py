"""项目请求文件：字节不可变；移除仅隐藏，已冻结执行仍可读取原字节。"""

from sqlalchemy import Column, String, Integer, LargeBinary, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGBLOB
from database import Base
from models.base import BaseModel


class NativeRequestFile(Base, BaseModel):
    __tablename__ = "native_request_files"
    project_id = Column(
        String(36),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name = Column(String(255), nullable=False)
    content_type = Column(String(255), nullable=False)
    byte_length = Column(Integer, nullable=False)
    sha256 = Column(String(64), nullable=False)
    content = Column(LargeBinary().with_variant(LONGBLOB(), "mysql"), nullable=False)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)
