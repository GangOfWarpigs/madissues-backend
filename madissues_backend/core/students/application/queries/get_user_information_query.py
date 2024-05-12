from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.query import Query, QueryParams, QueryResult
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.students.application.ports.student_query_repository import StudentQueryRepository
from madissues_backend.core.students.domain.read_model.student_read_model import StudentReadModel


class GetStudentInformationQuery(Query[None, StudentReadModel]):
    def __init__(self, authorization_service: AuthenticationService, query_repository: StudentQueryRepository):
        self.authentication_service = authorization_service
        self.query_repository = query_repository

    def execute(self, params: QueryParams | None = None) -> Response[StudentReadModel]:
        student = self.query_repository.get_by_id(self.authentication_service.get_user_id())
        if student is None: return Response.fail("There is not student with that token")
        return Response.ok(student)
