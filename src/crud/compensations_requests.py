from datetime import datetime
from typing import Type
from uuid import UUID

from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import Session

from annotations import OrderLiteral
from models import CompensationRequest, EnergyType, CompensationRequestGrade, State, Locality
from schemas.compensation_requests import CompensationRequestBase

TCompensationRequest = Type[CompensationRequest]
TEnergyType = Type[EnergyType]
TState = Type[State]
TLocality = Type[Locality]


class CompensationsCRUD:
    @classmethod
    def get(cls, db: Session, uid: UUID) -> CompensationRequest | None:
        return db.query(CompensationRequest).filter(CompensationRequest.uid == uid).first()

    @classmethod
    def list_energy_types(cls, db: Session) -> list[TEnergyType]:
        return db.query(EnergyType).all()


    @classmethod
    def get_by_idnp(cls, db: Session, idnp: str) -> CompensationRequest | None:
        return db.query(CompensationRequest).filter(CompensationRequest.idnp == idnp).first()

    @classmethod
    def list_compensation_requests(
            cls,
            db: Session,
            limit: int,
            offset: int,
            order: OrderLiteral,
            order_by: str,
            energy_types: list[str],
            is_anomaly: bool | None = None,
            search: str | None = None,
    ) -> tuple[list[TCompensationRequest], int, int, int]:
        direction = desc if order == 'desc' else asc
        query = db.query(CompensationRequest)
        total: int = query.count()
        total_ok: int = query.filter(CompensationRequest.is_anomaly.is_(False)).count()
        total_anomalies: int = query.filter(CompensationRequest.is_anomaly.is_(True)).count()

        if is_anomaly is not None:
            query = query.filter(CompensationRequest.is_anomaly.is_(is_anomaly))

        if search:
            query = query.filter(or_(
                CompensationRequest.idnp.ilike(f"%{search}%"),
                CompensationRequest.street.ilike(f"%{search}%"),
            ))

        if energy_types:
            query = query.filter(CompensationRequest.main_heating_type.has(EnergyType.uid.in_(energy_types)))

        compensations = query.order_by(
            direction(getattr(CompensationRequest, order_by))
        ).offset(offset).limit(limit).all()
        return compensations, total, total_ok, total_anomalies

    @classmethod
    def change_grade(
            cls,
            db: Session,
            db_compensation_request: CompensationRequest,
            author_id: UUID,
            new_value: int,
            comment: str | None = None
    ) -> CompensationRequest:
        db_compensation_request_grade = CompensationRequestGrade(
            compensation_request_id=db_compensation_request.uid,
            author_id=author_id,
            old_value=db_compensation_request.grade,
            new_value=new_value,
            comment=comment,
            auto_set=False,
        )
        db_compensation_request.grade = new_value
        db.add(db_compensation_request_grade)
        db.add(db_compensation_request)
        db.commit()
        db.refresh(db_compensation_request)
        return db_compensation_request

    @classmethod
    def list_regions(
            cls,
            db: Session,
    ) -> list[TState]:
        return db.query(State).all()

    @classmethod
    def list_localities(
            cls,
            db: Session,
    ) -> list[TLocality]:
        return db.query(Locality).all()
