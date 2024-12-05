from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    super_admin: bool
    disabled: bool | None = None

    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class GetUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    disabled: bool
    created_at: datetime
    super_admin: bool

    class Config:
        from_attributes = True
