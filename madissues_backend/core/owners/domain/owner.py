from typing import Annotated
from pydantic import Field
from madissues_backend.core.owners.domain.owner_email_updated import OwnerEmailUpdatedPayload, OwnerEmailUpdated
from madissues_backend.core.owners.domain.owner_task_manager import OwnerTaskManager
from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.task_manager import TaskManager
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.domain.value_objects import Email, GenericUUID
from madissues_backend.core.shared.domain.password import Password
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher


class Owner(AggregateRoot[GenericUUID]):
    email: Email
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    phone_number: str = Field(min_length=1, pattern=r'^(\+\d{1,3})?(\d{9,15})$')
    password: str = Field(default="",
                          init=False)
    token: str = Field(default="", init=False)
    task_manager: OwnerTaskManager | None = Field(init=False, default=None)

    def __init__(self, **data):
        super().__init__(**data)

    def set_password(self, raw_password, hasher: PasswordHasher):
        password_validator = Password(password_value=raw_password)
        self.password = hasher.hash(password_validator.password_value)

    def generate_auth_token(self, token_generator: TokenGenerator):
        self.token = token_generator.generate()

    def change_email(self, email: Email):
        self.validate_field("email", email)
        self.email = email
        self.register_event(
            OwnerEmailUpdated(payload=OwnerEmailUpdatedPayload(user_id=str(self.id), email=email))
        )

    def integrate_task_manager(self, task_manager : str, api_token):
        self.task_manager = OwnerTaskManager(
            task_manager_name=task_manager,
            token=api_token
        )
