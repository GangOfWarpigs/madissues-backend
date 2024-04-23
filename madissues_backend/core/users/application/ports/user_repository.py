from abc import ABC, abstractmethod

from madissues_backend.core.shared.application.repository import GenericRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.users.domain.user import User


class UserRepository(GenericRepository[GenericUUID, User], ABC):
    @abstractmethod
    def exists_user_with_email(self, email : str) -> bool:
        pass