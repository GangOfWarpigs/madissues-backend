from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, organization_repository, \
    storage_service, organization_query_repository, event_bus
from madissues_backend.core.organizations.application.commands.course.create_organization_course_command import \
    CreateOrganizationCourseRequest, CreateOrganizationCourseResponse, CreateOrganizationCourseCommand
from madissues_backend.core.organizations.application.commands.organization.create_organization_command import \
    CreateOrganizationRequest, CreateOrganizationResponse, CreateOrganizationCommand
from madissues_backend.core.organizations.application.queries.get_organization_courses_query import \
    GetOrganizationCoursesQuery
from madissues_backend.core.organizations.application.queries.get_organization_teachers_query import \
    GetOrganizationTeachersQuery
from madissues_backend.core.organizations.application.queries.get_organizations_of_owner_query import \
    GetOrganizationsOfOwnerQuery
from madissues_backend.core.organizations.application.queries.get_single_organization_query import \
    GetSingleOrganizationQuery, Params
from madissues_backend.core.organizations.domain.read_models.organization_course_read_model import \
    OrganizationCourseReadModel
from madissues_backend.core.organizations.domain.read_models.organization_read_model import OrganizationReadModel
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



@router.get("/organizations/", tags=["organizations"])
def list_organization(token: Annotated[str, Header()]) -> Response[list[OrganizationReadModel]]:
    authorization = authorization_service(token)
    query = GetOrganizationsOfOwnerQuery(authorization, organization_query_repository)
    return query.execute()


@router.get("/organizations/{id}", tags=["organizations"])
def single_organization(token: Annotated[str, Header()], id: str) -> Response[OrganizationReadModel]:
    authorization = authorization_service(token)
    query = GetSingleOrganizationQuery(authorization, organization_query_repository)
    return query.execute(Params(id=id))

@router.get("/organizations/{id}/teachers", tags=["organizations"])
def get_organization_teachers(token: Annotated[str, Header()], id: str) -> Response[list[OrganizationTeacherReadModel]]:
    authorization = authorization_service(token)
    query = GetOrganizationTeachersQuery(authorization, organization_query_repository)
    return query.execute(id)

@router.get("/organizations/{id}/teachers", tags=["organizations"])
def get_organization_courses(token: Annotated[str, Header()], id: str) -> Response[list[OrganizationCourseReadModel]]:
    authorization = authorization_service(token)
    query = GetOrganizationCoursesQuery(authorization, organization_query_repository)
    return query.execute(id)
