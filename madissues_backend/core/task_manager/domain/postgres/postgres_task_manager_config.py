from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresTaskManagerConfig(Base):
    __tablename__ = 'task_manager_configs'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    service = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    api_token = Column(String, nullable=False)
    task_manager_id = Column(UUID(as_uuid=True), ForeignKey('backend.task_managers.id'), unique=True, nullable=False)

    # Relationships
    task_manager = relationship("PostgresTaskManager", back_populates="config", uselist=False)
