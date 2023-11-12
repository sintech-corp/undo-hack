import typer

from models.fixtures.load_energy_type import load_energy_types
from models.fixtures.load_users import load_users
from models.fixtures.load_geo import load_geo


def loaddata():
    load_users()
    load_geo()
    load_energy_types()


if __name__ == "__main__":
    typer.run(loaddata)
