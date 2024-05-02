from datetime import datetime
from typing import Annotated
from pydantic import Field

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.domain.value_objects import Email, GenericUUID
from madissues_backend.core.shared.domain.password import Password
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.students.domain.events.student_banned import StudentBannedPayload, StudentBanned
from madissues_backend.core.students.domain.events.student_email_updated import StudentEmailUpdated, \
    StudentEmailUpdatedPayload
from madissues_backend.core.students.domain.events.student_personal_data_updated import \
    StudentPersonalDataUpdatedPayload, StudentPersonalDataUpdated
from madissues_backend.core.students.domain.events.student_preferences_updated import StudentPreferencesUpdated, \
    StudentPreferencesUpdatedPayload
from madissues_backend.core.students.domain.events.student_profile_updated import StudentProfileUpdated, \
    StudentProfileUpdatedPayload
from madissues_backend.core.students.domain.events.student_role_changed import StudentRoleChanged, \
    StudentRoleChangedPayload
from madissues_backend.core.students.domain.student_preferences import StudentPreferences
from madissues_backend.core.students.domain.student_profile import StudentProfile


class Student(AggregateRoot[GenericUUID]):
    organization_id: GenericUUID
    email: Email
    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    password: str = Field(default="", init=False)
    started_studies_date: datetime
    is_site_admin: bool
    is_council_member: bool
    is_banned: bool
    token: str = Field(default="", init=False)
    profile: StudentProfile
    preferences: StudentPreferences

    def __init__(self, **data):
        super().__init__(**data)

    def set_password(self, raw_password: str, hasher: PasswordHasher):
        new_password = Password(password_value=raw_password)
        self.password = hasher.hash(new_password.password_value)

    def generate_auth_token(self, token_generator: TokenGenerator):
        self.token = token_generator.generate()

    def check_password(self, raw_password: str, hasher: PasswordHasher) -> bool:
        return hasher.hash(raw_password) == self.password

    def change_email(self, email: Email):
        self.validate_field("email", email)
        self.email = email
        self.register_event(
            StudentEmailUpdated(payload=StudentEmailUpdatedPayload(user_id=str(self.id), email=email))
        )

    def change_role(self, make_admin: bool = False, make_council_member: bool = False):
        self.is_site_admin = make_admin
        self.is_council_member = make_council_member
        self.register_event(
            StudentRoleChanged(payload=StudentRoleChangedPayload(user_id=str(self.id),
                                                                 admin=make_admin,
                                                                 council_member=make_council_member))
        )

    def ban(self):
        self.is_banned = True
        self.register_event(
            StudentBanned(payload=StudentBannedPayload(user_id=str(self.id)))
        )

    def change_preferences(self, preferences: StudentPreferences):
        self.preferences = preferences
        self.register_event(
            StudentPreferencesUpdated(
                payload=StudentPreferencesUpdatedPayload(user_id=str(self.id),
                                                         language=preferences.language,
                                                         theme=preferences.theme))
        )

    def update_personal_data(self, first_name: str, last_name: str, email: str, started_studies_date: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.started_studies_date = datetime.strptime(started_studies_date, "%Y-%m-%d")

        self.register_event(
            StudentPersonalDataUpdated(
                payload=StudentPersonalDataUpdatedPayload(user_id=str(self.id),
                                                          first_name=first_name,
                                                          last_name=last_name,
                                                          email=email,
                                                          started_studies_date=started_studies_date))
        )

    def update_profile(self, degree: str, joined_courses: list[str]):
        self.profile.degree = GenericUUID(degree)
        self.profile.joined_courses = [GenericUUID(joined_course) for joined_course in joined_courses]
        self.register_event(
            StudentProfileUpdated(
                payload=StudentProfileUpdatedPayload(user_id=str(self.id),
                                                     degree=degree,
                                                     joined_courses=joined_courses))
        )
