from pydantic import BaseModel
from madissues_backend.core.shared.application.command import Command
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import Email, GenericUUID
from madissues_backend.core.users.domain.user.password_hasher import PasswordHasher
from madissues_backend.core.users.domain.user import User
from madissues_backend.core.users.application.ports.user_repository import UserRepository


class SignUpStudentRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    raw_password: str


class SignUpStudentResponse(BaseModel):
    message: str


class SignUpStudentCommand(Command[SignUpStudentRequest, SignUpStudentResponse]):
    def __init__(self, user_repository: UserRepository, event_bus: EventBus, password_hasher: PasswordHasher) -> None:
        self.user_repository = user_repository
        self.event_bus = event_bus
        self.password_hasher = password_hasher

    def execute(self, request: SignUpStudentRequest) -> Response[SignUpStudentResponse]:
        try:
            if self.user_repository.exists_user_with_email(request.email):
                raise ValueError("User with this email already exists")
            user = User(
                id=GenericUUID.next_id(),
                email=Email(request.email),
                first_name=request.first_name,
                last_name=request.last_name,
            )
            user.set_password(request.raw_password, self.password_hasher)
            self.user_repository.save(user)
            self.event_bus.notify_all(user.collect_events())
            return Response.ok(SignUpStudentResponse(
                message="User created correctly"
            ))
        except ValueError as e:
            return Response.fail(message=str(e))
