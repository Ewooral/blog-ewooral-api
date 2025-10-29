from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select, SQLModel
from datetime import timedelta
from app.api.deps import get_session
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.models.user import User

router = APIRouter()


class Token(SQLModel):
    access_token: str
    token_type: str


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.uuid, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }