from pydantic import EmailStr, BaseModel

from schemas.base import CamelModel
from schemas.users import UserModel


class APIAuthenticationRequest(CamelModel):
    """Authentication (login) request."""

    email: EmailStr
    password: str


class AuthToken(CamelModel):
    access_token: str
    user: UserModel
    token_type: str
