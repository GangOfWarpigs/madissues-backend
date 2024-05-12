import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


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

        # Crear una clase base para las tablas
        self.base = declarative_base()

    def getBase(self):
        return self.base

    # Función para obtener una sesión
    def get_session(self):
        return self.SessionFactory()

# Instantiate the PostgresManager class if dotenv variables are set
load_dotenv()

# Obtener valores de las variables de entorno o proporcionar valores predeterminados
POSTGRES_USER = os.getenv('POSTGRES_USER', 'default_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'default_password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'default_db')

postgres_manager = None
# Only instantiate the PostgresManager if all the environment variables are set
if all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB]):
    postgres_manager = PostgresManager(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db=POSTGRES_DB
    )