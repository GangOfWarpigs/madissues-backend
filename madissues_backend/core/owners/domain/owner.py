from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import Email
from madissues_backend.core.shared.domain.password import Password
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher


class Owner(AggregateRoot):
    email: Email
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    phone_number: str
    password: str = Field(default="", init=False)

    def __init__(self, **data):
        super().__init__(**data)

    def set_password(self, raw_password, hasher: PasswordHasher):
        password = Password(value=raw_password)
        self.password = hasher.hash(password.value)
