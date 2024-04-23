from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import Email
from madissues_backend.core.users.domain.user.password import Password
from madissues_backend.core.users.domain.user.password_hasher import PasswordHasher


class User(AggregateRoot):
    email: Email
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    password: str = Field(default="", init=False)

    def set_password(self, password, hasher: PasswordHasher):
        checked_password = Password(value=password)
        self.password = hasher.hash(checked_password.value)
