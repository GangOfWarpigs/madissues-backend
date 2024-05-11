import json
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import ValidationError

from madissues_backend.core.shared.application.command import CommandRequest, CommandResponse
from madissues_backend.core.shared.domain.response import Response

QueryResult = TypeVar("QueryResult")
QueryParams = TypeVar("QueryParams")


class Query(ABC, Generic[QueryParams, QueryResult]):
    @abstractmethod
    def execute(self, params: QueryParams | None = None) -> Response[QueryResult]:
        pass

    def run(self, params: QueryParams | None = None) -> Response[QueryResult]:
        try:
            return self.execute(params)
        except ValidationError as e:
            field: list[str] = json.loads(e.json())[0]["loc"]
            return Response.field_fail(message='{} must be valid'.format(", ".join(field)), field=field)
        except ValueError as e:
            return Response.fail(message=str(e))
        except Exception as e:
            return Response.fail(code=-1, message=str(e))
