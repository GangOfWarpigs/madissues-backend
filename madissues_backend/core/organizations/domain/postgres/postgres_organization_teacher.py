from sqlalchemy import Column, String, UUID, ARRAY, ForeignKey, Table
from sqlalchemy.orm import relationship

from madissues_backend.core.issues.domain.postgres.issue_model import issue_teacher_association
from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base

# Tabla de asociación para profesores y cursos
teacher_course_association = Table(
    'teacher_course_association',
    Base.metadata,
    Column('teacher_id', ForeignKey('backend.organization_teachers.id'), primary_key=True),
    Column('course_id', ForeignKey('backend.organization_courses.id'), primary_key=True),
    schema='backend'
)


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
    courses = relationship("PostgresOrganizationCourse",
                           secondary=teacher_course_association,
                           back_populates="teachers")

    issues = relationship("PostgresIssueModel",
                          secondary=issue_teacher_association,
                          back_populates="teachers")
