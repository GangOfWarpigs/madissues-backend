from abc import abstractmethod, ABC
from functools import wraps
from typing import Generic, TypeVar, Any, Callable

from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.infrastructure.token_authentication_service import TokenAuthenticationService

CommandRequest = TypeVar("CommandRequest")
CommandResponse = TypeVar("CommandResponse")


class Command(Generic[CommandRequest, CommandResponse]):
    @abstractmethod
    def execute(self, request: CommandRequest) -> Response[CommandResponse]:
        pass


def AuthenticatedOnly(cls):
    original_execute: Callable[[Command[CommandRequest, Response[CommandResponse]], CommandRequest], Response[
        CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_authenticated():
            return Response.fail("User must be authenticated")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def StudentsOnly(cls):
    original_execute: Callable[[Command[CommandRequest, Response[CommandResponse]], CommandRequest], Response[
        CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_student():
            return Response.fail("User must be a student")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def OwnersOnly(cls):
    original_execute: Callable[[Command[CommandRequest, Response[CommandResponse]], CommandRequest], Response[
        CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_owner():
            return Response.fail("User must be a owner")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def SiteAdminsOnly(cls):
    original_execute: Callable[[Command[CommandRequest, Response[CommandResponse]], CommandRequest], Response[
        CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_site_admin():
            return Response.fail("User must be a site admin")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def CouncilMembersOnly(cls):
    original_execute: Callable[[Command[CommandRequest, Response[CommandResponse]], CommandRequest], Response[
        CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_council_member():
            return Response.fail("User must be a council member")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls
