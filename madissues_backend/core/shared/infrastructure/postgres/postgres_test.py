import os

from dotenv import load_dotenv

from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgres_issue_query_repository import \
    PostgresIssueQueryRepository
from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgres_issue_repository import \
    PostgresIssueRepository
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base

from madissues_backend.core.shared.infrastructure.postgres.postgres_manager import PostgresManager
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.infrastructure.postgres.ports.postgres_student_repository import \
    PostgresStudentRepository

# Ejemplo de uso
if __name__ == "__main__":
    # Postgres
    load_dotenv()

    # Obtener valores de las variables de entorno o proporcionar valores predeterminados
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')

    postgres_manager = PostgresManager(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db=POSTGRES_DB
    )

    session = postgres_manager.get_session()

    Base.metadata.create_all(
        postgres_manager.engine
    )

    # Instanciar el repositorio
    issue_repository = PostgresIssueRepository(session)
    issue_query_repository = PostgresIssueQueryRepository(session)
    student_repository = PostgresStudentRepository(session)

    # # Crear un student
    student = StudentMother.random_student()
    #
    # # Agregar el student a la base de datos
    student_repository.add(student)

    # Obtener el estudiante
    student = student_repository.get_by_id(GenericUUID("7eb20012-1f74-4907-b322-81f45b8c2d62"))
    if student:
        print(student)
    else:
        print("Student not found")

    session.close()  # No olvides cerrar la sesión
