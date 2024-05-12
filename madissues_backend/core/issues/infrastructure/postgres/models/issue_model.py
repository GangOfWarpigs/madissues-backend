from datetime import datetime

from sqlalchemy import Column, String, DateTime, ARRAY, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Definir la clase para la tabla Issue
class PostgresIssueModel(Base):
    __tablename__ = 'issues'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String(length=80), nullable=False)
    description = Column(String, nullable=False)
    details = Column(String(length=1000), nullable=False)
    proofs = Column(ARRAY(String))
    status = Column(String(length=20), nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    course = Column(UUID(as_uuid=True), nullable=False)
    teachers = Column(ARRAY(UUID(as_uuid=True)))
    student_id = Column(UUID(as_uuid=True), nullable=False)
    organization_id = Column(UUID(as_uuid=True), nullable=False)

