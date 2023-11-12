import random
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ai.engine import return_prediction
from crud.compensations_requests import CompensationsCRUD
from dependencies.auth import get_current_staff_user
from dependencies.db import get_db
from schemas.queries import PaginationQuery
from schemas.compensation_requests import CompensationRequestBase, CompensationRequestModel, CompensationsListResponse, \
    CompensationsFilterQuery, CompensationsOrderingQuery, EnergyTypeModel, CompensationRequestModelWithGrades, \
    CompensationRequestGradeBase, ValidateCompensationResponse, ChangeRequestGradeItem
from schemas.users import UserModel

router = APIRouter(
    prefix="/compensation-requests",
    tags=["compensation requests"],
)


@router.get("/", response_model=CompensationsListResponse)
def list_compensation_requests(
        db: Annotated[Session, Depends(get_db)],
        # user: Annotated[UserModel, Depends(get_current_staff_user)],
        pagination: Annotated[PaginationQuery, Depends()],
        ordering: Annotated[CompensationsOrderingQuery, Depends()],
        filters: CompensationsFilterQuery = Depends(CompensationsFilterQuery),
):
    compensations, total, total_ok, total_anomalies = CompensationsCRUD.list_compensation_requests(
        db,
        **pagination.model_dump(),
        **ordering.model_dump(),
        **filters.model_dump(exclude_unset=True),
    )
    return CompensationsListResponse(
        compensations=compensations,
        total=total,
        total_ok=total_ok,
        total_anomalies=total_anomalies,
        **pagination.model_dump(),
    )


@router.get("/{request_id}", response_model=CompensationRequestModelWithGrades)
def get(request_id: UUID, db: Session = Depends(get_db)):
    if (compensation := CompensationsCRUD.get(db, request_id)) is None:
        raise HTTPException(status_code=404, detail="Compensation not found")
    return compensation


@router.post("/{request_id}/validate-grade", response_model=ValidateCompensationResponse)
def change_request_grade(
    request_id: UUID,
    new_value: ChangeRequestGradeItem,
    user: Annotated[UserModel, Depends(get_current_staff_user)],
    db: Session = Depends(get_db),
) -> ValidateCompensationResponse:
    if (db_compensation_request := CompensationsCRUD.get(db, request_id)) is None:
        raise HTTPException(status_code=404, detail="Compensation request not found")
    # Pass all values from DB to model
    result = return_prediction('svm_model.pkl', db_compensation_request, new_value.new_value)
    if new_value.new_value == db_compensation_request.grade:
        is_valid = True
    else:
        is_valid = False
    return ValidateCompensationResponse(is_valid=is_valid)


@router.post("/{request_id}/change-grade", response_model=CompensationRequestModelWithGrades)
def change_request_grade(
    request_id: UUID,
    compensation_request_grade: CompensationRequestGradeBase,
    user: Annotated[UserModel, Depends(get_current_staff_user)],
    db: Session = Depends(get_db),
):
    if (db_compensation_request := CompensationsCRUD.get(db, request_id)) is None:
        raise HTTPException(status_code=404, detail="Compensation request not found")
    return CompensationsCRUD.change_grade(
        db,
        db_compensation_request=db_compensation_request,
        author_id=user.uid,
        new_value=compensation_request_grade.new_value,
        comment=compensation_request_grade.comment,
    )
