from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class PostIssueSchema(BaseModel):
    issue: str
    status: Optional[str] = None


class GetIssue(BaseModel):
    id: int
    issue: str
    created_at: datetime
