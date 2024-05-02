from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository
from madissues_backend.core.students.domain.student_preferences import StudentPreferences


class ChangeStudentPreferencesRequest(BaseModel):
    language: str
    theme: str


class ChangeStudentPreferencesResponse(BaseModel):
    student_id: str
    language: str
    theme: str


@students_only
class UpdateStudentPreferencesCommand(Command[ChangeStudentPreferencesRequest, ChangeStudentPreferencesResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 student_repository: StudentRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.student_repository = student_repository
        self.event_bus = event_bus

    def execute(self, request: ChangeStudentPreferencesRequest) -> Response[ChangeStudentPreferencesResponse]:
        student_id = self.authentication_service.get_user_id()
        student = self.student_repository.get_by_id(GenericUUID(student_id))
        student.change_preferences(StudentPreferences(
            language=request.language,
            theme=request.theme
        ))
        self.student_repository.save(student)
        self.event_bus.notify_all(student.collect_events())
        return Response.ok(ChangeStudentPreferencesResponse(
            student_id=str(student.id),
            language=student.preferences.language,
            theme=student.preferences.theme
        ))
