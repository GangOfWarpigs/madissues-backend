from pydantic import BaseModel
from madissues_backend.core.shared.application.command import Command
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.students.application.ports.student_repository import StudentRepository


class SignInStudentCommandRequest(BaseModel):
    email: str
    password: str


class SignInStudentCommandResponse(BaseModel):
    token: str
    student_id: str


class SignInStudentCommand(Command[SignInStudentCommandRequest, SignInStudentCommandResponse]):

    def __init__(self, student_repository: StudentRepository, password_hasher: PasswordHasher):
        self.student_repository = student_repository
        self.password_hasher = password_hasher

    def execute(self, request: SignInStudentCommandRequest) -> Response[SignInStudentCommandResponse]:
        student = self.student_repository.get_by_email(request.email)
        if not student:
            return Response.fail(code=1, message="User not found")

        if not student.check_password(request.password, self.password_hasher):
            return Response.fail(code=2, message="Incorrect password")

        return Response.ok(
            SignInStudentCommandResponse(
                student_id=str(student.id),
                token=student.token
            )
        )
