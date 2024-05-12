from datetime import datetime

from sqlalchemy import Column, String, DateTime, ARRAY, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


# Definir la clase para la tabla IssueComment en el esquema "backend"
class PostgresIssueCommentModel(Base):
    __tablename__ = 'issue_comments'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    issue_id = Column(UUID(as_uuid=True), ForeignKey('backend.issues.id'), nullable=False)
    author = Column(UUID(as_uuid=True), ForeignKey('backend.students.id'), nullable=False)  # Author is a student
    likes = Column(ARRAY(UUID(as_uuid=True)))
    content = Column(String, nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    response_to = Column(UUID(as_uuid=True), ForeignKey('backend.issue_comments.id'), nullable=True)

    # Relación inversa con Issue
    issue = relationship("PostgresIssueModel", back_populates="comments")

    # Relación opcional con otro comentario
    response_to_comment = relationship("PostgresIssueCommentModel", remote_side=[id], backref="replies")