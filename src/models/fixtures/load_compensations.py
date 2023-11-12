import csv
from functools import lru_cache

import typer
from sqlalchemy.orm import Session

from config import get_settings
from dependencies.db import get_db
from models import CompensationRequest, EnergyType
from models.compensation_requests import CompensationRequestGrade
from models.geo import State, City, Locality


def my_str(db: Session, value: str) -> str:
    return str(value)


def none_or_int(db: Session, value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def zero_or_int(db: Session, value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


@lru_cache(maxsize=50)
def load_state(db: Session, value: str) -> State | None:
    return db.query(State).filter(State.name == value).first()


@lru_cache(maxsize=1000)
def load_locality(db: Session, value: str) -> Locality | None:
    return db.query(Locality).filter(Locality.name == value).first()


@lru_cache(maxsize=10)
def load_energy_type_by_ro_name(db: Session, value: str) -> EnergyType | None:
    return db.query(EnergyType).filter(EnergyType.name == value).first()


def outliner_to_boolean(db: Session, value: str) -> bool:
    if value == "-1":
        return True
    return False


CSV_FIELD_MAPPING = {
    # "Id": "uid",
    "Grad": "grade",
    "Raion": "state",
    "Localitate": "locality",
    "Strada": "street",
    "Tip incalzire principal": "main_heating_type",
    "DateOfBirth": "date_of_birth",
    "Sex": "sex",
    "AverageIncome": "average_income",
    "Name": "provider_name",
    # "Consum volum 11.2022": "consumption_november",
    # "Consum volum 12.2022": "consumption_december",
    # "Consum volum 01.2023": "consumption_january",
    # "Consum volum 02.2023": "consumption_february",
    # "Consum volum 03.2023": "consumption_march",
    "IsOutlier": "is_anomaly",
    "NrMembriDeFamilie": "number_of_residents",
    "Age": "age",
    "AgeRange": "age_range",
    "SalaryRange": "salary_range",
    "SalaryRange_encoded": "salary_range_encoded",
    "AgeRange_encoded": "age_range_encoded",
    "Localitate_encoded": "locality_encoded",
    "Tip_incalzire_principal_encoded": "main_heating_type_encoded",
    "Company_name_encoded": "company_encoded",
}

CONVERTERS_MAPPING = {
    # "uid": my_str,
    "grade": zero_or_int,
    "state": load_state,
    "locality": load_locality,
    "street": my_str,
    "main_heating_type": load_energy_type_by_ro_name,
    "date_of_birth": none_or_int,
    "sex": zero_or_int,
    "average_income": zero_or_int,
    "provider_name": my_str,
    # "consumption_november": zero_or_int,
    # "consumption_december": zero_or_int,
    # "consumption_january": zero_or_int,
    # "consumption_february": zero_or_int,
    # "consumption_march": zero_or_int,
    "is_anomaly": outliner_to_boolean,
    "number_of_residents": zero_or_int,
    "age": zero_or_int,
    "age_range": my_str,
    "salary_range": my_str,
    "salary_range_encoded": zero_or_int,
    "age_range_encoded": my_str,
    "locality_encoded": zero_or_int,
    "main_heating_type_encoded": zero_or_int,
    "company_encoded": zero_or_int,
}


def load_compensations():
    db_session = next(get_db())
    db_session.query(CompensationRequestGrade).delete()
    db_session.query(CompensationRequest).delete()

    db_compensations = []

    # load data from CSV
    with open('src/models/fixtures/New_data.csv') as csv_obj:
        csv_reader = csv.DictReader(csv_obj)

        for idx, row in enumerate(csv_reader):
            if idx and idx % 10000 == 0:
                print(f"{idx}")
            data = {}
            for csv_field, db_field in CSV_FIELD_MAPPING.items():
                value = row[csv_field]
                data[db_field] = CONVERTERS_MAPPING[db_field](db_session, value)
            db_compensation = CompensationRequest(**data)
            if db_compensation.main_heating_type:
                db_compensation.main_heating_type_id = db_compensation.main_heating_type.uid
            if db_compensation.state:
                db_compensation.state_id = db_compensation.state.id
            if db_compensation.locality:
                db_compensation.locality_id = db_compensation.locality.id

            db_compensations.append(db_compensation)

    db_session.bulk_save_objects(db_compensations)
    db_session.commit()
    load_compensations_grades()


def load_compensations_grades():
    db_session = next(get_db())
    db_session.query(CompensationRequestGrade).delete()

    db_compensations_grades = []

    for db_compensation in db_session.query(CompensationRequest).all():
        db_compensations_grades.append(
            CompensationRequestGrade(
                new_value=db_compensation.grade,
                compensation_request_id=db_compensation.uid,
            )
        )
    db_session.bulk_save_objects(db_compensations_grades)
    db_session.commit()


if __name__ == "__main__":
    get_settings()
    typer.run(load_compensations)
