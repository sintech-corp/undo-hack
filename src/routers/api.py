from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import get_settings
from crud.compensations_requests import CompensationsCRUD
from dependencies.db import get_db
from routers import auth, users, compensation_requests
from schemas.compensation_requests import EnergyTypeModel
from schemas.geo import StateModel, LocalityModel

api_router = APIRouter(prefix=get_settings().api_str)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(compensation_requests.router)


@api_router.get("/energy-types", response_model=list[EnergyTypeModel])
def list_energy_types(db: Session = Depends(get_db)):
    return CompensationsCRUD.list_energy_types(db)


@api_router.get("/regions", response_model=list[StateModel])
def list_regions(db: Session = Depends(get_db)):
    return CompensationsCRUD.list_regions(db)


@api_router.get("/localities", response_model=list[LocalityModel])
def list_localities(db: Session = Depends(get_db)):
    return CompensationsCRUD.list_localities(db)
