from datetime import datetime
from app.config.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Enum
from app.routes.users.models import User
import enum


class Status(enum.Enum):
    published = "published"                         # The item has been published, made public.
    approved = "approved"                           # The item has been approved.
    draft = "draft"                                 # The item is awaiting to publish.
    suspended = "suspended"                         # The item or user has been temporarily suspended.
    processing = "processing"                       # The item is being processed.
    rejected = "rejected"                           # The item has been rejected.
    inactive = "inactive"                           # The item is inactive or disabled.
    completed = "completed"                         # The item has been completed or finished.
    canceled = "canceled"                           # The item or process has been canceled.
    expired = "expired"                             # The item or offer has expired.
    waiting_for_approval = "waiting_for_approval"   # Waiting for external approval before proceeding.
    resolved = "resolved"                           # The issue or task has been resolved.
    closed = "closed"                               # The process or item has been closed, no further action required.


class Issues(Base):
    __tablename__ = "issues"

    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True, default=0)
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue = Column(String(length=256))
    status = Column(Enum(Status), nullable=False, default=Status.draft)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, default=datetime.utcnow())