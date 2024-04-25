from pydantic import BaseModel

from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, CommandRequest, CommandResponse, \
    command_error_handler
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.response import Response


class SignInOwnerCommandRequest(BaseModel):
    email: str
    password: str


class SignInOwnerCommandResponse(BaseModel):
    token: str


class SignInOwnerCommand(Command[SignInOwnerCommandRequest, SignInOwnerCommandResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OwnerRepository, password_hasher: PasswordHasher):
        self.authentication_service = authentication_service
        self.repository = repository
        self.password_hasher=password_hasher

    @command_error_handler
    def execute(self, request: SignInOwnerCommandRequest) -> Response[SignInOwnerCommandResponse]:
        if not self.repository.exists_owner_with_email(request.email):
            return Response.fail("Owner with this email does not exist")

        owner = self.repository.get_owner_by_email(request.email)

        if self.passwordsDoesNotMatch(request.password, owner.password):
            return Response.fail("Invalid password")

        return Response.success(SignInOwnerCommandResponse(
            token=owner.token
        ))

    def passwordsDoesNotMatch(self, password, password1):
        return self.password_hasher.hash(password) != password1

