from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import authorization_service, task_manager_repository, \
    task_manager_factory
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.task_manager.application.commands.integrate_organization_with_task_manager import \
    IntegrateOrganizationWithTaskManagerRequest, IntegrateOrganizationWithTaskManagerResponse, \
    IntegrateOrganizationWithTaskManagerCommand

router = APIRouter()


@router.post("/task_manager/integrate/", tags=["task manager"])
def integrate_task_manager_with_organization(token: Annotated[str, Header()] = None,
                                             request: IntegrateOrganizationWithTaskManagerRequest = None) -> Response[IntegrateOrganizationWithTaskManagerResponse]:
    print(token)
    authorization = authorization_service(token)
    command = IntegrateOrganizationWithTaskManagerCommand(authorization, task_manager_repository, task_manager_factory)
    return command.run(request)
