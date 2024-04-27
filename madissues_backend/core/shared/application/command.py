import json
from abc import abstractmethod, ABC
from functools import wraps
from typing import Generic, TypeVar, Any, Callable

from pydantic import BaseModel, ValidationError

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.infrastructure.mock_authentication_service import TokenAuthenticationService

CommandRequest = TypeVar("CommandRequest")
CommandResponse = TypeVar("CommandResponse")


class Command(Generic[CommandRequest, CommandResponse]):
    @abstractmethod
    def execute(self, request: CommandRequest) -> Response[CommandResponse]:
        pass


def AuthenticatedOnly(cls):
    original_execute: Callable[[Command[CommandRequest, Response[CommandResponse]], CommandRequest], Response[
        # type: ignore
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


def command_error_handler(func):
    """ Decorator to handle exceptions in command execution methods """
    def wrapper(self: Command[CommandRequest, CommandResponse], request: CommandRequest) -> Response[CommandResponse]:
        try:
            return func(self, request)
        except ValidationError as e:
            field: list[str] = json.loads(e.json())[0]["loc"]
            return Response.field_fail(message='{} must be valid'.format(", ".join(field)), field=field)
        except ValueError as e:
            return Response.fail(message=str(e))
        except Exception as e:
            return Response.fail(code=-1, message="An unexpected error occurred")
    return wrapper


