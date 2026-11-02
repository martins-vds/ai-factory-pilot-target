import calendar
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, time, timedelta

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEvent, HandlingEventType
from cargotracker.handling.domain.handling_history import HandlingHistory
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
    legs: tuple[_LegSeed, ...]
    events: tuple[_EventSeed, ...]
    deadline_days: int | None = None
    deadline_months: int | None = None


SAMPLE_CARGOS = (
    _CargoSeed(
        'ABC123',
        'CNHKG',
        'FIHEL',
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
    ),
    _CargoSeed(
        'JKL567',
        'CNHGH',
        'SESTO',
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
    ),
    _CargoSeed(
        'DEF789',
        'CNHKG',
        'AUMEL',
        (),
        (),
        deadline_months=2,
    ),
    _CargoSeed(
        'MNO456',
        'USNYC',
        'USDAL',
        (_LegSeed('0200T', 'USNYC', 'USDAL', -34, -28),),
        (
            _EventSeed(HandlingEventType.RECEIVE, 'USNYC', None, -37),
            _EventSeed(HandlingEventType.LOAD, 'USNYC', '0200T', -34),
            _EventSeed(HandlingEventType.UNLOAD, 'USDAL', '0200T', -28),
            _EventSeed(HandlingEventType.CUSTOMS, 'USDAL', None, -27),
            _EventSeed(HandlingEventType.CLAIM, 'USDAL', None, -26),
        ),
        deadline_days=-24,
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
    route_specification = RouteSpecification(
        locations[seed.origin],
        locations[seed.destination],
        datetime.combine(deadline, time.min, tzinfo=UTC),
    )
    itinerary = Itinerary(itinerary_legs) if itinerary_legs else Itinerary.EMPTY
    return Cargo(
        tracking_id=TrackingId(seed.tracking_id),
        route_specification=route_specification,
        delivery=Delivery.derived_from(
            route_specification,
            itinerary,
            HandlingHistory.EMPTY,
            calculated_at,
        ),
        itinerary=itinerary,
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
            history = self._handling_events.lookup_handling_history_of_cargo(cargo.tracking_id)
            cargo.delivery = replace(
                Delivery.derived_from(
                    cargo.route_specification,
                    cargo.itinerary,
                    history,
                    calculated_at,
                ),
                last_event_id=last_event_id,
            )
            self._cargos.upsert(cargo)
