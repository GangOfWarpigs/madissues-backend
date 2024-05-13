from datetime import datetime

from sqlalchemy import Column, String, DateTime, ARRAY, UUID, ForeignKey, Table
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base

issue_teacher_association = Table(
    'issue_teacher_association',
    Base.metadata,
    Column('issue_id', ForeignKey('backend.issues.id'), primary_key=True),
    Column('teacher_id', ForeignKey('backend.organization_teachers.id'), primary_key=True),
    schema='backend'
)


# Definir la clase para la tabla Issue
class PostgresIssueModel(Base):
    __tablename__ = 'issues'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(length=80), nullable=False)
    description = Column(String, nullable=False)
    details = Column(String(length=1000), nullable=False)
    proofs = Column(ARRAY(String))
    status = Column(String(length=20), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    course_id = Column(UUID(as_uuid=True), ForeignKey('backend.organization_courses.id'), nullable=False)  # Course foreign key
    student_id = Column(UUID(as_uuid=True), ForeignKey('backend.students.id'), nullable=False)  # Author is a student
    organization_id = Column(UUID(as_uuid=True), ForeignKey('backend.organizations.id'),
                             nullable=False)  # Organization foreign key

    # Relación con los comentarios
    comments = relationship("PostgresIssueCommentModel", back_populates="issue")

    # Relación inversa con la organización
    organization = relationship("PostgresOrganization", back_populates="issues")

    teachers = relationship("PostgresOrganizationTeacher",
                            secondary=issue_teacher_association,
                            back_populates="issues")

    # Relación con los cursos
    course = relationship("PostgresOrganizationCourse", back_populates="issues")
