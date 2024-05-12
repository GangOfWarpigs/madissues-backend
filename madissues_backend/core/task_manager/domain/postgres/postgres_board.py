from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresBoard(Base):
    __tablename__ = 'boards'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    queued_list_id = Column(String, nullable=False)
    in_progress_list_id = Column(String, nullable=False)
    solved_list_id = Column(String, nullable=False)
    not_solved_list_id = Column(String, nullable=False)
    board_id = Column(String, nullable=False)

    # Correct relationship specifications
    faqs_task_manager_id = Column(UUID(as_uuid=True), ForeignKey('backend.task_managers.id'), nullable=True)
    issue_task_manager_id = Column(UUID(as_uuid=True), ForeignKey('backend.task_managers.id'), nullable=True)

    # Relationship with TaskManager for FAQs
    faqs_task_manager = relationship("PostgresTaskManager", foreign_keys=[faqs_task_manager_id],
                                      uselist=False)

    # Relationship with TaskManager for Issues
    issue_task_manager = relationship("PostgresTaskManager", foreign_keys=[issue_task_manager_id],
                                     uselist=False)