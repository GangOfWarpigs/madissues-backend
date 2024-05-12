from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_manager import postgres_manager


class StudentPreferences(postgres_manager.getBase()):
    __tablename__ = 'student_preferences'
    __table_args__ = {'schema': 'backend'}

    student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'), primary_key=True)
    theme = Column(String, nullable=False)  # 'Dark' o 'Light'
    language = Column(String, nullable=False)  # Country code

    @staticmethod
    def default():
        return StudentPreferences(
            theme="Dark",
            language="es"
        )

    # student = relationship("Student", back_populates="preferences")