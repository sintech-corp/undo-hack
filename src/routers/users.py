from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.users import UsersCRUD
from dependencies.auth import get_current_staff_user
from dependencies.db import get_db
from schemas.queries import PaginationQuery
from schemas.users import UserModel, UsersListResponse, UsersOrderingQuery, UsersFilterQuery

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=UsersListResponse)
@router.get("/", response_model=UsersListResponse)
def list_users(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[UserModel, Depends(get_current_staff_user)],
        pagination: Annotated[PaginationQuery, Depends()],
        ordering: Annotated[UsersOrderingQuery, Depends()],
        filters: UsersFilterQuery = Depends(UsersFilterQuery),
):
    order_by = "first_name"
    users, total, total_active, total_disabled = UsersCRUD.list_users(
        db,
        **pagination.model_dump(),
        **ordering.model_dump(exclude={"order_by"}),
        **filters.model_dump(exclude_unset=True),
        order_by=order_by
    )
    return UsersListResponse(
        users=users,
        total=total,
        total_active=total_active,
        total_disabled=total_disabled,
        **pagination.model_dump(),
    )


@router.get("/{user_id}", response_model=UserModel)
def get(user_id: UUID, db: Session = Depends(get_db)):
    if (user := UsersCRUD.get(db, user_id)) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
