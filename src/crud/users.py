from datetime import datetime
from typing import Type
from uuid import UUID

from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session

from annotations import OrderLiteral
from core.security import get_password_hash
from models import User
from schemas.users import UserCreateModel, UserUpdateModel

TUser = Type[User]


class UsersCRUD:
    @classmethod
    def get(cls, db: Session, uid: UUID) -> User | None:
        return db.query(User).filter(User.uid == uid).first()

    @classmethod
    def get_by_email(cls, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @classmethod
    def list_users(
            cls,
            db: Session,
            limit: int,
            offset: int,
            order: OrderLiteral,
            order_by: str,
            is_active: bool | None = None,
            search: str | None = None,
    ) -> tuple[list[TUser], int, int, int]:
        direction = desc if order == 'desc' else asc
        query = db.query(User)
        total_users: int = query.count()
        total_active: int = query.filter(User.is_active.is_(True)).count()
        total_inactive: int = query.filter(User.is_active.is_(False)).count()

        if is_active is not None:
            query = query.filter(User.is_active.is_(is_active))

        if search:
            query = query.filter(or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
            ))

        users = query.order_by(User.is_active.desc(), direction(getattr(User, order_by))).offset(offset).limit(limit).all()
        return users, total_users, total_active, total_inactive

    @classmethod
    def login_user(cls, db: Session, user: TUser) -> TUser:
        user.last_login_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
