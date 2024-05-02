from datetime import datetime

from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, students_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.students.application.ports.student_repository import StudentRepository


class ChangeStudentPersonalDataRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    started_studies_date: str


class ChangeStudentPersonalDataResponse(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    email: str
    started_studies_date: str


@students_only
class UpdateStudentPersonalDataCommand(Command[ChangeStudentPersonalDataRequest, ChangeStudentPersonalDataResponse]):
    def __init__(self, authentication_service: AuthenticationService,
                 student_repository: StudentRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.student_repository = student_repository
        self.event_bus = event_bus

    def execute(self, request: ChangeStudentPersonalDataRequest) -> Response[ChangeStudentPersonalDataResponse]:
        student_id = self.authentication_service.get_user_id()
        student = self.student_repository.get_by_id(GenericUUID(student_id))
        student.update_personal_data(
                first_name=request.first_name,
                last_name=request.last_name,
                email=request.email,
                started_studies_date=request.started_studies_date
        )

        self.student_repository.save(student)
        self.event_bus.notify_all(student.collect_events())

        return Response.ok(ChangeStudentPersonalDataResponse(
            student_id=str(student.id),
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            started_studies_date=datetime.strftime(student.started_studies_date, '%Y-%m-%d')
        ))
