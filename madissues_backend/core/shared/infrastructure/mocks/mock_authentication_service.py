from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.mock_repository import EntityTable


def createMockAuthenticationService(database: EntityTable):
    class MockAuthenticationService(AuthenticationService):
        def __init__(self, token: str):
            self.token: str = token
            self.database: EntityTable = database

        def is_authenticated(self) -> bool:
            ...

        def get_user_id(self) -> int:
            raise NotImplementedError()

        def is_student(self) -> bool:
            raise NotImplementedError()

        def is_owner(self) -> bool:
            raise NotImplementedError()

        def is_site_admin(self) -> bool:
            raise NotImplementedError()

        def is_council_member(self) -> bool:
            raise NotImplementedError()


    return MockAuthenticationService