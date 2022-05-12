from typing import TypeVar, Generic

from fastapi import Query

from fastapi_pagination.default import Page as BasePage, Params as BaseParams

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(10, ge=1, le=100, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
