from madissues_backend.core.shared.application.event_bus import EventBus
from madissues_backend.core.shared.application.event_handler import EventHandler
from madissues_backend.core.shared.domain.events import DomainEvent


class MockEventBus(EventBus):
    handlers: dict[str, list[EventHandler]]
    events: list[DomainEvent]

    def __init__(self):
        self.handlers = {}
        self.events = []

    def subscribe(self, handler: EventHandler):
        self.handlers.setdefault(handler.event_name, []).append(handler)

    def notify(self, event: DomainEvent):
        for handler in self.handlers.get(event.name, []):
            handler.handle(event.payload)
        # FIXME: borra el evento de la lista pero lo añade a un archivo llamado events.txt, EventSourcing

    def notify_all(self, events: list[DomainEvent]):
        for event in events:
            self.notify(event)
            self.events.append(event)
