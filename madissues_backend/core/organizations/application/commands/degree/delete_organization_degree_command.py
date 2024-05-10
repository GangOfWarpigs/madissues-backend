from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.domain.organization import Organization


class DeleteOrganizationDegreeRequest(BaseModel):
    organization_id: str
    degree_id: str


class DeleteOrganizationDegreeResponse(BaseModel):
    degree_id: str
    organization_id: str


@owners_only
class DeleteOrganizationDegreeCommand(Command[DeleteOrganizationDegreeRequest, DeleteOrganizationDegreeResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository,
                 event_bus: EventBus):
        self.authentication_service = authentication_service
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, request: DeleteOrganizationDegreeRequest) -> Response[DeleteOrganizationDegreeResponse]:
        try:
            organization = self.repository.get_by_id(GenericUUID(request.organization_id))
            assert organization is not None
        except (ValueError, AttributeError):
            return Response.fail(message="Invalid organization ID")

        # Check if the requestor is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        try:
            organization.delete_degree(GenericUUID(request.degree_id))
        except ValueError as e:
            return Response.fail(message=str(e))  # Degree not found

        self.event_bus.notify_all(organization.collect_events())
        self.repository.save(organization)

        return Response.ok(DeleteOrganizationDegreeResponse(
            degree_id=request.degree_id,
            organization_id=request.organization_id
        ))
