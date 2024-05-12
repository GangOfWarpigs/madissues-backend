from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from sqlalchemy import text
from sqlalchemy.orm import Session


def create_postgres_authentication_service(session: Session):
    class PostgresAuthenticationService(AuthenticationService):
        def __init__(self, token: str):
            self.session = session
            self.token = token

        def is_authenticated(self) -> bool:
            return self._exists_in_table("owners", self.token) or self._exists_in_table("students", self.token)

        def get_user_id(self) -> str:
            owner_id = self._get_id_from_table("owners", self.token)
            if owner_id:
                return owner_id
            student_id = self._get_id_from_table("students", self.token)
            return student_id if student_id else ''

        def get_student(self):
            return self._get_user_from_table("students", self.token)

        def is_student(self) -> bool:
            return self._exists_in_table("students", self.token)

        def is_site_admin(self) -> bool:
            return self._check_role("students", self.token, "is_site_admin")

        def is_council_member(self) -> bool:
            return self._check_role("students", self.token, "is_council_member")

        def is_owner(self) -> bool:
            return self._exists_in_table("owners", self.token)

        def is_owner_of(self, organization_id: str) -> bool:
            query = text("""
                SELECT EXISTS (
                    SELECT 1 FROM backend.organizations
                    WHERE id = :org_id AND owner_id = (
                        SELECT id FROM backend.owners WHERE token = :token
                    )
                )
            """)
            return self.session.execute(query, {"org_id": organization_id, "token": self.token}).scalar()

        def _exists_in_table(self, table_name, token):
            query = text(f"SELECT EXISTS (SELECT 1 FROM backend.{table_name} WHERE token = :token)")
            return self.session.execute(query, {"token": token}).scalar()

        def _get_id_from_table(self, table_name, token):
            query = text(f"SELECT id FROM backend.{table_name} WHERE token = :token")
            result = self.session.execute(query, {"token": token}).fetchone()
            return str(result[0]) if result else None

        def _get_user_from_table(self, table_name, token):
            query = text(f"SELECT * FROM backend.{table_name} WHERE token = :token")
            return self.session.execute(query, {"token": token}).fetchone()

        def _check_role(self, table_name, token, role_column):
            query = text(f"SELECT {role_column} FROM backend.{table_name} WHERE token = :token")
            result = self.session.execute(query, {"token": token}).scalar()
            return result is True

    return PostgresAuthenticationService
