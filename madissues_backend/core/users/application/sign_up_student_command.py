from pydantic import BaseModel
from madissues_backend.core.shared.application.command import Command
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import Email
from madissues_backend.core.users.domain.user import User
from madissues_backend.core.users.application.user_repository import UserRepository

class SignUpStudentRequest(BaseModel):
    first_name : str
    last_name : str
    email : str
    raw_password : str

class SignUpStudentResponse(BaseModel):
    message : str

class SignUpStudentCommand(Command[SignUpStudentRequest, SignUpStudentResponse]):
    def __init__(self, user_repository : UserRepository, event_bus : EventBus) -> None:
        self.user_repository = user_repository
        self.event_bus = event_bus

    def execute(self, request: SignUpStudentRequest) -> Response[SignUpStudentResponse]:
        try:
            user = User(
                id="",
                email = Email(request.email),
                first_name=request.first_name,
                last_name=request.last_name,
                password=request.raw_password
            )
            self.user_repository.save(user)
            self.event_bus.notify_all(user.collect_events())
            return Response.ok(SignUpStudentResponse(
                message="User created correctly"
            ))
        except ValueError as e:
            return Response.fail(message=str(e))