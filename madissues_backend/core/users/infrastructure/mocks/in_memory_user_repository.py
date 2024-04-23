from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.users.application.ports.user_repository import UserRepository
from madissues_backend.core.users.domain.user.user import User


class InMemoryUserRepository(UserRepository):
    users: list[User]

    def __init__(self):
        self.users = []

    def add(self, entity: User):
        if self.__index_user_by_id(entity.id) is not None:
            raise Exception("User already exists")
        self.users.append(entity)

    def remove(self, user_id: GenericUUID):
        index = self.__index_user_by_id(user_id)
        if index is None:
            raise Exception("User does not exist")
        del self.users[index]

    def get_by_id(self, user_id: GenericUUID) -> User:
        index = self.__index_user_by_id(user_id)
        if index is None:
            raise Exception("User not found")
        return self.users[index]

    def save(self, entity: User):
        index = self.__index_user_by_id(entity.id)
        if index is None:
            raise Exception("User not found")
        self.users[index] = entity

    def __index_user_by_id(self, user_id) -> int | None:
        for i in range(len(self.users)):
            if self.users[i].id == user_id:
                return i
        return None

    def exists_user_with_email(self, email: str) -> bool:
        raise NotImplementedError()
