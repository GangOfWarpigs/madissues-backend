from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository


class ChangeStudentProfileRequest(BaseModel):
    degree: str
    joined_courses: list[str]


class ChangeStudentProfileResponse(BaseModel):
    student_id: str
    degree: str
    joined_courses: list[str]


@students_only
class UpdateStudentProfileCommand(Command[ChangeStudentProfileRequest, ChangeStudentProfileResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 student_repository: StudentRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.student_repository = student_repository
        self.event_bus = event_bus

    def execute(self, request: ChangeStudentProfileRequest) -> Response[ChangeStudentProfileResponse]:
        student_id = self.authentication_service.get_user_id()
        student = self.student_repository.get_by_id(GenericUUID(student_id))
        if student is None:
            return Response.fail(code=2, message="Student is not found")
        student.update_profile(
            degree=request.degree,
            joined_courses=request.joined_courses
        )

        self.student_repository.save(student)
        self.event_bus.notify_all(student.collect_events())

        return Response.ok(ChangeStudentProfileResponse(
            student_id=str(student.id),
            degree=str(student.profile.degree),
            joined_courses=[str(course) for course in student.profile.joined_courses]
        ))
