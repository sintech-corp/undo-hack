from uuid import UUID

import typer

from dependencies.db import get_db
from models import EnergyType

energy_types = [
    {
        "uid": UUID('2df4b99c-2ddf-403a-bd2f-fcf3c5fc64a3'),
        "name": "Incalzire centralizata",
        "ru_name": "Центральное отопление",
        "en_name": "Central heating",
    },
    {
        "uid": UUID('14e19c53-4ec0-47c4-b42f-0d6aca39377b'),
        "name": "Electricitate",
        "ru_name": "Электричество",
        "en_name": "Electricity",
    },
{
        "uid": UUID('3c5e8fde-67b6-43bc-b610-38c3ecd4c548'),
        "name": "Gaze naturale",
        "ru_name": "Природный газ",
        "en_name": "Natural gas",
    },
{
        "uid": UUID('e169c5f5-3d2e-4ee0-b8fa-edf9137afb91'),
        "name": "Combustibil solid",
        "ru_name": "Твёрдое топливо",
        "en_name": "Solid fuel stove",
    },
]


def load_energy_types():
    db_session = next(get_db())
    existing_energy_types = db_session.query(EnergyType).filter(EnergyType.uid.in_([energy_type["uid"] for energy_type in energy_types])).all()
    existing_energy_types_uids = [str(existing_energy_type.uid) for existing_energy_type in existing_energy_types]
    for energy_type in energy_types:
        db_energy_type = EnergyType(**energy_type)
        if str(energy_type["uid"]) in existing_energy_types_uids:
            db_session.merge(db_energy_type)
        else:
            db_session.add(db_energy_type)

    db_session.commit()


if __name__ == "__main__":
    typer.run(load_energy_types)

