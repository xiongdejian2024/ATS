"""Project-scoped immutable shared files and durable evidence references."""
from database import Base
from models.base import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, UniqueConstraint


class LibraryFolder(Base, BaseModel):
    __tablename__ = 'library_folders'
    project_id = Column(String(36), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    parent_id = Column(String(36), ForeignKey('library_folders.id'), nullable=True, index=True)
    name = Column(String(255), nullable=False)


class LibraryFile(Base, BaseModel):
    __tablename__ = 'library_files'
    project_id = Column(String(36), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)
    folder_id = Column(String(36), ForeignKey('library_folders.id'), nullable=True, index=True)
    uploaded_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    sha256 = Column(String(64), nullable=False)
    mime_type = Column(String(100), nullable=False)
    published = Column(Boolean, nullable=False, default=False)
    archived = Column(Boolean, nullable=False, default=False)


class LibraryReference(Base, BaseModel):
    __tablename__ = 'library_references'
    __table_args__ = (UniqueConstraint('file_id', 'entity_kind', 'entity_id', name='uq_library_reference'),)
    file_id = Column(String(36), ForeignKey('library_files.id'), nullable=False, index=True)
    entity_kind = Column(String(30), nullable=False)
    entity_id = Column(String(36), nullable=False, index=True)
    created_by = Column(String(36), ForeignKey('users.id'), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
