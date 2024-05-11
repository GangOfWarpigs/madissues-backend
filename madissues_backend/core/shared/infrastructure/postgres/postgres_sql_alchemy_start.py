import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

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


# Función para obtener una sesión
def get_session():
    return SessionFactory()


# Ejemplo de uso
if __name__ == "__main__":
    session = get_session()
    # Aquí puedes realizar operaciones de base de datos, como session.add() o session.query()
    print("Conexión establecida con éxito.")
    # Obtener las tablas del esquema "backend"
    tables = engine.connect().execute("SELECT table_name FROM information_schema.tables WHERE table_schema='backend'")
    session.close()  # No olvides cerrar la sesión
