from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository


class ChangeStudentEmailRequest(BaseModel):
    email: str


class ChangeStudentEmailResponse(BaseModel):
    student_id: str
    email: str


@students_only
class ChangeStudentEmailCommand(Command[ChangeStudentEmailRequest, ChangeStudentEmailResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 student_repository: StudentRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.student_repository = student_repository
        self.event_bus = event_bus

    def execute(self, request: ChangeStudentEmailRequest) -> Response[ChangeStudentEmailResponse]:
        student_id = self.authentication_service.get_user_id()
        student = self.student_repository.get_by_id(GenericUUID(student_id))
        student.change_email(request.email)
        self.student_repository.save(student)
        self.event_bus.notify_all(student.collect_events())
        return Response.ok(ChangeStudentEmailResponse(
            student_id=str(student.id),
            email=student.email
        ))
