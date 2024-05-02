from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, council_members_or_site_admins_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository


class ChangeStudentRoleRequest(BaseModel):
    student_id: str
    admin_role: bool
    council_member_role: bool


class ChangeStudentRoleResponse(BaseModel):
    student_id: str
    admin_role: bool
    council_member_role: bool


@council_members_or_site_admins_only
class ChangeStudentRoleCommand(Command[ChangeStudentRoleRequest, ChangeStudentRoleResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 student_repository: StudentRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.student_repository = student_repository
        self.event_bus = event_bus

    def execute(self, request: ChangeStudentRoleRequest) -> Response[ChangeStudentRoleResponse]:
        student = self.student_repository.get_by_id(GenericUUID(request.student_id))
        if student is None:
            return Response.fail(code=2, message="Student is not found")
        student.change_role(make_admin=request.admin_role,
                            make_council_member=request.council_member_role)
        self.student_repository.save(student)
        self.event_bus.notify_all(student.collect_events())
        return Response.ok(ChangeStudentRoleResponse(
            student_id=str(student.id),
            admin_role=student.is_site_admin,
            council_member_role=student.is_council_member

        ))
