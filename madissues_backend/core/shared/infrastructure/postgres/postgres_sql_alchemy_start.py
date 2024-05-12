import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from madissues_backend.core.issues.infrastructure.postgres.ports.issues.postgress_issue_repository import PostgresIssueRepository

# Cargar las variables de entorno
load_dotenv()

# Configuración de la conexión a la base de datos PostgreSQL desde las variables de entorno

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una clase de SessionFactory
SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()




# Función para obtener una sesión
def get_session():
    return SessionFactory()


# Ejemplo de uso
if __name__ == "__main__":
    session = get_session()
    # Aquí puedes realizar operaciones de base de datos, como session.add() o session.query()
    print("Conexión establecida con éxito.")

    # Crear la tabla en la base de datos
    Base.metadata.create_all(engine)

    # Instanciar el repositorio
    issue_repository = PostgresIssueRepository(session)

    # Instanciar el repositorio de comentarios
    #issue_comment_repository = PostgresIssueCommentRepository(session)

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
    issues = issue_repository.get_all()
    print("Todas las issues en la base de datos:")
    for issue in issues:
        print(issue.title)

    # Obtener una issue por su ID y mostrar sus detalles
    issue_id = issues[0].id
    retrieved_issue = issue_repository.get_by_id(issue_id)
    if retrieved_issue:
        print("\nDetalles de la primera issue:")
        print(f"Título: {retrieved_issue.title}")
        print(f"Descripción: {retrieved_issue.description}")
        print(f"Estado: {retrieved_issue.status}")
    else:
        print("No se encontró ninguna issue con ese ID.")

    issues = issue_repository.get_all_by_status("Queued")
    print("\nIssues en estado 'Queued':")
    for issue in issues:
        print(issue)

    # Add comments for each queued issue
    # for issue in issues:
    #     issue_repository.add_comment_to_issue(issue.id, "This is a test comment", datetime.utcnow())



    # Create comments


    session.close()  # No olvides cerrar la sesión
