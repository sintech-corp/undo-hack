from datetime import datetime
from typing import Literal

from pydantic import EmailStr, SecretStr

from schemas.base import CamelModel, UidSchema, UpdatedAtSchema, CreatedAtSchema, ORMModel
from schemas.queries import PaginationResponse, OrderQuery


class UserBase(CamelModel):
    email: EmailStr
    phone_number: str

    first_name: str
    last_name: str
    middle_name: str | None = None

    is_active: bool = True
    is_staff: bool = True
    is_superuser: bool = False
    position: str | None = None


class UserModel(UserBase, UidSchema, CreatedAtSchema, UpdatedAtSchema, ORMModel):
    last_login_at: datetime | None = None


class UserCreateModel(UserBase):
    password: SecretStr


class UserUpdateModel(UserBase):
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str | None = None

    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None

    is_active: bool | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None
    position: str | None = None


class UsersListResponse(PaginationResponse):
    users: list[UserModel]
    total_active: int
    total_disabled: int


class UsersOrderingQuery(OrderQuery):
    order_by: Literal['name'] = 'name'


class UsersFilterQuery(CamelModel):
    is_active: bool | None = None
    search: str | None = None
