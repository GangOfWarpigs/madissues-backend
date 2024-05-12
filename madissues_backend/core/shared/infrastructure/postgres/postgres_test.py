import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgres_issue_query_repository import \
    PostgresIssueQueryRepository
from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgres_issue_repository import \
    PostgresIssueRepository
from madissues_backend.core.organizations.domain.organization_mother import OrganizationMother
from madissues_backend.core.organizations.infrastructure.ports.postgres_organization_repository import \
    PostgresOrganizationRepository
from madissues_backend.core.owners.domain.owner_mother import OwnerMother
from madissues_backend.core.owners.infrastructure.postgres.ports.postgres_owner_repository import \
    PostgresOwnerRepository
from madissues_backend.core.shared.infrastructure.postgres.postgres_authentication_service import \
    create_postgres_authentication_service
from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base
from madissues_backend.core.shared.infrastructure.postgres.postgres_manager import PostgresManager
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.infrastructure.postgres.ports.postgres_student_repository import \
    PostgresStudentRepository


def check_cases():
    # Instanciar el repositorio
    issue_repository = PostgresIssueRepository(session)
    issue_query_repository = PostgresIssueQueryRepository(session)
    student_repository = PostgresStudentRepository(session)
    organization_repository = PostgresOrganizationRepository(session)
    owner_repository = PostgresOwnerRepository(session)

    # # Crear un student
    student = StudentMother.random_student()
    print("============================================================")
    print(student)
    print("============================================================")

    # Agregar el student a la base de datos
    student_repository.add(student)

    # Obtener el estudiante
    student = student_repository.get_by_id(student.id)

    print("------------------------------------------------------------")
    if student:
        print(student)
    else:
        print("Student not found")
    print("------------------------------------------------------------")

    owner = OwnerMother.generate_owner()
    print("============================================================")
    print(owner)
    print("============================================================")

    # Agregar el owner a la base de datos
    owner_repository.add(owner)

    # Obtener el owner
    owner = owner_repository.get_by_id(owner.id)
    print("------------------------------------------------------------")
    if owner:
        print(owner)
    else:
        print("Owner not found")
    print("------------------------------------------------------------")

    # # Crear una instancia de Issue para probar el repositorio
    organization = OrganizationMother.generate_organization()
    organization.owner_id = owner.id
    print(organization)

    # Agregar la organization a la base de datos
    organization_repository.add(organization)

    # Obtener todas las organizations y mostrarlas
    organization = organization_repository.get_by_id(organization.id)

    if organization:
        print(organization)
    else:
        print("Organization not found")
    #


def check_authentication_service(session: Session):
    authentication_service = create_postgres_authentication_service(session)("57eed210-3abe-448e-98d7-841ae7504a4f")
    print("------------------------------------------------------------")
    print("IS_AUTHENTICATED: ", authentication_service.is_authenticated())
    print("------------------------------------------------------------")
    print("IS OWNER: ", authentication_service.is_owner())
    print("------------------------------------------------------------")
    print("IS STUDENT: ", authentication_service.is_student())
    print("------------------------------------------------------------")
    print("IS SITE ADMIN: ", authentication_service.is_site_admin())
    print("------------------------------------------------------------")
    print("IS COUNCIL MEMBER: ", authentication_service.is_council_member())
    print("------------------------------------------------------------")
    print("IS OWNER OF: ", authentication_service.is_owner_of("57eed210-3abe-448e-98d7-841ae7504a4f"))
    print("------------------------------------------------------------")
    print("GET USER ID: ", authentication_service.get_user_id())
    print("------------------------------------------------------------")
    print("GET STUDENT: ", authentication_service.get_student())
    print("------------------------------------------------------------")


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

    check_authentication_service(session)

    session.close()  # No olvides cerrar la sesión
