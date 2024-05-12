from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from madissues_backend.core.issues.domain.postgres.issue_comment_model import PostgresIssueCommentModel
from madissues_backend.core.issues.domain.postgres.issue_model import PostgresIssueModel
from madissues_backend.core.organizations.domain.postgres.postgres_organization import PostgresOrganization
from madissues_backend.core.organizations.domain.postgres.postgres_organization_course import PostgresOrganizationCourse
from madissues_backend.core.organizations.domain.postgres.postgres_organization_degree import PostgresOrganizationDegree
from madissues_backend.core.organizations.domain.postgres.postgres_organization_teacher import \
    PostgresOrganizationTeacher
from madissues_backend.core.owners.domain.postgres.postgres_owner_model import PostgresOwner
from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base

from madissues_backend.core.students.domain.postgres.student_model import PostgresStudent
from madissues_backend.core.students.domain.postgres.student_preferences_model import PostgresStudentPreferences
from madissues_backend.core.students.domain.postgres.student_profile_model import PostgresStudentProfile
from madissues_backend.core.task_manager.domain.postgres.postgres_board import PostgresBoard
from madissues_backend.core.task_manager.domain.postgres.postgres_member import PostgresMember
from madissues_backend.core.task_manager.domain.postgres.postgres_task_manager import PostgresTaskManager
from madissues_backend.core.task_manager.domain.postgres.postgres_task_manager_config import PostgresTaskManagerConfig

PostgresIssueCommentModel()
PostgresIssueModel()
PostgresStudent()
PostgresStudentPreferences()
PostgresStudentProfile()
PostgresOrganization()
PostgresOrganizationCourse()
PostgresOrganizationDegree()
PostgresOrganizationTeacher()
PostgresOwner()
PostgresTaskManager()
PostgresMember()
PostgresBoard()
PostgresTaskManagerConfig()


class PostgresManager:
    def __init__(self, user, password, host, port, db):
        # Configuración de la conexión a la base de datos PostgreSQL
        self.POSTGRES_USER = user
        self.POSTGRES_PASSWORD = password
        self.POSTGRES_HOST = host
        self.POSTGRES_PORT = port
        self.POSTGRES_DB = db

        self.DATABASE_URL = f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

        # Crear el motor de base de datos
        self.engine = create_engine(self.DATABASE_URL, echo=True)

        # Crear una clase de SessionFactory
        self.SessionFactory = sessionmaker(bind=self.engine)

        self.base = Base

    # Función para obtener una sesión
    def get_session(self):
        return self.SessionFactory()
