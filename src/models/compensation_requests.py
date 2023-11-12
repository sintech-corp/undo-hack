from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from models.mixins import BaseDBModel


if TYPE_CHECKING:
    from models.geo import Locality, State
    from models.users import User


class EnergyType(Base, BaseDBModel):
    __tablename__ = "energy_types"

    name: Mapped[str]
    ru_name: Mapped[str]
    en_name: Mapped[str]

    compensation_requests: Mapped[list["CompensationRequest"]] = relationship(back_populates="main_heating_type")


class CompensationRequest(Base, BaseDBModel):
    __tablename__ = "compensation_requests"

    is_anomaly: Mapped[bool] = mapped_column(default=False)
    grade: Mapped[int]
    idnp: Mapped[str | None]

    main_heating_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("energy_types.uid"), nullable=True)
    main_heating_type: Mapped["EnergyType"] = relationship(back_populates="compensation_requests")

    state_id: Mapped[int | None] = mapped_column(ForeignKey("states.id"), nullable=True)
    state: Mapped["State"] = relationship(back_populates="compensation_requests")

    locality_id: Mapped[int | None] = mapped_column(ForeignKey("localities.id"), nullable=True)
    locality: Mapped["Locality"] = relationship(back_populates="compensation_requests")

    street: Mapped[str | None]

    date_of_birth: Mapped[int | None]
    sex: Mapped[int | None]
    average_income: Mapped[int | None]

    provider_name: Mapped[str | None]

    consumption_november: Mapped[int | None]
    consumption_december: Mapped[int | None]
    consumption_january: Mapped[int | None]
    consumption_february: Mapped[int | None]
    consumption_march: Mapped[int | None]

    number_of_residents: Mapped[int | None]
    age: Mapped[int]
    age_range: Mapped[str]
    salary_range: Mapped[str]
    salary_range_encoded: Mapped[int]
    age_range_encoded: Mapped[int]
    locality_encoded: Mapped[int]
    main_heating_type_encoded: Mapped[int]
    company_encoded: Mapped[int]

    grades: Mapped[list["CompensationRequestGrade"]] = relationship(
        back_populates="compensation_request", lazy="joined", order_by="desc(CompensationRequestGrade.created_at)",
    )


class CompensationRequestGrade(Base, BaseDBModel):
    __tablename__ = "compensation_request_grades"

    old_value: Mapped[int | None] = mapped_column(default=None)
    new_value: Mapped[int]
    comment: Mapped[str | None] = mapped_column(default=None)
    auto_set: Mapped[bool] = mapped_column(default=True)

    compensation_request: Mapped["CompensationRequest"] = relationship(back_populates="grades")
    compensation_request_id: Mapped[UUID] = mapped_column(ForeignKey("compensation_requests.uid"))

    author_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.uid"), nullable=True)
    author: Mapped["User"] = relationship(back_populates="grades")
