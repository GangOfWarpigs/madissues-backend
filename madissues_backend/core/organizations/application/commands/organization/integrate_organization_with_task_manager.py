from pydantic import BaseModel

from madissues_backend.core.organizations.application.ports.organization_repository import OrganizationRepository
from madissues_backend.core.shared.application.command import Command, CommandRequest, CommandResponse, owners_only
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.task_manager_service import TaskManagerServiceFactory
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.task_manager import TaskManager
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class IntegrateOrganizationWithTaskManagerRequest(BaseModel):
    organization_id: str
    task_manager_name: TaskManager
    token: str


class IntegrateOrganizationWithTaskManagerResponse(BaseModel):
    message: str


@owners_only
class IntegrateOrganizationWithTaskManagerCommand(
    Command[IntegrateOrganizationWithTaskManagerRequest, IntegrateOrganizationWithTaskManagerResponse]):
    def __init__(self, authorization_service: AuthenticationService,
                 organization_repository: OrganizationRepository,
                 task_manager_factory: TaskManagerServiceFactory):
        self.repository = organization_repository
        self.authorization_service = authorization_service
        self.task_manager_factory = task_manager_factory

    def execute(self, request: IntegrateOrganizationWithTaskManagerRequest) -> Response[
        IntegrateOrganizationWithTaskManagerResponse]:
        organization = self.repository.get_by_id(GenericUUID(request.organization_id))
        task_manager = self.task_manager_factory.get_task_manager_by_name(request.task_manager_name)
        if organization is None:
            return Response.fail(code=2, message="Organization does not exist")
        if organization.owner_id != self.authorization_service.get_user_id():
            return Response.fail(code=3, message="You are not owner of this organization")
        if not task_manager.is_api_key_valid(request.token):
            return Response.fail(code=4, message="Api key is not valid for service")

        organization.integrate_task_manager(request.task_manager_name, request.token)
        self.repository.save(organization)

        return Response.ok(
            IntegrateOrganizationWithTaskManagerResponse(
                message="Integration successful"
            )
        )
