from sqlalchemy import Column, String, UUID, ARRAY, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresOrganizationTeacher(Base):
    __tablename__ = 'organization_teachers'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String, nullable=True)
    office_link = Column(String, nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('backend.organizations.id'))

    # Relación inversa
    organization = relationship("PostgresOrganization", back_populates="teachers")
    courses = Column(ARRAY(UUID(as_uuid=True)))

