from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresStudentPreferences(Base):
    __tablename__ = 'student_preferences'
    __table_args__ = {'schema': 'backend'}

    student_id = Column(UUID(as_uuid=True), ForeignKey('backend.students.id'), primary_key=True)
    theme = Column(String, nullable=False)  # 'Dark' o 'Light'
    language = Column(String, nullable=False)  # Country code
    student = relationship("PostgresStudent", back_populates="preferences")

    @staticmethod
    def default():
        return PostgresStudentPreferences(
            theme="Dark",
            language="es"
        )
