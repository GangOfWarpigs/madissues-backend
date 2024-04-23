from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import Email
from madissues_backend.core.users.domain.user.created_user_event import CreatedUserDomainEvent, Payload
from madissues_backend.core.users.domain.user.password import Password
from madissues_backend.core.users.domain.user.password_hasher import PasswordHasher


class User(AggregateRoot):
    email: Email
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    password: str = Field(default="", init=False)

    def __init__(self, **data):
        super().__init__(**data)
        self.register_event(CreatedUserDomainEvent(
            Payload(
                user_id=data.id,
                email=data.email
            )
        ))

    def set_password(self, raw_password, hasher: PasswordHasher):
        password = Password(value=raw_password)
        self.password = hasher.hash(password.value)
