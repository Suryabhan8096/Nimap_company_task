from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.auth.service import (
    authenticate_user,
    create_user,
    generate_token,
    get_user_by_email,
    get_user_by_username,
)
from app.database.session import get_db
from app.enums import UserRole
from app.models.user import User
from app.schemas.user import RoleUpdate, Token, UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return create_user(db, user_data)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=generate_token(user))


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/users/{user_id}/role", response_model=UserRead)
def update_user_role(
    user_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return db.query(User).all()
