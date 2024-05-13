from sqlalchemy import Column, ARRAY, UUID, ForeignKey, Table
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base

student_course_association = Table(
    'student_course_association',
    Base.metadata,
    Column('student_id', ForeignKey('backend.student_profiles.student_id'), primary_key=True),
    Column('course_id',  ForeignKey('backend.organization_courses.id'), primary_key=True),
    schema='backend'
)


class PostgresStudentProfile(Base):
    __tablename__ = 'student_profiles'
    __table_args__ = {'schema': 'backend'}

    student_id = Column(UUID(as_uuid=True), ForeignKey('backend.students.id'), primary_key=True)
    degree_id = Column(UUID(as_uuid=True), ForeignKey('backend.organization_degrees.id'), nullable=False)
    student = relationship("PostgresStudent", back_populates="profile")
    joined_courses = relationship("PostgresOrganizationCourse",
                                  secondary=student_course_association,
                                  back_populates="students")

    degree = relationship("PostgresOrganizationDegree", back_populates="students")