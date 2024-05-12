from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresTaskManager(Base):
    __tablename__ = 'task_managers'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('backend.organizations.id'), nullable=False)
    task_manager_project_id = Column(UUID(as_uuid=True), nullable=False)

    faqs_board_id = Column(UUID(as_uuid=True), ForeignKey('backend.boards.id'), nullable=True)
    issue_board_id = Column(UUID(as_uuid=True), ForeignKey('backend.boards.id'), nullable=True)

    # Relationships
    config = relationship("PostgresTaskManagerConfig", back_populates="task_manager", uselist=False)
    members = relationship("PostgresMember", back_populates="task_manager")

    # Board relationships
    # faqs_board = relationship("PostgresBoard", back_populates="faqs_task_manager")
    # issue_board = relationship("PostgresBoard", back_populates="issue_task_manager")

    # Relación con Organization
    organization = relationship("PostgresOrganization", foreign_keys=[organization_id])
