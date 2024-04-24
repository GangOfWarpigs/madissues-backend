from datetime import datetime
from typing import Annotated
from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import Email, GenericUUID
from madissues_backend.core.shared.domain.password import Password
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.students.domain.student_preferences import StudentPreferences
from madissues_backend.core.students.domain.student_profile import StudentProfile


class Student(AggregateRoot[GenericUUID]):
    organization: GenericUUID
    email: Email
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    password: str = Field(default="", init=False)
    started_studies_date: datetime
    is_site_admin: bool
    is_council_member: bool
    is_banned: bool
    token: str
    profile: StudentProfile
    preferences: StudentPreferences

    def __init__(self, **data):
        super().__init__(**data)

    def set_password(self, raw_password, hasher: PasswordHasher):
        password = Password(value=raw_password)
        self.password = hasher.hash(password.value)
