from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, organization_repository, \
    storage_service, organization_query_repository
from madissues_backend.core.organizations.application.commands.organization.create_organization_command import \
    CreateOrganizationRequest, CreateOrganizationResponse, CreateOrganizationCommand
from madissues_backend.core.organizations.application.queries.get_organizations_of_owner_query import \
    GetOrganizationsOfOwnerQuery
from madissues_backend.core.organizations.application.queries.get_single_organization_query import \
    GetSingleOrganizationQuery, Params
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/organizations/", tags=["organizations"])
def create_organization(request: CreateOrganizationRequest,
                        token: Annotated[str, Header()]) -> Response[CreateOrganizationResponse]:
    authorization = authorization_service(token)
    command = CreateOrganizationCommand(authorization, organization_repository, storage_service)
    return command.run(request)


@router.get("/organizations/", tags=["organizations"])
def list_organization(token: Annotated[str, Header()]):
    authorization = authorization_service(token)
    query = GetOrganizationsOfOwnerQuery(authorization, organization_query_repository)
    return query.execute()


@router.get("/organizations/{id}", tags=["organizations"])
def single_organization(token: Annotated[str, Header()], id: str):
    authorization = authorization_service(token)
    query = GetSingleOrganizationQuery(authorization, organization_query_repository)
    return query.execute(Params(id=id))
