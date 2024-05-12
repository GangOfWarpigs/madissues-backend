from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresOrganization(Base):
    __tablename__ = 'organizations'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('backend.owners.id'), nullable=False)
    name = Column(String(280), nullable=False)
    logo = Column(String, default='default_organization_logo.png')
    description = Column(String(4500), nullable=False)
    contact_info = Column(String(80), nullable=False)
    primary_color = Column(String, nullable=False)
    secondary_color = Column(String, nullable=False)

    # Relaciones
    teachers = relationship("PostgresOrganizationTeacher", back_populates="organization")
    courses = relationship("PostgresOrganizationCourse", back_populates="organization")
    degrees = relationship("PostgresOrganizationDegree", back_populates="organization")

    # Relación inversa: una organización tiene un único propietario
    owner = relationship("PostgresOwner", back_populates="organizations")
