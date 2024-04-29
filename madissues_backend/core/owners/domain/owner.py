from typing import Annotated

from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.domain.value_objects import Email, GenericUUID
from madissues_backend.core.shared.domain.password import Password
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher


class Owner(AggregateRoot[GenericUUID]):
    email: Email
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    phone_number: str = Field(min_length=1, pattern=r'^(\+\d{1,3})?(\d{9,15})$')
    password: str = Field(default="", init=False)  # Minimo 8 caracteres, mayusculas obligatorias, caracter especial, un numero mínimo
    token: str = Field(default="", init=False)

    def __init__(self, **data):
        super().__init__(**data)

    def set_password(self, raw_password, hasher: PasswordHasher):
        password_validator = Password(password_value=raw_password)
        self.password = hasher.hash(password_validator.password_value)

    def generate_auth_token(self, token_generator: TokenGenerator):
        self.token = token_generator.generate()
