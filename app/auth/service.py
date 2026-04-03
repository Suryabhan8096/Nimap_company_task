from __future__ import annotations

from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password, create_access_token
from app.enums import UserRole
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate, role: UserRole = UserRole.CLIENT) -> User:
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def generate_token(user: User) -> str:
    return create_access_token(data={"sub": str(user.id), "role": user.role.value})
