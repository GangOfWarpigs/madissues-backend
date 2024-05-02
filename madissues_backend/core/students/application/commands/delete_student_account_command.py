from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, council_members_or_site_admins_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.events.student_deleted import StudentDeleted, StudentDeletedPayload


class DeleteStudentRequest(BaseModel):
    student_id: str


class DeleteStudentResponse(BaseModel):
    student_id: str


class DeleteStudentCommand(Command[DeleteStudentRequest, DeleteStudentResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 student_repository: StudentRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.student_repository = student_repository
        self.event_bus = event_bus

    def execute(self, request: DeleteStudentRequest) -> Response[DeleteStudentResponse]:
        deletion_requestor_id = self.authentication_service.get_user_id()
        deletion_requestor = self.student_repository.get_by_id(GenericUUID(deletion_requestor_id))
        if deletion_requestor is None:
            return Response.fail(code=2, message="User is not found")
        if (not deletion_requestor.is_council_member and
                not deletion_requestor.is_site_admin and
                deletion_requestor.id != request.student_id):
            return Response.fail(code=500, message="You can only delete your own account")

        student_being_deleted = self.student_repository.get_by_id(GenericUUID(request.student_id))
        if student_being_deleted is None:
            return Response.fail(code=3, message="Student is not found")
        self.student_repository.remove(student_being_deleted.id)
        student_being_deleted.register_event(
            StudentDeleted(payload=StudentDeletedPayload(
                deletion_requestor_id=str(deletion_requestor.id),
                user_being_deleted_id=str(student_being_deleted.id)))
        )

        self.event_bus.notify_all(student_being_deleted.collect_events())
        return Response.ok(DeleteStudentResponse(
            student_id=str(student_being_deleted.id)
        ))
