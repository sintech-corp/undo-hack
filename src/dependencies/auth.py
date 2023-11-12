from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from config import get_settings
from core.auth import oauth2_scheme
from crud.users import UsersCRUD
from dependencies.db import get_db
from schemas.users import UserModel


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().auth_secret_key, algorithms=[get_settings().jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = UsersCRUD.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return UserModel.model_validate(user)


def get_current_active_user(user: UserModel = Depends(get_current_user)) -> UserModel:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def get_current_staff_user(user: UserModel = Depends(get_current_active_user)) -> UserModel:
    if not user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a staff")
    return user


def get_current_superuser(user: UserModel = Depends(get_current_staff_user)) -> UserModel:
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a superuser")
    return user


class PermissionChecker:

    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: UserModel = Depends(get_current_active_user)) -> bool:
        for r_perm in self.required_permissions:
            if r_perm not in user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Permissions'
                )
        return True
