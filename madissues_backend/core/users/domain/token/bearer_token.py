from operator import gt
from typing import Annotated

from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class BearerToken(Entity[GenericUUID]):
    user_id: Annotated[int, gt(0)]
    token: str

