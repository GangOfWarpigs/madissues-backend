from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.task_manager import TaskManager
from madissues_backend.core.shared.domain.value_objects import ValueObject
from madissues_backend.core.shared.domain.board import Board



class OrganizationTaskManager(ValueObject):
    task_manager_name: TaskManager
    token: str
    faqs_board: Board
    issues_board: Board
