from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


def create_mock_authentication_service(database: EntityTable):
    class MockAuthenticationService(AuthenticationService):
        def __init__(self, token: str):
            self.token: str = token
            self.database: EntityTable = database

        def is_authenticated(self) -> bool:
            owners = self.database.tables["owners"]
            for owner in owners.values():
                if owner.token == self.token:
                    return True
            students = self.database.tables["students"]
            for student in students.values():
                if student.token == self.token:
                    return True
            return False

        def get_user_id(self) -> str:
            owners = self.database.tables["owners"]
            students = self.database.tables["students"]
            for owner in owners.values():
                if owner.token == self.token:
                    return str(owner.id)
            for student in students.values():
                if student.token == self.token:
                    return str(student.id)
            return ''

        def get_student(self):
            students = self.database.tables["students"]
            for student in students.values():
                if student.token == self.token:
                    return student
            return None

        def is_student(self) -> bool:
            if self.__token_is_in_owner_table() or not self.__token_is_in_student_table():
                return False
            return True

        def is_owner(self) -> bool:
            if self.__token_is_in_student_table() or not self.__token_is_in_owner_table():
                return False
            return True

        def is_owner_of(self, organization_id: str) -> bool:
            # Get organization by id
            organization = self.database.tables["organizations"][GenericUUID(organization_id)]
            owners = self.database.tables["owners"]
            for owner in owners.values():
                if owner.token == self.token and owner.id == organization.owner_id:
                    return True
            return False

        def is_site_admin(self) -> bool:
            students = self.database.tables["students"]
            for student in students.values():
                if student.token == self.token and student.is_site_admin:
                    return True
            return False

        def is_council_member(self) -> bool:
            students = self.database.tables["students"]
            for student in students.values():
                if student.token == self.token and student.is_council_member:
                    return True
            return False

        def __token_is_in_owner_table(self):
            owners = self.database.tables["owners"]
            for owner in owners.values():
                if owner.token == self.token:
                    return True
            return False

        def __token_is_in_student_table(self):
            students = self.database.tables["students"]
            for student in students.values():
                if student.token == self.token:
                    return True
            return False



    return MockAuthenticationService
