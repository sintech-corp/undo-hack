from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config import get_settings
from core.auth import authenticate_user, create_access_token
from dependencies.auth import get_current_active_user
from dependencies.db import get_db
from schemas.auth import APIAuthenticationRequest, AuthToken
from schemas.users import UserModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=AuthToken)
def login(auth_data: APIAuthenticationRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, auth_data.email, auth_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "user": user,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserModel)
def me(db: Session = Depends(get_db), user: UserModel = Depends(get_current_active_user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
