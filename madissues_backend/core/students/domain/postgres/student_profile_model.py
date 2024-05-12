from sqlalchemy import Column, ARRAY, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresStudentProfile(Base):
    __tablename__ = 'student_profiles'
    __table_args__ = {'schema': 'backend'}

    student_id = Column(UUID(as_uuid=True), ForeignKey('backend.students.id'), primary_key=True)
    degree = Column(UUID(as_uuid=True), nullable=False)
    joined_courses = Column(ARRAY(UUID(as_uuid=True)), nullable=True)  # Lista de cursos
    student = relationship("PostgresStudent", back_populates="profile")

