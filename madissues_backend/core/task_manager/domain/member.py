from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID, Email


class Member(Entity[GenericUUID]):
    student_id: GenericUUID
    task_manager_email: Email
