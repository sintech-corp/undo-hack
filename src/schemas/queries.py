from typing import Literal

from fastapi import Query

from annotations import OrderLiteral
from schemas.base import CamelModel


class PaginationQuery(CamelModel):
    offset: int = Query(0, title="Starting point", ge=0)
    limit: int = Query(20, title="Records per request", ge=1, le=50)


class PaginationResponse(CamelModel):
    offset: int
    limit: int
    total: int


class OrderQuery(CamelModel):
    order: OrderLiteral = 'asc'
