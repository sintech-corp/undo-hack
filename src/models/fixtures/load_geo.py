import json

import typer
from sqlalchemy.orm import Session

from config import get_settings
from dependencies.db import get_db
from models.geo import State, City, Locality


def load_states(db_session: Session, states_file: str):
    with open(states_file, 'rb') as f_obj:
        states = json.load(f_obj)
        db_states = []
        db_cities = []
        db_localities = []
        existing_states_ids = {state.id for state in db_session.query(State).all()}
        existing_cities_ids = {state.id for state in db_session.query(City).all()}
        existing_localities_ids = {state.id for state in db_session.query(Locality).all()}
        for state in states:
            if state["id"] not in existing_states_ids:
                db_states.append(
                    State(
                        id=state["id"],
                        name=state["name"],
                        ru_name=state.get('ru_name') or state["name"],
                    )
                )
            for city in state.get('cities', []):
                if city["id"] not in existing_cities_ids:
                    db_cities.append(
                        City(
                            id=city["id"],
                            name=city["name"],
                            ru_name=city.get('ru_name') or city["name"],
                            state_id=state["id"],
                        )
                    )
                for locality in city.get('localities', []):
                    if locality["id"] not in existing_localities_ids:
                        db_localities.append(
                            Locality(
                                id=locality["id"],
                                name=locality["name"],
                                ru_name=locality.get('ru_name') or locality["name"],
                                city_id=city["id"],
                            )
                        )
        db_session.bulk_save_objects(db_states)
        db_session.bulk_save_objects(db_cities)
        db_session.bulk_save_objects(db_localities)
        db_session.commit()


def load_geo():
    db_session = next(get_db())
    load_states(db_session, 'src/models/fixtures/states_and_cities.json')


if __name__ == "__main__":
    get_settings()
    typer.run(load_geo)
