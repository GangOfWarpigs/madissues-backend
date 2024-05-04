from pydantic import Field
from typing import Annotated


from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import ValueObject, GenericUUID


class Board(Entity[GenericUUID]):
    queued_list_id: Annotated[str, Field(min_length=1)]
    in_progress_list_id: Annotated[str, Field(min_length=1)]
    solved_list_id: Annotated[str, Field(min_length=1)]
    not_solved_list_id: Annotated[str, Field(min_length=1)]
    board_id: str
