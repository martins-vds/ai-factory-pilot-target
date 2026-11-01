from datetime import UTC, date, datetime, time

from django.db.models import Prefetch

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord


class DjangoCargoRepository(CargoRepository):
    def upsert(self, cargo: Cargo) -> None:
        delivery = cargo.delivery
        activity = delivery.next_expected_activity
        cargo_record, _ = CargoRecord.objects.update_or_create(
            tracking_id=cargo.tracking_id.value,
            defaults={
                'origin': self._location_record(cargo.origin),
                'spec_origin': self._location_record(cargo.route_specification.origin),
                'spec_destination': self._location_record(cargo.route_specification.destination),
                'spec_arrival_deadline': cargo.route_specification.arrival_deadline.date(),
                'transport_status': delivery.transport_status.value,
                'last_known_location': (
                    self._location_record(delivery.last_known_location)
                    if delivery.last_known_location is not None
                    else None
                ),
                'current_voyage': (
                    self._voyage_record(delivery.current_voyage)
                    if delivery.current_voyage is not None
                    else None
                ),
                'misdirected': delivery.misdirected,
                'eta': delivery.eta.date() if delivery.eta is not None else None,
                'next_expected_handling_event_type': activity.event_type,
                'next_expected_location': (
                    self._location_record(activity.location)
                    if activity.location is not None
                    else None
                ),
                'next_expected_voyage': (
                    self._voyage_record(activity.voyage) if activity.voyage is not None else None
                ),
                'unloaded_at_dest': delivery.unloaded_at_destination,
                'routing_status': delivery.routing_status.value,
                'calculated_at': delivery.calculated_at,
                'last_event_id': delivery.last_event_id,
            },
        )
        for leg in cargo.itinerary.legs:
            LegRecord.objects.update_or_create(
                cargo=cargo_record,
                voyage=self._voyage_record(leg.voyage),
                load_location=self._location_record(leg.load_location),
                unload_location=self._location_record(leg.unload_location),
                defaults={
                    'load_time': leg.load_time,
                    'unload_time': leg.unload_time,
                },
            )

    def find(self, tracking_id: TrackingId) -> Cargo | None:
        record = self._queryset().filter(tracking_id=tracking_id.value).first()
        return self._to_domain(record) if record is not None else None

    def find_all(self) -> list[Cargo]:
        return [self._to_domain(record) for record in self._queryset()]

    @staticmethod
    def _queryset():
        return CargoRecord.objects.select_related(
            'origin',
            'spec_origin',
            'spec_destination',
            'last_known_location',
            'current_voyage',
            'next_expected_location',
            'next_expected_voyage',
        ).prefetch_related(
            Prefetch(
                'legs',
                queryset=LegRecord.objects.select_related(
                    'voyage', 'load_location', 'unload_location'
                ),
            )
        )

    def _to_domain(self, record: CargoRecord) -> Cargo:
        itinerary_legs = tuple(
            Leg(
                self._to_voyage(leg.voyage),
                self._to_location(leg.load_location),
                self._to_location(leg.unload_location),
                leg.load_time,
                leg.unload_time,
            )
            for leg in record.legs.all()
        )
        event_type = record.next_expected_handling_event_type
        location = record.next_expected_location
        voyage = record.next_expected_voyage
        if event_type is None and location is None and voyage is None:
            activity = HandlingActivity.EMPTY
        else:
            activity = HandlingActivity(
                event_type,
                self._to_location(location) if location is not None else None,
                self._to_voyage(voyage) if voyage is not None else None,
            )
        return Cargo(
            tracking_id=TrackingId(record.tracking_id),
            route_specification=RouteSpecification(
                self._to_location(record.spec_origin),
                self._to_location(record.spec_destination),
                self._as_utc_datetime(record.spec_arrival_deadline),
            ),
            delivery=Delivery(
                transport_status=TransportStatus(record.transport_status),
                last_known_location=(
                    self._to_location(record.last_known_location)
                    if record.last_known_location is not None
                    else None
                ),
                current_voyage=(
                    self._to_voyage(record.current_voyage)
                    if record.current_voyage is not None
                    else None
                ),
                misdirected=record.misdirected,
                eta=(self._as_utc_datetime(record.eta) if record.eta is not None else None),
                next_expected_activity=activity,
                unloaded_at_destination=record.unloaded_at_dest,
                routing_status=RoutingStatus(record.routing_status),
                calculated_at=record.calculated_at,
                last_event_id=record.last_event_id,
            ),
            itinerary=Itinerary(itinerary_legs) if itinerary_legs else Itinerary.EMPTY,
            origin=self._to_location(record.origin),
        )

    @staticmethod
    def _as_utc_datetime(value: date | datetime) -> datetime:
        if isinstance(value, datetime):
            return (
                value.astimezone(UTC)
                if value.utcoffset() is not None
                else value.replace(tzinfo=UTC)
            )
        return datetime.combine(value, time.min, tzinfo=UTC)

    @staticmethod
    def _to_location(record) -> Location:
        return Location(UnLocode(record.unlocode), record.name)

    @staticmethod
    def _to_voyage(record) -> Voyage:
        return Voyage(VoyageNumber(record.voyage_number), Schedule.EMPTY)

    @staticmethod
    def _location_record(location: Location) -> LocationRecord:
        return LocationRecord.objects.get(unlocode=location.unlocode.value)

    @staticmethod
    def _voyage_record(voyage: Voyage) -> VoyageRecord:
        return VoyageRecord.objects.get(voyage_number=voyage.voyage_number.value)
