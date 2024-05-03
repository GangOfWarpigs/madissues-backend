from pydantic import Field

from madissues_backend.core.shared.domain.value_objects import ValueObject
from madissues_backend.core.task_manager.domain.card import Card


class Board(ValueObject):
    board_id: str
    queued_list_id: str
    in_progress_list_id: str
    solved_list_id: str
    not_solved_list_id: str
    cards: list[Card] = Field(init=False, default=list())
