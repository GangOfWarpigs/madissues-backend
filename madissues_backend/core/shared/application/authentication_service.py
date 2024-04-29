from abc import ABC, abstractmethod


class AuthenticationService(ABC):
    @abstractmethod
    def is_authenticated(self):
        ...

    @abstractmethod
    def get_user_id(self) -> int:
        ...

    @abstractmethod
    def is_student(self) -> bool:
        ...

    @abstractmethod
    def is_site_admin(self) -> bool:
        ...

    @abstractmethod
    def is_council_member(self) -> bool:
        ...

    @abstractmethod
    def is_owner(self) -> bool:
        ...

