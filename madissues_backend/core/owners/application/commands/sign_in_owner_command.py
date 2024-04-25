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
    def __init__(self, authentication_service: AuthenticationService, repository: OwnerRepository,
                 password_hasher: PasswordHasher):
        self.authentication_service = authentication_service
        self.repository = repository
        self.password_hasher = password_hasher

    @command_error_handler
    def execute(self, request: SignInOwnerCommandRequest) -> Response[SignInOwnerCommandResponse]:
        owner = self.repository.get_owner_by_email(request.email)

        if owner is None:
            return Response.fail(code=1, message="Owner does not exists")

        if self.passwordsDoesNotMatch(request.password, owner.password):
            return Response.fail(code=2, message="Invalid password")

        return Response.ok(SignInOwnerCommandResponse(
            token=owner.token
        ))

    def passwordsDoesNotMatch(self, password, real_password):
        return self.password_hasher.hash(password) != real_password
