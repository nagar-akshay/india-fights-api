# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.api.v1 import issues, users, auth, forum, whistleblower
from app.db.session import engine
from app.models import Base

settings = Settings()

app = FastAPI(
    title="CivicConnect API",
    description="Backend API for citizen issue reporting and civic engagement",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(issues.router, prefix="/api/v1/issues", tags=["issues"])
app.include_router(forum.router, prefix="/api/v1/forum", tags=["forum"])
app.include_router(whistleblower.router, prefix="/api/v1/whistleblower", tags=["whistleblower"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# app/api/v1/issues.py
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.schemas.issue import IssueCreate, IssueResponse
from app.services import issue_service
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=IssueResponse)
async def create_issue(
    issue: IssueCreate,
    files: List[UploadFile] = File(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new civic issue report"""
    return await issue_service.create_issue(db, issue, files, current_user)

@router.get("/stats")
async def get_issue_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get statistics about reported issues"""
    return await issue_service.get_stats(db)
