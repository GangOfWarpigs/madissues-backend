from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresOwner(Base):
    __tablename__ = 'owners'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(200), nullable=False)  # Asegúrate de validar el email como en tu dominio
    first_name = Column(String(50), nullable=False)  # Ajusta la longitud según tus requisitos
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)  # Ajusta el tamaño según el patrón de teléfono
    password = Column(String, nullable=False)  # Asumimos que la contraseña está ya hasheada
    token = Column(String, nullable=True)  # Token puede ser opcional

    # Relación con Organization
    organizations = relationship("PostgresOrganization", back_populates="owner")
