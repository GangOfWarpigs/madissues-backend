from operator import gt
from typing import Annotated
from pydantic import AfterValidator, BaseModel, field_validator

from madissues_backend.core.shared.domain.value_objects import ValueObject


class Password(ValueObject):
    password_value: str

    @field_validator('password_value', mode='before')
    @classmethod
    def is_secure_password(cls, password: str) -> str:
        min_length = 8
        requires_digit = True
        requires_uppercase = True
        requires_lowercase = True
        requires_special_char = True
        assert len(password) >= min_length, "Password must be at least 8 characters long."
        assert any(
            char.isdigit() for char in password) or not requires_digit, "Password must contain at least one digit."
        assert any(char.isupper() for char in
                   password) or not requires_uppercase, "Password must contain at least one uppercase letter."
        assert any(char.islower() for char in
                   password) or not requires_lowercase, "Password must contain at least one lowercase letter."
        assert any(char in "!@#$%^&*()-_+=<>?/|" for char in
                   password) or not requires_special_char, "Password must contain at least one special character."
        return password
