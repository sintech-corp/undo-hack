from typing import Literal
from uuid import UUID

from fastapi import Query
from pydantic import Field

from schemas.base import CamelModel, ORMModel, UpdatedAtSchema, CreatedAtSchema, UidSchema
from schemas.geo import StateModel, CityModel, LocalityModel
from schemas.queries import OrderQuery, PaginationResponse
from schemas.users import UserModel


class EnergyTypeModel(UidSchema, CamelModel, ORMModel):
    name: str
    ru_name: str
    en_name: str


class CompensationRequestBase(CamelModel):
    idnp: str
    grade: int

    main_heating_type: UUID | None = None

    state: int
    city: int
    locality: int

    street: str

    date_of_birth: int
    sex: int
    average_income: int

    provider_name: str

    consumption_november: int
    consumption_december: int
    consumption_january: int
    consumption_february: int
    consumption_march: int
    is_anomaly: bool


class CompensationRequestModel(CompensationRequestBase, ORMModel, UpdatedAtSchema, CreatedAtSchema, UidSchema):
    idnp: str | None = None
    grade: int

    street: str | None = None

    date_of_birth: int | None = None
    sex: int | None = None
    average_income: int | None = None

    provider_name: str | None = None

    consumption_november: int | None = None
    consumption_december: int | None = None
    consumption_january: int | None = None
    consumption_february: int | None = None
    consumption_march: int | None = None

    main_heating_type: EnergyTypeModel | None = None

    state: StateModel | None = None
    city: CityModel | None = None
    locality: LocalityModel | None = None
    is_anomaly: bool


class CompensationRequestGradeBase(CamelModel):
    new_value: int
    comment: str | None = None


class CompensationRequestGradeModel(CompensationRequestGradeBase, ORMModel, UpdatedAtSchema, CreatedAtSchema, UidSchema):
    old_value: int | None = None
    author: UserModel | None = None
    auto_set: bool


class CompensationRequestModelWithGrades(CompensationRequestModel):
    grades: list[CompensationRequestGradeModel]


class CompensationsListResponse(PaginationResponse):
    compensations: list[CompensationRequestModel]
    total_ok: int
    total_anomalies: int


class CompensationsOrderingQuery(OrderQuery, CamelModel):
    order_by: str = 'grade'


class CompensationsFilterQuery(CamelModel):
    is_anomaly: bool | None = None
    search: str | None = None
    energy_types: list[str] = Field(Query([]))


class ValidateCompensationResponse(CamelModel):
    is_valid: bool


class ChangeRequestGradeItem(CamelModel):
    new_value: int
