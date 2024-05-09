from abc import ABC, abstractmethod
from typing import Generic, TypeVar

QueryResult = TypeVar("QueryResult")
QueryParams = TypeVar("QueryParams")


class Query(ABC, Generic[QueryParams, QueryResult]):
    @abstractmethod
    def execute(self, params: QueryParams | None = None) -> QueryResult:
        pass
