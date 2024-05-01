from pydantic import BaseModel

from madissues_backend.core.shared.domain.value_objects import GenericUUID


class StudentProfile(BaseModel):
    degree: GenericUUID
    joined_courses: list[GenericUUID]
