from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from madissues_backend.core.faqs.domain.faq import Faq
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.shared.infrastructure.postgres.postgres_dependencies import Base


class PostgresFaq(Base):
    __tablename__ = 'faqs'
    __table_args__ = {'schema': 'backend'}

    id = Column(UUID(as_uuid=True), primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    organization_id = Column(UUID(as_uuid=True), ForeignKey('backend.organizations.id'), nullable=False)

    # Relación inversa con la organización
    organization = relationship("PostgresOrganization", back_populates="faqs")

    @classmethod
    def from_entity(cls, faq: Faq):
        return cls(
            id=faq.id,
            question=faq.question,
            answer=faq.answer,
            organization_id=faq.organization_id
        )

    def to_entity(self):
        return Faq(
            id=GenericUUID(str(self.id)),
            question=self.question,
            answer=self.answer,
            organization_id=GenericUUID(str(self.organization_id))
        )
