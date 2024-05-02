from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, council_members_or_site_admins_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository


class BanStudentRequest(BaseModel):
    student_id: str


class BanStudentResponse(BaseModel):
    student_id: str
    banned: bool


@council_members_or_site_admins_only
class BanStudentCommand(Command[BanStudentRequest, BanStudentResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 student_repository: StudentRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.student_repository = student_repository
        self.event_bus = event_bus

    def execute(self, request: BanStudentRequest) -> Response[BanStudentResponse]:
        student = self.student_repository.get_by_id(GenericUUID(request.student_id))
        student.ban()
        self.student_repository.save(student)
        self.event_bus.notify_all(student.collect_events())
        return Response.ok(BanStudentResponse(
            student_id=str(student.id),
            banned=student.is_banned
        ))
