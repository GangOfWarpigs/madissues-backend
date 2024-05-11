from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, organization_repository, \
    storage_service, organization_query_repository, event_bus, issue_query_repository
from madissues_backend.core.issues.application.queries.find_all_issues_for_organization_query import FindAllIssuesQuery, \
    FindAllIssuesQueryParams
from madissues_backend.core.issues.domain.read_models.issue_read_model import IssueReadModel
from madissues_backend.core.organizations.application.commands.course.create_organization_course_command import \
    CreateOrganizationCourseRequest, CreateOrganizationCourseResponse, CreateOrganizationCourseCommand
from madissues_backend.core.organizations.application.commands.degree.create_organization_degree_command import \
    CreateOrganizationDegreeCommand, CreateOrganizationDegreeRequest, CreateOrganizationDegreeResponse
from madissues_backend.core.organizations.application.commands.organization.create_organization_command import \
    CreateOrganizationRequest, CreateOrganizationResponse, CreateOrganizationCommand
from madissues_backend.core.organizations.application.commands.teacher.create_organization_teacher_command import \
    CreateOrganizationTeacherResponse, CreateOrganizationTeacherRequest, CreateOrganizationTeacherCommand
from madissues_backend.core.organizations.application.queries.get_organization_courses_query import \
    GetOrganizationCoursesQuery
from madissues_backend.core.organizations.application.queries.get_organization_degrees_query import \
    GetOrganizationDegreesQuery
from madissues_backend.core.organizations.application.queries.get_organization_task_manager_query import \
    GetOrganizationTaskManagerQuery, GetOrganizationTaskManagerQueryParams
from madissues_backend.core.organizations.application.queries.get_organization_teachers_query import \
    GetOrganizationTeachersQuery
from madissues_backend.core.organizations.application.queries.get_organizations_of_owner_query import \
    GetOrganizationsOfOwnerQuery
from madissues_backend.core.organizations.application.queries.get_single_organization_query import \
    GetSingleOrganizationQuery, Params
from madissues_backend.core.organizations.domain.read_models.organization_course_read_model import \
    OrganizationCourseReadModel
from madissues_backend.core.organizations.domain.read_models.organization_degree_read_model import \
    OrganizationDegreeReadModel
from madissues_backend.core.organizations.domain.read_models.organization_read_model import OrganizationReadModel
from madissues_backend.core.organizations.domain.read_models.organization_task_manager_read_model import \
    OrganizationTaskManagerReadModel
from madissues_backend.core.organizations.domain.read_models.organization_teacher_read_model import \
    OrganizationTeacherReadModel
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/organizations/", tags=["organizations"])
def create_organization(request: CreateOrganizationRequest,
                        token: Annotated[str, Header()]) -> Response[CreateOrganizationResponse]:
    authorization = authorization_service(token)
    command = CreateOrganizationCommand(authorization, organization_repository, storage_service)
    return command.run(request)


@router.post("/organizations/{id}/courses", tags=["organizations"])
def create_organization_course(request: CreateOrganizationCourseRequest,
                               token: Annotated[str, Header()]) -> Response[CreateOrganizationCourseResponse]:
    authorization = authorization_service(token)
    command = CreateOrganizationCourseCommand(authorization, organization_repository, event_bus)
    return command.run(request)


@router.post("/organizations/{id}/teachers", tags=["organizations"])
def create_organization_teacher(request: CreateOrganizationTeacherRequest,
                                token: Annotated[str, Header()]) -> Response[CreateOrganizationTeacherResponse]:
    authorization = authorization_service(token)
    command = CreateOrganizationTeacherCommand(authorization, organization_repository, event_bus)
    return command.run(request)


@router.post("/organizations/{id}/degrees", tags=["organizations"])
def create_organization_degree(request: CreateOrganizationDegreeRequest,
                               token: Annotated[str, Header()]) -> Response[CreateOrganizationDegreeResponse]:
    authorization = authorization_service(token)
    command = CreateOrganizationDegreeCommand(authorization, organization_repository, event_bus)
    return command.run(request)


@router.get("/organizations/", tags=["organizations"])
def list_organization(token: Annotated[str, Header()]) -> Response[list[OrganizationReadModel]]:
    authorization = authorization_service(token)
    query = GetOrganizationsOfOwnerQuery(authorization, organization_query_repository)
    return query.run()


@router.get("/organizations/{id}", tags=["organizations"])
def single_organization(id: str) -> Response[OrganizationReadModel]:
    query = GetSingleOrganizationQuery(organization_query_repository)
    return query.run(Params(id=id))


@router.get("/organizations/{id}/teachers", tags=["organizations"])
def get_organization_teachers(id: str) -> Response[list[OrganizationTeacherReadModel]]:
    query = GetOrganizationTeachersQuery(organization_query_repository)
    return query.run(id)


@router.get("/organizations/{id}/courses", tags=["organizations"])
def get_organization_courses(id: str) -> Response[list[OrganizationCourseReadModel]]:
    query = GetOrganizationCoursesQuery(organization_query_repository)
    return query.run(id)


@router.get("/organizations/{id}/degrees", tags=["organizations"])
def get_organization_degrees(id: str) -> Response[list[OrganizationDegreeReadModel]]:
    query = GetOrganizationDegreesQuery(organization_query_repository)
    return query.run(id)


@router.get("/organizations/{id}/issues/", tags=["organizations"])
def create_issues(token: Annotated[str, Header()], id: str) -> Response[list[IssueReadModel]]:
    authorization = authorization_service(token)
    command = FindAllIssuesQuery(authorization, issue_query_repository)
    return command.run(FindAllIssuesQueryParams(
        organization_id=id
    ))


@router.get("/organizations/{id}/task_manager", tags=["organizations"])
def get_organization_task_manager(id: str) -> Response[OrganizationTaskManagerReadModel]:
    query = GetOrganizationTaskManagerQuery(organization_query_repository)
    return query.run(GetOrganizationTaskManagerQueryParams(
        organization_id=id
    ))
