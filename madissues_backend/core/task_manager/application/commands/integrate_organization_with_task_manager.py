from pydantic import BaseModel

from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.command import Command, CommandRequest, CommandResponse, owners_only
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.application.ports.task_manager_repository import TaskManagerRepository
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerFactory


class IntegrateOrganizationWithTaskManagerRequest(BaseModel):
    organization_id: str
    task_manager: str
    api_key: str


class IntegrateOrganizationWithTaskManagerResponse(BaseModel):
    message: str


@owners_only
class IntegrateOrganizationWithTaskManagerCommand(
    Command[IntegrateOrganizationWithTaskManagerRequest, IntegrateOrganizationWithTaskManagerResponse]):

    def __init__(self, authentication_service: AuthenticationService, repository: TaskManagerRepository,
                 factory: TaskManagerFactory):
        self.authentication_service = authentication_service
        self.repository = repository
        self.factory = factory

    def execute(self, request: IntegrateOrganizationWithTaskManagerRequest) -> Response[
        IntegrateOrganizationWithTaskManagerResponse]:
        owner_id = self.authentication_service.get_user_id()
        organization_id = request.organization_id
        if not self.repository.check_can_integrate_organization(organization_id, owner_id):
            return Response.fail(code=2, message="You have no permissions for performing this action")

        if self.repository.is_there_a_task_manager_for_organization(organization_id):
            return Response.fail(code=2, message="You have integrated your organization with a task manager already")

        task_manager = TaskManager(
            id=GenericUUID.next_id(),
            organization_id=GenericUUID(organization_id),
            config=TaskManagerConfig(
                service=request.task_manager,
                api_key=request.api_key
            )
        )

        task_manager.generate_infrastructure(task_manager_factory=self.factory)

        return Response.ok(
            IntegrateOrganizationWithTaskManagerResponse(
                message="Integration finished successfully"
            )
        )
