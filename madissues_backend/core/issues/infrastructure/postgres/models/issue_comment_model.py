from datetime import datetime

from sqlalchemy import Column, String, DateTime, ARRAY, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Definir la clase para la tabla IssueComment en el esquema "backend"
class IssueComment(Base):
    __tablename__ = 'issue_comments'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    issue_id = Column(UUID(as_uuid=True), nullable=False)
    author = Column(UUID(as_uuid=True), nullable=False)
    likes = Column(ARRAY(UUID(as_uuid=True)))
    content = Column(String, nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    response_to = Column(UUID(as_uuid=True))
