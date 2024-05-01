from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, organization_repository, storage_service
from madissues_backend.core.organizations.application.commands.organization.create_organization_command import \
    CreateOrganizationRequest, CreateOrganizationResponse, CreateOrganizationCommand
from madissues_backend.core.shared.domain.response import Response

router = APIRouter()


@router.post("/organizations/", tags=["organizations"])
def create_organization(request: CreateOrganizationRequest,
                        token: Annotated[str, Header()]) -> Response[CreateOrganizationResponse]:
    authorization = authorization_service(token)
    command = CreateOrganizationCommand(authorization, organization_repository, storage_service)
    return command.run(request)
