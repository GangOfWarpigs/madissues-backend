from typing import Optional

from pydantic import Field, BaseModel

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.storage_service import StorageService
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class UpdateOrganizationRequest(BaseModel):
    organization_id: str
    name: Optional[str] = None
    logo: Optional[str] = Field(default=None)
    description: Optional[str] = None
    contact_info: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None


class UpdateOrganizationResponse(BaseModel):
    id: str
    name: str
    logo: str | None
    description: str
    contact_info: str
    primary_color: str
    secondary_color: str


@owners_only
class UpdateOrganizationCommand(Command[UpdateOrganizationRequest, UpdateOrganizationResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository,
                 storage: StorageService, event_bus: EventBus):
        self.authentication_service = authentication_service
        self.repository = repository
        self.storage_service = storage
        self.event_bus = event_bus

    def execute(self, request: UpdateOrganizationRequest) -> Response[UpdateOrganizationResponse]:
        organization = self.repository.get_by_id(GenericUUID(request.organization_id))
        if not organization:
            return Response.fail(code=404, message="Organization not found")

        # Check if the requestor is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        # Update the organization with the provided data
        organization.update_info(
            name=request.name if request.name else organization.name,
            description=request.description if request.description else organization.description,
            contact_info=request.contact_info if request.contact_info else organization.contact_info,
            primary_color=request.primary_color if request.primary_color else organization.primary_color,
            secondary_color=request.secondary_color if request.secondary_color else organization.secondary_color
        )

        # Handle logo update if provided
        if request.logo:
            organization.upload_logo(request.logo, self.storage_service)

        # Publish the organization updated event
        self.event_bus.notify_all(organization.collect_events())

        # Save the updated organization
        updated_organization = self.repository.save(organization)

        return Response.ok(UpdateOrganizationResponse(
            **updated_organization.dict()
        ))
