"""Optional database-backed binary attachments; included in ordinary DB backup."""
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.dialects.mysql import LONGBLOB
from database import Base


class AttachmentBlob(Base):
    __tablename__ = "attachment_blobs"
    key = Column(String(512), primary_key=True)
    content = Column(LargeBinary().with_variant(LONGBLOB(), "mysql"), nullable=False)
