from pydantic import BaseModel

from madissues_backend.core.shared.application.command import Command


class SignInOwnerCommandRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str


class SignInOwnerCommandResponse(BaseModel):
    ...


class SignInOwnerCommand(Command):
    ...
