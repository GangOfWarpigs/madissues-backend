from madissues_backend.core.shared.domain.entity import (Entity)
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class StudentProfile(Entity[GenericUUID]):
    degree: int
    joined_courses: list[int]
