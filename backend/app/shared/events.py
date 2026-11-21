"""Synchronous in-process domain events (ADR-002 rules 3 and 4, docs/domain_events.md).

A lower module reacts to a higher one by subscribing to an event instead of being called.
Handlers run immediately, in the publisher's transaction, and their return values are given
back to the publisher (the return flow needs the maintenance evaluation result).

    # maintenance/events.py
    bus.subscribe(TripCompletedEvent, on_trip_completed)

    # handover/service.py
    [result] = bus.publish(TripCompletedEvent(reservation_id=..., vehicle_id=..., odometer_km=...,
                                              trip_km=..., severe_damage_reported=False))
"""

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    """Base class of every domain event (docs/domain_events.md §1).

    Adds `event_id` and `occurred_at` (timezone-aware UTC). Subclasses are
    `@dataclass(frozen=True, kw_only=True)` defined in the publishing module's events.py.
    """

    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


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
