from schemas.base import CamelModel, ORMModel


class StateModel(CamelModel, ORMModel):
    id: int
    name: str
    ru_name: str


class CityModel(CamelModel, ORMModel):
    id: int
    name: str
    ru_name: str


class LocalityModel(CamelModel, ORMModel):
    id: int
    name: str
    ru_name: str
