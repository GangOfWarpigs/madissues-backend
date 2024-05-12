from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresMember(Base):
    __tablename__ = 'members'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey('backend.students.id'), nullable=False)
    task_manager_id = Column(UUID(as_uuid=True), ForeignKey('backend.task_managers.id'), nullable=False)

    student = relationship("PostgresStudent", foreign_keys=[student_id])
    task_manager = relationship("PostgresTaskManager", back_populates="members")
