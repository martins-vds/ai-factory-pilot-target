from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from cargotracker.cargo.domain.dates import as_utc
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.location.domain.location import Location
from cargotracker.voyage.domain.voyage import Voyage


class TransportStatus(StrEnum):
    NOT_RECEIVED = 'NOT_RECEIVED'
    IN_PORT = 'IN_PORT'
    ONBOARD_CARRIER = 'ONBOARD_CARRIER'
    CLAIMED = 'CLAIMED'
    UNKNOWN = 'UNKNOWN'


class RoutingStatus(StrEnum):
    NOT_ROUTED = 'NOT_ROUTED'
    ROUTED = 'ROUTED'
    MISROUTED = 'MISROUTED'


@dataclass(frozen=True)
class Delivery:
    transport_status: TransportStatus
    last_known_location: Location | None
    current_voyage: Voyage | None
    misdirected: bool
    eta: datetime | None
    next_expected_activity: HandlingActivity
    unloaded_at_destination: bool
    routing_status: RoutingStatus
    calculated_at: datetime
    last_event_id: int | None = None

    def __post_init__(self):
        if not isinstance(self.transport_status, TransportStatus):
            raise TypeError('A delivery requires a transport status')
        if self.last_known_location is not None and not isinstance(
            self.last_known_location, Location
        ):
            raise TypeError('A delivery last-known location must be a location')
        if self.current_voyage is not None and not isinstance(self.current_voyage, Voyage):
            raise TypeError('A delivery current voyage must be a voyage')
        if not isinstance(self.misdirected, bool):
            raise TypeError('A delivery misdirected flag must be a boolean')
        if self.eta is not None:
            object.__setattr__(self, 'eta', as_utc(self.eta, 'ETA'))
        if not isinstance(self.next_expected_activity, HandlingActivity):
            raise TypeError('A delivery requires a next expected activity')
        if not isinstance(self.unloaded_at_destination, bool):
            raise TypeError('A delivery unloaded-at-destination flag must be a boolean')
        if not isinstance(self.routing_status, RoutingStatus):
            raise TypeError('A delivery requires a routing status')
        object.__setattr__(self, 'calculated_at', as_utc(self.calculated_at, 'calculated time'))
        if self.last_event_id is not None and (
            not isinstance(self.last_event_id, int) or isinstance(self.last_event_id, bool)
        ):
            raise TypeError('A delivery last event ID must be an integer')
