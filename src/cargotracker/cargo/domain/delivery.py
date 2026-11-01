from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from cargotracker.cargo.domain.dates import as_utc
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.location.domain.location import Location
from cargotracker.voyage.domain.voyage import Voyage

if TYPE_CHECKING:
    from cargotracker.handling.domain.handling_event import HandlingEvent
    from cargotracker.handling.domain.handling_history import HandlingHistory


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

    @classmethod
    def derived_from(
        cls,
        route_specification: RouteSpecification,
        itinerary: Itinerary,
        handling_history: 'HandlingHistory',
        calculated_at: datetime | None = None,
    ) -> 'Delivery':
        cls._validate_derivation_inputs(route_specification, itinerary, handling_history)

        latest_event = handling_history.most_recent_event
        misdirected = cls._calculate_misdirection_status(itinerary, latest_event)
        routing_status = cls._calculate_routing_status(route_specification, itinerary)
        transport_status = cls._calculate_transport_status(latest_event)
        on_track = cls._is_on_track(routing_status, misdirected)
        return cls(
            transport_status=transport_status,
            last_known_location=cls._calculate_last_known_location(latest_event),
            current_voyage=cls._calculate_current_voyage(transport_status, latest_event),
            misdirected=misdirected,
            eta=cls._calculate_eta(itinerary, on_track),
            next_expected_activity=cls._calculate_next_expected_activity(
                route_specification, itinerary, latest_event, on_track
            ),
            unloaded_at_destination=cls._calculate_unloaded_at_destination(
                route_specification, latest_event
            ),
            routing_status=routing_status,
            calculated_at=cls._calculate_time(calculated_at),
        )

    @staticmethod
    def _validate_derivation_inputs(
        route_specification: RouteSpecification,
        itinerary: Itinerary,
        handling_history: 'HandlingHistory',
    ) -> None:
        from cargotracker.handling.domain.handling_history import HandlingHistory

        if not isinstance(route_specification, RouteSpecification):
            raise TypeError('A delivery requires a route specification')
        if not isinstance(itinerary, Itinerary):
            raise TypeError('A delivery requires an itinerary')
        if not isinstance(handling_history, HandlingHistory):
            raise TypeError('A delivery requires a handling history')

    @staticmethod
    def _calculate_time(calculated_at: datetime | None) -> datetime:
        return calculated_at if calculated_at is not None else datetime.now(UTC)

    @staticmethod
    def _calculate_last_known_location(latest_event: 'HandlingEvent | None') -> Location | None:
        return latest_event.location if latest_event is not None else None

    @staticmethod
    def _calculate_current_voyage(
        transport_status: TransportStatus, latest_event: 'HandlingEvent | None'
    ) -> Voyage | None:
        return latest_event.voyage if transport_status is TransportStatus.ONBOARD_CARRIER else None

    @staticmethod
    def _is_on_track(routing_status: RoutingStatus, misdirected: bool) -> bool:
        return routing_status is RoutingStatus.ROUTED and not misdirected

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

    @staticmethod
    def _calculate_transport_status(latest_event: 'HandlingEvent | None') -> TransportStatus:
        if latest_event is None:
            return TransportStatus.NOT_RECEIVED
        return {
            'LOAD': TransportStatus.ONBOARD_CARRIER,
            'UNLOAD': TransportStatus.IN_PORT,
            'RECEIVE': TransportStatus.IN_PORT,
            'CUSTOMS': TransportStatus.IN_PORT,
            'CLAIM': TransportStatus.CLAIMED,
        }.get(latest_event.event_type, TransportStatus.UNKNOWN)

    @staticmethod
    def _calculate_misdirection_status(
        itinerary: Itinerary, latest_event: 'HandlingEvent | None'
    ) -> bool:
        return latest_event is not None and not itinerary.is_expected(latest_event)

    @staticmethod
    def _calculate_routing_status(
        route_specification: RouteSpecification, itinerary: Itinerary
    ) -> RoutingStatus:
        if not itinerary.legs:
            return RoutingStatus.NOT_ROUTED
        if route_specification.is_satisfied_by(itinerary):
            return RoutingStatus.ROUTED
        return RoutingStatus.MISROUTED

    @staticmethod
    def _calculate_eta(itinerary: Itinerary, on_track: bool) -> datetime | None:
        return itinerary.legs[-1].unload_time if on_track else None

    @classmethod
    def _calculate_next_expected_activity(
        cls,
        route_specification: RouteSpecification,
        itinerary: Itinerary,
        latest_event: 'HandlingEvent | None',
        on_track: bool,
    ) -> HandlingActivity:
        if not on_track:
            return HandlingActivity.EMPTY
        if latest_event is None:
            return HandlingActivity('RECEIVE', route_specification.origin)
        calculators = {
            'RECEIVE': cls._after_receive,
            'LOAD': cls._after_load,
            'UNLOAD': cls._after_unload,
        }
        calculator = calculators.get(latest_event.event_type)
        return (
            calculator(itinerary, latest_event)
            if calculator is not None
            else HandlingActivity.EMPTY
        )

    @staticmethod
    def _after_receive(itinerary: Itinerary, _latest_event: 'HandlingEvent') -> HandlingActivity:
        first_leg = itinerary.legs[0]
        return HandlingActivity('LOAD', first_leg.load_location, first_leg.voyage)

    @staticmethod
    def _after_load(itinerary: Itinerary, latest_event: 'HandlingEvent') -> HandlingActivity:
        leg = next(
            (leg for leg in itinerary.legs if leg.load_location == latest_event.location),
            None,
        )
        if leg is None:
            return HandlingActivity.EMPTY
        return HandlingActivity('UNLOAD', leg.unload_location, leg.voyage)

    @staticmethod
    def _after_unload(itinerary: Itinerary, latest_event: 'HandlingEvent') -> HandlingActivity:
        for index, leg in enumerate(itinerary.legs):
            if leg.unload_location == latest_event.location:
                if index + 1 < len(itinerary.legs):
                    next_leg = itinerary.legs[index + 1]
                    return HandlingActivity('LOAD', next_leg.load_location, next_leg.voyage)
                return HandlingActivity('CLAIM', leg.unload_location)
        return HandlingActivity.EMPTY

    @staticmethod
    def _calculate_unloaded_at_destination(
        route_specification: RouteSpecification, latest_event: 'HandlingEvent | None'
    ) -> bool:
        return (
            latest_event is not None
            and latest_event.event_type == 'UNLOAD'
            and latest_event.location == route_specification.destination
        )
