import reflex as rx
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_session
from app.core.security import get_password_hash
from app.models.user import User, UserCreate, UserRead, Role

router = APIRouter()


@router.post(
    "/", response_model=UserRead, status_code=201, summary="Register a new user"
)
def create_user(
    *, session: Session = Depends(get_session), user_in: UserCreate
) -> User:
    """
    Create new user.
    """
    db_user = session.exec(select(User).where(User.email == user_in.email)).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    reader_role = session.exec(select(Role).where(Role.name == "reader")).first()
    if not reader_role:
        raise HTTPException(status_code=500, detail="Default reader role not found")
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        roles=[reader_role],
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user