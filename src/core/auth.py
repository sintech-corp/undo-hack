from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from config import get_settings
from core.security import verify_password
from crud.users import UsersCRUD
from schemas.users import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{get_settings().api_str}/auth/login")


def authenticate_user(db: Session, email: str, password: str) -> UserModel | None:
    user = UsersCRUD.get_by_email(db, email)
    if not (user and user.is_active):
        return None
    if not verify_password(password, user.hashed_password):
        return None
    user = UsersCRUD.login_user(db, user)
    return UserModel.model_validate(user)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().auth_secret_key, algorithm=get_settings().jwt_algorithm)
    return encoded_jwt
