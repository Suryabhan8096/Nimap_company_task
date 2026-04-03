from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.enums import UserRole


class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    role: UserRole | None = None


class RoleUpdate(BaseModel):
    role: UserRole
