"""Synchronous in-process domain events (ADR-002 rules 3 and 4).

A lower module reacts to a higher one by subscribing to an event instead of being called.
Handlers run immediately, in the publisher's transaction, and their return values are given
back to the publisher (the return flow needs the generated maintenance alerts).

    # maintenance/events.py
    bus.subscribe(TripCompleted, on_trip_completed)

    # handover/service.py
    alerts = bus.publish(TripCompleted(vehicle_id=..., odometer_km=..., session=session))
"""

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class DomainEvent:
    """Marker base class. Concrete events are frozen dataclasses defined by the publishing module."""


Handler = Callable[[Any], Any]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: type[DomainEvent], handler: Handler) -> None:
        if handler not in self._handlers[event_type]:
            self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> list[Any]:
        """Call every handler in subscription order; an exception aborts the whole request."""
        return [handler(event) for handler in self._handlers[type(event)]]

    def clear(self) -> None:
        self._handlers.clear()


bus = EventBus()
