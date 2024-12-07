from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse
from starlette import status
from sqlalchemy.orm import Session
from typing import List

from app.routes.api.controller import tuck_issue_user, get_user_issue_list, get_issue_by_user
from app.routes.api.schemas import PostIssueSchema, GetIssue
from app.routes.auth.controller import get_current_active_user
from app.routes.users.models import User
from app.util.db_dependency import get_db


router = APIRouter(
    tags=["Issues"],
)


@router.post("/issue")
async def post_issue(issue_schema: PostIssueSchema, user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    # post issue
    The user can insert the issue.
    **Access:** Private.
    """
    if await tuck_issue_user(user.id, issue=issue_schema.issue, status=issue_schema.status, db=db):
        return JSONResponse(status_code=200, content={"detail": "Successfully posted the issue."})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while posting the issue.")


@router.get("/issues", response_model=List[GetIssue])
async def get_issues_list(user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    # get current user issues list
    The user can get the list of issues.
    **Access:** Private.
    """
    get_issues = get_user_issue_list(user.id, db)
    return get_issues


@router.get("/issue/{issue}", response_model=GetIssue)
async def get_issue(issue: int, user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    # get an issue to the current user
    The user can get the list of issues.
    **Access:** Private.
    """
    issue = get_issue_by_user(user.id, issue, db)
    return issue
