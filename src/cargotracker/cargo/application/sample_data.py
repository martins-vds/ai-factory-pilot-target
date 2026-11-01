import calendar
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, time, timedelta

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEvent, HandlingEventType
from cargotracker.handling.domain.repository import HandlingEventRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.repository import LocationRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.repository import VoyageRepository
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber

LOCATIONS = (
    ('CNHKG', 'Hong Kong'),
    ('AUMEL', 'Melbourne'),
    ('SESTO', 'Stockholm'),
    ('FIHEL', 'Helsinki'),
    ('USCHI', 'Chicago'),
    ('JNTKO', 'Tokyo'),
    ('DEHAM', 'Hamburg'),
    ('CNSHA', 'Shanghai'),
    ('NLRTM', 'Rotterdam'),
    ('SEGOT', 'Gothenburg'),
    ('CNHGH', 'Hangzhou'),
    ('USNYC', 'New York'),
    ('USDAL', 'Dallas'),
)
VOYAGES = ('0100S', '0200T', '0300A', '0400S', '0301S')


@dataclass(frozen=True)
class _LegSeed:
    voyage: str
    load_location: str
    unload_location: str
    load_offset: int
    unload_offset: int


@dataclass(frozen=True)
class _EventSeed:
    event_type: HandlingEventType
    location: str
    voyage: str | None
    completion_offset: int


@dataclass(frozen=True)
class _CargoSeed:
    tracking_id: str
    origin: str
    destination: str
    transport_status: TransportStatus
    routing_status: RoutingStatus
    legs: tuple[_LegSeed, ...]
    events: tuple[_EventSeed, ...]
    deadline_days: int | None = None
    deadline_months: int | None = None
    last_known_location: str | None = None
    current_voyage: str | None = None
    misdirected: bool = False
    eta_days: int | None = None
    next_activity: tuple[HandlingEventType, str, str] | None = None
    unloaded_at_destination: bool = False


SAMPLE_CARGOS = (
    _CargoSeed(
        'ABC123',
        'CNHKG',
        'FIHEL',
        TransportStatus.IN_PORT,
        RoutingStatus.ROUTED,
        (
            _LegSeed('0100S', 'CNHKG', 'USNYC', -7, -1),
            _LegSeed('0200T', 'USNYC', 'USDAL', 2, 6),
            _LegSeed('0300A', 'USDAL', 'FIHEL', 8, 14),
        ),
        (
            _EventSeed(HandlingEventType.RECEIVE, 'CNHKG', None, -10),
            _EventSeed(HandlingEventType.LOAD, 'CNHKG', '0100S', -7),
            _EventSeed(HandlingEventType.UNLOAD, 'USNYC', '0100S', -1),
        ),
        deadline_days=15,
        last_known_location='USNYC',
        eta_days=14,
        next_activity=(HandlingEventType.LOAD, 'USNYC', '0200T'),
    ),
    _CargoSeed(
        'JKL567',
        'CNHGH',
        'SESTO',
        TransportStatus.ONBOARD_CARRIER,
        RoutingStatus.ROUTED,
        (
            _LegSeed('0100S', 'CNHGH', 'USNYC', -10, -3),
            _LegSeed('0200T', 'USNYC', 'USDAL', -2, 2),
            _LegSeed('0300A', 'USDAL', 'SESTO', 6, 15),
        ),
        (
            _EventSeed(HandlingEventType.RECEIVE, 'CNHGH', None, -15),
            _EventSeed(HandlingEventType.LOAD, 'CNHGH', '0100S', -10),
            _EventSeed(HandlingEventType.UNLOAD, 'USNYC', '0100S', -3),
            _EventSeed(HandlingEventType.LOAD, 'USNYC', '0100S', -2),
        ),
        deadline_days=18,
        last_known_location='USNYC',
        current_voyage='0100S',
        misdirected=True,
    ),
    _CargoSeed(
        'DEF789',
        'CNHKG',
        'AUMEL',
        TransportStatus.NOT_RECEIVED,
        RoutingStatus.NOT_ROUTED,
        (),
        (),
        deadline_months=2,
    ),
    _CargoSeed(
        'MNO456',
        'USNYC',
        'USDAL',
        TransportStatus.CLAIMED,
        RoutingStatus.ROUTED,
        (_LegSeed('0200T', 'USNYC', 'USDAL', -34, -28),),
        (
            _EventSeed(HandlingEventType.RECEIVE, 'USNYC', None, -37),
            _EventSeed(HandlingEventType.LOAD, 'USNYC', '0200T', -34),
            _EventSeed(HandlingEventType.UNLOAD, 'USDAL', '0200T', -28),
            _EventSeed(HandlingEventType.CUSTOMS, 'USDAL', None, -27),
            _EventSeed(HandlingEventType.CLAIM, 'USDAL', None, -26),
        ),
        deadline_days=-24,
        last_known_location='USDAL',
        eta_days=-28,
        unloaded_at_destination=True,
    ),
)


def _add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    return value.replace(
        year=year,
        month=month,
        day=min(value.day, calendar.monthrange(year, month)[1]),
    )


def _at_day_offset(today: date, offset: int) -> datetime:
    return datetime.combine(today + timedelta(days=offset), time.min, tzinfo=UTC)


def _cargo_from_seed(seed, locations, voyages, today, calculated_at):
    deadline = (
        _add_months(today, seed.deadline_months)
        if seed.deadline_months is not None
        else today + timedelta(days=seed.deadline_days)
    )
    itinerary_legs = tuple(
        Leg(
            voyages[leg.voyage],
            locations[leg.load_location],
            locations[leg.unload_location],
            _at_day_offset(today, leg.load_offset),
            _at_day_offset(today, leg.unload_offset),
        )
        for leg in seed.legs
    )
    next_activity = (
        HandlingActivity(
            seed.next_activity[0].value,
            locations[seed.next_activity[1]],
            voyages[seed.next_activity[2]],
        )
        if seed.next_activity is not None
        else HandlingActivity.EMPTY
    )
    return Cargo(
        tracking_id=TrackingId(seed.tracking_id),
        route_specification=RouteSpecification(
            locations[seed.origin],
            locations[seed.destination],
            datetime.combine(deadline, time.min, tzinfo=UTC),
        ),
        delivery=Delivery(
            transport_status=seed.transport_status,
            last_known_location=locations.get(seed.last_known_location),
            current_voyage=voyages.get(seed.current_voyage),
            misdirected=seed.misdirected,
            eta=(_at_day_offset(today, seed.eta_days) if seed.eta_days is not None else None),
            next_expected_activity=next_activity,
            unloaded_at_destination=seed.unloaded_at_destination,
            routing_status=seed.routing_status,
            calculated_at=calculated_at,
        ),
        itinerary=Itinerary(itinerary_legs) if itinerary_legs else Itinerary.EMPTY,
    )


class SampleDataSeeder:
    def __init__(
        self,
        locations: LocationRepository,
        voyages: VoyageRepository,
        cargos: CargoRepository,
        handling_events: HandlingEventRepository,
    ):
        self._locations = locations
        self._voyages = voyages
        self._cargos = cargos
        self._handling_events = handling_events

    def seed(self, today: date) -> None:
        locations = {code: Location(UnLocode(code), name) for code, name in LOCATIONS}
        voyages = {number: Voyage(VoyageNumber(number), Schedule.EMPTY) for number in VOYAGES}
        for location in locations.values():
            self._locations.upsert(location)
        for voyage in voyages.values():
            self._voyages.upsert(voyage)
        self._seed_cargos(locations, voyages, today, datetime.now(UTC))

    def _seed_cargos(self, locations, voyages, today, calculated_at):
        registration_time = datetime.now(UTC)
        for seed in SAMPLE_CARGOS:
            cargo = _cargo_from_seed(seed, locations, voyages, today, calculated_at)
            self._cargos.upsert(cargo)
            last_event_id = None
            for event_seed in seed.events:
                event = HandlingEvent(
                    cargo,
                    _at_day_offset(today, event_seed.completion_offset),
                    registration_time,
                    event_seed.event_type,
                    locations[event_seed.location],
                    voyages.get(event_seed.voyage),
                )
                last_event_id = self._handling_events.upsert(event)
            if last_event_id is not None:
                cargo.delivery = replace(cargo.delivery, last_event_id=last_event_id)
                self._cargos.upsert(cargo)
