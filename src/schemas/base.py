from datetime import datetime
from uuid import UUID

from humps.camel import case
from pydantic import BaseModel, ConfigDict


def to_camel(value: str) -> str:
    return case(value)


class CamelModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UidSchema(CamelModel):
    uid: UUID


class OptionalUidSchema(CamelModel):
    uid: UUID | None = None


class CreatedAtSchema(CamelModel):
    created_at: datetime


class UpdatedAtSchema(CamelModel):
    updated_at: datetime

