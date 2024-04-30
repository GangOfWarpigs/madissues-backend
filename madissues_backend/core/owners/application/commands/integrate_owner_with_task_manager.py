from enum import Enum

from pydantic import BaseModel
from madissues_backend.core.shared.application.command import Command, CommandRequest, CommandResponse, owners_only
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.task_manager_service import TaskManagerServiceFactory
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.shared.domain.task_manager import TaskManager


class IntegrateOwnerWithTaskManagerRequest(BaseModel):
    name: str
    api_key: str


class IntegrateOwnerWithTaskManagerResponse(BaseModel):
    name: str
    api_key: str


@owners_only
class IntegrateOwnerWithTaskManagerCommand(Command[IntegrateOwnerWithTaskManagerRequest, IntegrateOwnerWithTaskManagerResponse]):
    def __init__(self, authentication_service: AuthenticationService, owner_repository: OwnerRepository,
                 task_manager_factory: TaskManagerServiceFactory):
        self.authentication_service = authentication_service
        self.repository = owner_repository
        self.task_manager_factory = task_manager_factory

    def execute(self, request: IntegrateOwnerWithTaskManagerRequest) -> Response[IntegrateOwnerWithTaskManagerResponse]:
        owner_id = self.authentication_service.get_user_id()
        task_manager = self.task_manager_factory.get_task_manager_by_name(request.name)
        if not task_manager.is_api_key_valid(request.api_key):
            return Response.fail(code=1, message="Api Key is invalid")
        owner = self.repository.get_by_id(GenericUUID(owner_id))
        owner.integrate_task_manager(request.name, request.api_key)
        self.repository.save(owner)
        return Response.ok(
            IntegrateOwnerWithTaskManagerResponse(
                name=request.name,
                api_key=request.api_key
            )
        )

