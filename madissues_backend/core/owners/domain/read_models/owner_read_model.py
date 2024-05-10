from pydantic import BaseModel

from madissues_backend.core.owners.domain.owner import Owner


class OwnerReadModel(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone_number: str

    @staticmethod
    def of(owner: Owner) -> "OwnerReadModel":
        return OwnerReadModel(
            id=str(owner.id),
            email=owner.email,
            first_name=owner.first_name,
            last_name=owner.last_name,
            phone_number=owner.phone_number
        )


