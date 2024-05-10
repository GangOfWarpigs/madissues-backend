from abc import ABC, abstractmethod

from madissues_backend.core.owners.domain.read_models.owner_read_model import OwnerReadModel


class OwnerQueryRepository(ABC):
    @abstractmethod
    def get_owner_profile(self, id : str) -> OwnerReadModel:
        ...