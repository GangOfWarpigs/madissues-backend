from typing import Literal

from madissues_backend.core.shared.domain.entity import AggregateRoot
from madissues_backend.core.shared.domain.value_objects import GenericUUID, ValueObject
from madissues_backend.core.task_manager.domain.board import Board
from madissues_backend.core.task_manager.domain.member import Member
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerFactory, TaskManagerService


class TaskManager(AggregateRoot[GenericUUID]):
    config: TaskManagerConfig
    faqs_board: Board
    issue_board: Board
    members: list[Member]

    def generate_infrastructure(self, task_manager_factory: TaskManagerFactory):
        task_manager = task_manager_factory.of(self.config)
        self.faqs_board = self.generate_idle_board("faqs", task_manager)
        self.issue_board = self.generate_idle_board("issues", task_manager)

    @staticmethod
    def generate_idle_board(name: str, task_manager: TaskManagerService) -> Board:
        board_id = task_manager.create_empty_board(name)
        return Board(
            board_id=board_id,
            queued_list_id=task_manager.create_empty_list(board_id, "Queued"),
            in_progress_list_id=task_manager.create_empty_list(board_id, "In progress"),
            solved_list_id=task_manager.create_empty_list(board_id, "Solved"),
            not_solved_list_id=task_manager.create_empty_list(board_id, "Not solved")
        )
