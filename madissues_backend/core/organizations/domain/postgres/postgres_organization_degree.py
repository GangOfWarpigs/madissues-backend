from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresOrganizationDegree(Base):
    __tablename__ = 'organization_degrees'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('backend.organizations.id'))

    # Relación inversa
    organization = relationship("PostgresOrganization", back_populates="degrees")
