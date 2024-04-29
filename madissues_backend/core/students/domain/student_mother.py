import random
from datetime import datetime, timedelta
from uuid import uuid4
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.mocks.mock_password_hasher import MockPasswordHasher

from madissues_backend.core.students.domain.student import Student
from madissues_backend.core.students.domain.student_preferences import StudentPreferences
from madissues_backend.core.students.domain.student_profile import StudentProfile


class StudentMother:
    @staticmethod
    def random_email() -> str:
        domains = ["example.com", "test.com", "demo.com"]
        return f"user{random.randint(1, 10000)}@{random.choice(domains)}"

    @staticmethod
    def random_name() -> str:
        names = ["John", "Jane", "Alex", "Maria", "Steve", "Laura"]
        return random.choice(names)

    @staticmethod
    def random_password() -> str:
        # Very simple password generator, for more complex passwords consider using a proper method
        return f"Passw0rd{random.randint(1000, 9999)}!"

    @staticmethod
    def random_theme() -> str:
        return random.choice(["Dark", "Light"])

    @staticmethod
    def random_language() -> str:
        languages = ["en", "es", "fr", "de"]
        return random.choice(languages)

    @staticmethod
    def random_generic_uuid() -> GenericUUID:
        return GenericUUID(str(uuid4()))

    @staticmethod
    def random_profile() -> StudentProfile:
        return StudentProfile(
            id=StudentMother.random_generic_uuid(),
            degree=StudentMother.random_generic_uuid(),
            joined_courses=[StudentMother.random_generic_uuid() for _ in range(random.randint(1, 5))]
        )

    @staticmethod
    def random_preferences() -> StudentPreferences:
        return StudentPreferences(
            id=StudentMother.random_generic_uuid(),
            theme=StudentMother.random_theme(),
            language=StudentMother.random_language()
        )

    @staticmethod
    def random_student() -> Student:
        hasher = MockPasswordHasher()
        raw_password = StudentMother.random_password()
        student = Student(
            id=StudentMother.random_generic_uuid(),
            organization_id=StudentMother.random_generic_uuid(),
            email=StudentMother.random_email(),
            first_name=StudentMother.random_name(),
            last_name=StudentMother.random_name(),
            started_studies_date=datetime.now() - timedelta(days=random.randint(0, 3650)),
            is_site_admin=random.choice([True, False]),
            is_council_member=random.choice([True, False]),
            is_banned=random.choice([True, False]),
            token=str(uuid4()),
            profile=StudentMother.random_profile(),
            preferences=StudentMother.random_preferences()
        )
        student.set_password(raw_password, hasher)
        return student


