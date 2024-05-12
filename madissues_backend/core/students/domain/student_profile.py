from madissues_backend.core.shared.domain.value_objects import GenericUUID, ValueObject


class StudentProfile(ValueObject):
    degree: GenericUUID
    joined_courses: list[GenericUUID]

