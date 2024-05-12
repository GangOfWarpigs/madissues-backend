from datetime import datetime

from sqlalchemy import Column, String, DateTime, ARRAY, UUID

from madissues_backend.core.shared.infrastructure.postgres.postgres_manager import postgres_manager


# Definir la clase para la tabla IssueComment en el esquema "backend"
class PostgresIssueCommentModel(postgres_manager.getBase()):
    __tablename__ = 'issue_comments'
    __table_args__ = {'schema': 'backend'}

    id: Column = Column(UUID(as_uuid=True), primary_key=True)
    issue_id: Column = Column(UUID(as_uuid=True), nullable=False)
    author: Column = Column(UUID(as_uuid=True), nullable=False)
    likes: Column = Column(ARRAY(UUID(as_uuid=True)))
    content: Column = Column(String, nullable=False)
    date_time: Column = Column(DateTime, default=datetime.utcnow)
    response_to: Column = Column(UUID(as_uuid=True))
