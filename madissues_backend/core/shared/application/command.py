
from abc import abstractmethod
from typing import Generic, TypeVar
from madissues_backend.core.shared.domain.response import Response

CommandRequest = TypeVar("CommandRequest")
CommandResponse = TypeVar("CommandResponse")

class Command(Generic[CommandRequest, CommandResponse]):
    @abstractmethod
    def execute(request : CommandRequest) -> Response[CommandResponse]:
        pass