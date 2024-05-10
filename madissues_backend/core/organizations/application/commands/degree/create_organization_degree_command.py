from pydantic import BaseModel, Field

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, owners_only
from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.domain.storage_service import StorageService
from madissues_backend.core.organizations.domain.organization import Organization
from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.organizations.domain.organization_degree import OrganizationDegree


class CreateOrganizationDegreeRequest(BaseModel):
    organization_id: str
    name: str


class CreateOrganizationDegreeResponse(BaseModel):
    id: str
    organization_id: str
    name: str


@owners_only
class CreateOrganizationDegreeCommand(Command[CreateOrganizationDegreeRequest, CreateOrganizationDegreeResponse]):
    def __init__(self, authentication_service: AuthenticationService, repository: OrganizationRepository, event_bus: EventBus):
        self.authentication_service = authentication_service
        self.repository = repository
        self.event_bus = event_bus

    def execute(self, request: CreateOrganizationDegreeRequest) -> Response[CreateOrganizationDegreeResponse]:
        try:
            organization = self.repository.get_by_id(GenericUUID(request.organization_id))
            assert organization is not None
        except (ValueError, AttributeError):
            return Response.fail(message="Invalid organization ID")

        # Check if the requestor is the owner of the organization
        if not self.authentication_service.is_owner_of(str(organization.id)):
            return Response.fail(message="You are not the owner of the organization")

        degree = OrganizationDegree(
            id=GenericUUID.next_id(),
            name=request.name
        )

        try:
            organization.add_degree(degree)
        except ValueError as e:
            return Response.fail(message=str(e))  # Degree already exists


        self.event_bus.notify_all(organization.collect_events())

        self.repository.save(organization)

        return Response.ok(CreateOrganizationDegreeResponse(
            id=str(degree.id),
            organization_id=str(organization.id),
            name=degree.name
        ))
