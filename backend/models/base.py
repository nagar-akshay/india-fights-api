# models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, Enum
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum('citizen', 'official', 'admin', name='user_roles'))

# models/issue.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Issue(Base, TimestampMixin):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    location = Column(String)
    coordinates = Column(JSON)  # {lat: float, lng: float}
    category = Column(String)
    status = Column(Enum('pending', 'in_progress', 'resolved', 'closed', name='issue_status'))
    priority = Column(Enum('low', 'medium', 'high', 'urgent', name='issue_priority'))
    reporter_id = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)
    media_urls = Column(JSON)  # List of uploaded media files
    upvotes = Column(Integer, default=0)
    
    reporter = relationship("User", foreign_keys=[reporter_id])
    assignee = relationship("User", foreign_keys=[assigned_to])
    comments = relationship("IssueComment", back_populates="issue")

# models/forum.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

thread_tags = Table(
    'thread_tags',
    Base.metadata,
    Column('thread_id', Integer, ForeignKey('forum_threads.id')),
    Column('tag', String)
)

class ForumThread(Base, TimestampMixin):
    __tablename__ = "forum_threads"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    votes = Column(Integer, default=0)
    tags = relationship("thread_tags")
    
    author = relationship("User")
    comments = relationship("ForumComment", back_populates="thread")

# models/whistleblower.py
from sqlalchemy import Column, Integer, String, JSON
from .base import Base, TimestampMixin

class WhistleblowerReport(Base, TimestampMixin):
    __tablename__ = "whistleblower_reports"

    id = Column(Integer, primary_key=True)
    tracking_id = Column(String, unique=True)  # Public ID for anonymous tracking
    department = Column(String)
    description = Column(String)
    evidence_hashes = Column(JSON)  # Hashes of uploaded files
    encrypted_data = Column(String)  # Additional encrypted details
