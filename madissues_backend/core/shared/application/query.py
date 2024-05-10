from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from madissues_backend.core.shared.domain.response import Response

QueryResult = TypeVar("QueryResult")
QueryParams = TypeVar("QueryParams")


class Query(ABC, Generic[QueryParams, QueryResult]):
    @abstractmethod
    def execute(self, params: QueryParams | None = None) -> Response[QueryResult]:
        pass
