import datetime

from pydantic import BaseModel

from madissues_backend.core.shared.application.command import Command
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.student import Student
from madissues_backend.core.students.domain.student_preferences import StudentPreferences
from madissues_backend.core.students.domain.student_profile import StudentProfile


class SignUpStudentCommandRequest(BaseModel):
    organization_id: str
    email: str
    first_name: str
    last_name: str
    password: str
    verify_password: str
    phone_number: str
    degreeId: str
    started_studies_date: str


class SignUpStudentCommandResponse(BaseModel):
    token: str
    student_id: str


class SignUpStudentCommand(Command[SignUpStudentCommandRequest, SignUpStudentCommandResponse]):

    def __init__(self, student_repository: StudentRepository, password_hasher: PasswordHasher,
                 token_generator: TokenGenerator):
        self.student_repository = student_repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    def execute(self, request: SignUpStudentCommandRequest) -> Response[SignUpStudentCommandResponse]:
        if self.student_repository.exists_with_email(request.email):
            return Response.fail(code=2, message="Email is already in use")
        if self.passwords_do_not_match(request.password, request.verify_password):
            return Response.fail(code=3, message="Passwords do not match")
        if not self.student_repository.can_student_join_organization(GenericUUID(request.organization_id)):
            return Response.fail(code=4, message="Student cannot join organization")

        student = Student(
            id=GenericUUID.next_id(),
            organization_id=GenericUUID(request.organization_id),
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            started_studies_date=datetime.datetime.strptime(request.started_studies_date, "%Y-%m-%d"),
            is_site_admin=False,
            is_council_member=False,
            is_banned=False,
            profile=StudentProfile(
                degree=GenericUUID(request.degreeId),
                joined_courses=[]
            ),
            preferences=StudentPreferences.default(),
        )
        student.set_password(raw_password=request.password, hasher=self.password_hasher)
        student.generate_auth_token(self.token_generator)

        self.student_repository.add(student)

        return Response.ok(
            SignUpStudentCommandResponse(
                student_id=str(student.id),
                token=student.token
            )
        )

    @staticmethod
    def passwords_do_not_match(password, verify_password):
        return password != verify_password
