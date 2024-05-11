from typing import ClassVar

from pydantic import BaseModel

from madissues_backend.core.shared.application.event_handler import EventHandler
from madissues_backend.core.task_manager.application.ports.task_manager_repository import TaskManagerRepository
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerService, TaskManagerFactory


class IssueCreatedPayload(BaseModel):
    title: str
    description: str
    details: str
    proofs: list[str]  # List of image links
    status: str  # Queued, In progress, Solved, Not Solved
    date_time: str
    course: str  # GenericUUID
    teachers: list[str]  # list[GenericUUID]
    student: str  # GenericUUID
    organization_id: str  # GenericUUID


class IssueCreatedHandler(EventHandler[IssueCreatedPayload]):
    event_name: ClassVar[str] = "@issue/issue_created"

    def __init__(self, task_manager_factory: TaskManagerFactory,
                 task_manager_repository: TaskManagerRepository):
        self.task_manager_repository = task_manager_repository
        self.task_manager_factory = task_manager_factory

    def handle(self, payload: IssueCreatedPayload):
        print("--------------Issue created event received--------------")
        print(payload.dict())

        task_manager: TaskManager | None = self.task_manager_repository.get_by_organization_id(payload.organization_id)
        if not task_manager:
            print("No task manager found")
            return

        task_manager_service: TaskManagerService = self.task_manager_factory.of(task_manager.config)

        board_id = task_manager_service.get_board_by_name_in_organization(payload.organization_id, "issues")
        if not board_id:
            print("No board found")
            return

        queued_list_id = task_manager_service.get_board_list_by_name(board_id, "Queued")
        if not queued_list_id:
            print("No list found")
            return

        card_id = task_manager_service.create_card(queued_list_id, payload.title, payload.description)

        print(f"Card created with id: {card_id}")

        # FIXME: Assign the issue to some council member
