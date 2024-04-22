
from abc import ABC, abstractmethod
from madissues_backend.core.shared.domain.events import DomainEvent

class EventBus(ABC):
    @abstractmethod
    def subscribe(self, handler):
        pass

    @abstractmethod
    def notify(self, event : DomainEvent):
        pass

    @abstractmethod
    def notify_all(self, events : list[DomainEvent]):
        pass