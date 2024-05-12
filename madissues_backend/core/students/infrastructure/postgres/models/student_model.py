from sqlalchemy import Column, String, DateTime, UUID, Boolean
from sqlalchemy.orm import relationship, Mapped

from madissues_backend.core.shared.infrastructure.postgres.postgres_manager import postgres_manager
from madissues_backend.core.students.infrastructure.postgres.models.student_preferences_model import StudentPreferences
from madissues_backend.core.students.infrastructure.postgres.models.student_profile_model import StudentProfile


class Student(postgres_manager.getBase()):
    __tablename__ = 'students'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False, default="")
    started_studies_date = Column(DateTime, nullable=False)
    is_site_admin = Column(Boolean, nullable=False, default=False)
    is_council_member = Column(Boolean, nullable=False, default=False)
    is_banned = Column(Boolean, nullable=False, default=False)
    token = Column(String, nullable=False, default="")

    # Relaciones
    # profile: Mapped["StudentProfile"] = relationship("StudentProfile", back_populates="student", uselist=False)
    # preferences: Mapped["StudentPreferences"] = relationship("StudentPreferences", back_populates="student", uselist=False)