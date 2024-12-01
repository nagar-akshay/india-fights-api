from fastapi import HTTPException
from sqlalchemy.orm import Session
import enum
from app.routes.api.models import Issues


async def tuck_issue_user(user_id: int, issue: str, status: enum, db: Session):
    issue = Issues(user_id=user_id, issue=issue, status=status)
    db.add(issue)
    db.commit()
    return True


def get_user_issue_list(user_id: int, db: Session):
    issues = db.query(Issues.id, Issues.issue, Issues.created_at).filter(user_id == user_id).all()

    if not issues:
        raise HTTPException(
            status_code=404,
            detail="There is no issue to the user."
        )
    return issues


def get_issue_by_user(user_id: int, issue_id: int,  db: Session):
    issue = db.query(Issues.id, Issues.issue, Issues.created_at).filter(user_id == user_id, Issues.id == issue_id).first()

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="There is no issue to the user with id."
        )
    return issue
