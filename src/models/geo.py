from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models.compensation_requests import CompensationRequest


class State(Base):
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    ru_name: Mapped[str | None]

    cities: Mapped[list["City"]] = relationship(back_populates="state")
    compensation_requests: Mapped[list["CompensationRequest"]] = relationship(back_populates="state")


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    ru_name: Mapped[str | None]

    state_id: Mapped[int] = mapped_column(ForeignKey("states.id"))
    state: Mapped["State"] = relationship(back_populates="cities")

    localities: Mapped[list["Locality"]] = relationship(back_populates="city")


class Locality(Base):
    __tablename__ = "localities"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    ru_name: Mapped[str | None]

    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship(back_populates="localities")

    compensation_requests: Mapped[list["CompensationRequest"]] = relationship(back_populates="locality")
