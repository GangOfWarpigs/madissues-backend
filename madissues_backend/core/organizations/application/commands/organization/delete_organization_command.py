from pydantic import BaseModel
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, CommandResponse, owners_only
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.shared.domain.storage_service import StorageService


class DeleteOrganizationRequest(BaseModel):
    organization_id: str


class DeleteOrganizationResponse(BaseModel):
    organization_id: str


@owners_only
class DeleteOrganizationCommand(Command[DeleteOrganizationRequest, DeleteOrganizationResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository,
                 storage_service: StorageService):
        self.authentication_service = authentication_service
        self.repository = repository
        self.storage_service = storage_service

    def execute(self, request: DeleteOrganizationRequest) -> Response[DeleteOrganizationResponse]:
        organization_id = GenericUUID(request.organization_id)

        # Retrieve organization by ID
        organization = self.repository.get_by_id(organization_id)
        if not organization:
            return Response.fail(code=404, message="Organization not found")

        # Check if the user is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        # Delete the organization's logo if it exists
        if organization.logo:
            organization.delete_logo(self.storage_service)

        # Delete the organization from the repository
        self.repository.remove(organization.id)

        return Response.ok(DeleteOrganizationResponse(
            organization_id=str(organization.id),
        ))
