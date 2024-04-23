from fastapi import FastAPI

from madissues_backend.core.shared.infrastructure.in_memory_event_bus import InMemoryEventBus
from madissues_backend.core.users.application.commands.sign_up_student_command import SignUpStudentCommand
from madissues_backend.core.users.infrastructure.mocks.in_memory_user_repository import InMemoryUserRepository
from madissues_backend.core.users.infrastructure.mocks.mock_password_hasher import MockPasswordHasher

app = FastAPI()

user_repository = InMemoryUserRepository()
event_bus = InMemoryEventBus()
password_hasher = MockPasswordHasher()

@app.post("/user/register")
def register_user(data):
    return SignUpStudentCommand(user_repository, event_bus, password_hasher).execute(data)
