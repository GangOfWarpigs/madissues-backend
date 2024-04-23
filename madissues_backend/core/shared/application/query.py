from abc import ABC, abstractmethod
from typing import Generic, TypeVar

QueryResult = TypeVar("QueryResult")


class Query(ABC, Generic[QueryResult]):
    @abstractmethod
    def query(self) -> QueryResult:
        pass
