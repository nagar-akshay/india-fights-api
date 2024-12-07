from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.routes.auth.controller import get_current_active_user, get_password_hash
from app.routes.users.controller import get_user_by_id
from app.util.db_dependency import get_db
from app.routes.users.models import User
from app.routes.users.schemas import CreateUser, GetUser


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


# ---------------------------
# ----- Crud-Operations -----
# ---------------------------
@router.get("/", response_model=GetUser)
async def get_user(user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    # Get a current login user
    **Access:** Private
    - Current login user.
    """
    current_user = get_user_by_id(user_id=user.id, db=db)
    return current_user


@router.post("/register")
def register_user(user: CreateUser, session: Session = Depends(get_db)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if existing_user and existing_user.disabled:
        raise HTTPException(status_code=400, detail="User is blocked")

    encrypted_password = get_password_hash(user.password)

    new_user = User(email=user.email, password=encrypted_password, first_name=user.first_name, last_name=user.last_name)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "user created successfully"}
