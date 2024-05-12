from sqlalchemy import Column, String, UUID, ForeignKey, Integer
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresOrganizationCourse(Base):
    __tablename__ = 'organization_courses'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(60), nullable=False)
    code = Column(String(8), nullable=False)
    year = Column(Integer, nullable=False)
    icon = Column(String(60), default='io-cog')
    primary_color = Column(String, nullable=False)
    secondary_color = Column(String, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('backend.organizations.id'))

    # Relación inversa
    organization = relationship("PostgresOrganization", back_populates="courses")
