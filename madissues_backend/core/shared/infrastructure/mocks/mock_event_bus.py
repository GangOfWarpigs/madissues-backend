from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.application.event_handler import EventHandler
from madissues_backend.core.shared.domain.events import DomainEvent


class MockEventBus(EventBus):

    handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, handler: EventHandler):
        self.handlers.setdefault(handler.event_name, []).append(handler)

    def notify(self, event: DomainEvent):
        for handler in self.handlers.get(event.name, []):
            handler.handle(event)

    def notify_all(self, events: list[DomainEvent]):
        for event in events:
            self.notify(event)
