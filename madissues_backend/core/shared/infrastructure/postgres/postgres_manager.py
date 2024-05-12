import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from madissues_backend.core.issues.infrastructure.postgres.ports.comments.postgress_issue_comment_query_repository import \
    PostgresIssueQueryRepository
from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgress_issue_repository import \
    PostgresIssueRepository


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

        self.Base = declarative_base()

    # Función para obtener una sesión
    def get_session(self):
        return self.SessionFactory()


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

    # Aquí puedes realizar operaciones de base de datos, como session.add() o session.query()
    print("Conexión establecida con éxito.")

    # Crear la tabla en la base de datos
    postgres_manager.Base.metadata.create_all(
        postgres_manager.engine
    )

    # Instanciar el repositorio
    issue_repository = PostgresIssueRepository(session)
    issue_query_repository = PostgresIssueQueryRepository(session)

    # Instanciar el repositorio de comentarios
    # issue_comment_repository = PostgresIssueCommentRepository(session)

    # Crear una instancia de Issue para probar el repositorio
    # issue = Issue(
    #     id=GenericUUID.next_id(),
    #     title="Test Issue",
    #     description="This is a test issue",
    #     details="Some details about the test issue",
    #     proofs=["proof1.jpg", "proof2.jpg"],
    #     status="Queued",
    #     date_time=datetime.utcnow(),
    #     course=GenericUUID.next_id(),
    #     teachers=[GenericUUID.next_id(), GenericUUID.next_id()],
    #     student_id=GenericUUID.next_id(),
    #     organization_id=GenericUUID.next_id()
    # )
    #
    # # Agregar la issue a la base de datos
    # issue_repository.add(issue)
    #
    # # Obtener todas las issues y mostrarlas

    session.close()  # No olvides cerrar la sesión
