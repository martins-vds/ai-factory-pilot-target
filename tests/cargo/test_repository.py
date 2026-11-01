from datetime import UTC, date, datetime

import pytest
from django.db import connection, models

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery, RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord


@pytest.mark.django_db
def test_cargo_and_leg_schema_matches_source_jpa_tables_and_relations():
    with connection.cursor() as cursor:
        cargo_columns = [
            column.name
            for column in connection.introspection.get_table_description(cursor, 'cargo')
        ]
        leg_columns = [
            column.name for column in connection.introspection.get_table_description(cursor, 'leg')
        ]

    assert set(cargo_columns) == {
        'id',
        'tracking_id',
        'origin_id',
        'spec_origin_id',
        'spec_destination_id',
        'spec_arrival_deadline',
        'transport_status',
        'last_known_location_id',
        'current_voyage_id',
        'misdirected',
        'eta',
        'next_expected_handling_event_type',
        'next_expected_location_id',
        'next_expected_voyage_id',
        'unloaded_at_dest',
        'routing_status',
        'calculated_at',
        'last_event_id',
    }
    assert set(leg_columns) == {
        'id',
        'cargo_id',
        'voyage_id',
        'load_location_id',
        'unload_location_id',
        'load_time',
        'unload_time',
    }
    assert CargoRecord._meta.db_table == 'cargo'
    assert CargoRecord._meta.get_field('tracking_id').unique
    assert {
        field: CargoRecord._meta.get_field(field).max_length
        for field in (
            'tracking_id',
            'transport_status',
            'next_expected_handling_event_type',
            'routing_status',
        )
    } == {
        'tracking_id': 255,
        'transport_status': 255,
        'next_expected_handling_event_type': 255,
        'routing_status': 255,
    }
    assert CargoRecord._meta.get_field('spec_arrival_deadline').get_internal_type() == 'DateField'
    assert CargoRecord._meta.get_field('eta').get_internal_type() == 'DateField'
    assert CargoRecord._meta.get_field('calculated_at').get_internal_type() == 'DateTimeField'
    expected_cargo_relations = {
        'origin': ('origin_id', LocationRecord),
        'spec_origin': ('spec_origin_id', LocationRecord),
        'spec_destination': ('spec_destination_id', LocationRecord),
        'last_known_location': ('last_known_location_id', LocationRecord),
        'current_voyage': ('current_voyage_id', VoyageRecord),
        'last_event': ('last_event_id', HandlingEventRecord),
        'next_expected_location': ('next_expected_location_id', LocationRecord),
        'next_expected_voyage': ('next_expected_voyage_id', VoyageRecord),
    }
    for field_name, (db_column, related_model) in expected_cargo_relations.items():
        field = CargoRecord._meta.get_field(field_name)
        assert field.db_column == db_column
        assert field.remote_field.model is related_model
        assert field.remote_field.on_delete is models.PROTECT
    assert {
        field: CargoRecord._meta.get_field(field).null
        for field in (
            'last_known_location',
            'current_voyage',
            'eta',
            'last_event',
            'next_expected_handling_event_type',
            'next_expected_location',
            'next_expected_voyage',
        )
    } == {
        'last_known_location': True,
        'current_voyage': True,
        'eta': True,
        'last_event': True,
        'next_expected_handling_event_type': True,
        'next_expected_location': True,
        'next_expected_voyage': True,
    }
    assert LegRecord._meta.db_table == 'leg'
    expected_leg_relations = {
        'cargo': ('cargo_id', CargoRecord),
        'voyage': ('voyage_id', VoyageRecord),
        'load_location': ('load_location_id', LocationRecord),
        'unload_location': ('unload_location_id', LocationRecord),
    }
    for field_name, (db_column, related_model) in expected_leg_relations.items():
        field = LegRecord._meta.get_field(field_name)
        assert field.db_column == db_column
        assert field.remote_field.model is related_model
        on_delete = models.CASCADE if field_name == 'cargo' else models.PROTECT
        assert field.remote_field.on_delete is on_delete
    assert LegRecord._meta.ordering == ('load_time',)


@pytest.mark.django_db
def test_repository_reads_cargo_embedded_fields_and_legs_by_tracking_id():
    origin_record = LocationRecord.objects.create(unlocode='USNYC', name='New York')
    destination_record = LocationRecord.objects.create(unlocode='FIHEL', name='Helsinki')
    last_known_record = LocationRecord.objects.create(unlocode='NLRTM', name='Rotterdam')
    voyage_record = VoyageRecord.objects.create(voyage_number='CM001')
    cargo_record = CargoRecord.objects.create(
        tracking_id='ABC123',
        origin=origin_record,
        spec_origin=origin_record,
        spec_destination=destination_record,
        spec_arrival_deadline=date(2026, 11, 12),
        transport_status='ONBOARD_CARRIER',
        last_known_location=last_known_record,
        current_voyage=voyage_record,
        misdirected=True,
        eta=date(2026, 11, 12),
        next_expected_handling_event_type='UNLOAD',
        next_expected_location=destination_record,
        next_expected_voyage=voyage_record,
        unloaded_at_dest=False,
        routing_status='MISROUTED',
        calculated_at=datetime(2026, 11, 1, 10, tzinfo=UTC),
    )
    LegRecord.objects.create(
        cargo=cargo_record,
        voyage=voyage_record,
        load_location=last_known_record,
        unload_location=destination_record,
        load_time=datetime(2026, 11, 3, 10, tzinfo=UTC),
        unload_time=datetime(2026, 11, 4, 10, tzinfo=UTC),
    )
    LegRecord.objects.create(
        cargo=cargo_record,
        voyage=voyage_record,
        load_location=origin_record,
        unload_location=last_known_record,
        load_time=datetime(2026, 11, 1, 10, tzinfo=UTC),
        unload_time=datetime(2026, 11, 2, 10, tzinfo=UTC),
    )
    last_event = HandlingEventRecord.objects.create(
        cargo=cargo_record,
        location=last_known_record,
        voyage=voyage_record,
        event_type='UNLOAD',
        completion_time=date(2026, 11, 2),
        registration_time=date(2026, 11, 2),
    )
    cargo_record.last_event = last_event
    cargo_record.save(update_fields=['last_event'])

    cargo = DjangoCargoRepository().find(TrackingId('ABC123'))

    assert cargo == Cargo(
        tracking_id=TrackingId('ABC123'),
        route_specification=RouteSpecification(
            Location(UnLocode('USNYC'), 'New York'),
            Location(UnLocode('FIHEL'), 'Helsinki'),
            datetime(2026, 11, 12, tzinfo=UTC),
        ),
        delivery=Delivery(
            transport_status=TransportStatus.ONBOARD_CARRIER,
            last_known_location=Location(UnLocode('NLRTM'), 'Rotterdam'),
            current_voyage=Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
            misdirected=True,
            eta=datetime(2026, 11, 12, tzinfo=UTC),
            next_expected_activity=HandlingActivity(
                'UNLOAD',
                Location(UnLocode('FIHEL'), 'Helsinki'),
                Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
            ),
            unloaded_at_destination=False,
            routing_status=RoutingStatus.MISROUTED,
            calculated_at=datetime(2026, 11, 1, 10, tzinfo=UTC),
            last_event_id=last_event.pk,
        ),
        itinerary=Itinerary(
            (
                Leg(
                    Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
                    Location(UnLocode('USNYC'), 'New York'),
                    Location(UnLocode('NLRTM'), 'Rotterdam'),
                    datetime(2026, 11, 1, 10, tzinfo=UTC),
                    datetime(2026, 11, 2, 10, tzinfo=UTC),
                ),
                Leg(
                    Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
                    Location(UnLocode('NLRTM'), 'Rotterdam'),
                    Location(UnLocode('FIHEL'), 'Helsinki'),
                    datetime(2026, 11, 3, 10, tzinfo=UTC),
                    datetime(2026, 11, 4, 10, tzinfo=UTC),
                ),
            )
        ),
        origin=Location(UnLocode('USNYC'), 'New York'),
    )
    assert cargo.origin == Location(UnLocode('USNYC'), 'New York')
    assert cargo.route_specification.origin == Location(UnLocode('USNYC'), 'New York')
    assert cargo.route_specification.destination == Location(UnLocode('FIHEL'), 'Helsinki')
    assert cargo.route_specification.arrival_deadline == datetime(2026, 11, 12, tzinfo=UTC)
    assert cargo.delivery.transport_status is TransportStatus.ONBOARD_CARRIER
    assert cargo.delivery.last_known_location == Location(UnLocode('NLRTM'), 'Rotterdam')
    assert cargo.delivery.current_voyage == Voyage(VoyageNumber('CM001'), Schedule.EMPTY)
    assert cargo.delivery.misdirected
    assert cargo.delivery.eta == datetime(2026, 11, 12, tzinfo=UTC)
    assert cargo.delivery.next_expected_activity == HandlingActivity(
        'UNLOAD',
        Location(UnLocode('FIHEL'), 'Helsinki'),
        Voyage(VoyageNumber('CM001'), Schedule.EMPTY),
    )
    assert not cargo.delivery.unloaded_at_destination
    assert cargo.delivery.routing_status is RoutingStatus.MISROUTED
    assert cargo.delivery.calculated_at == datetime(2026, 11, 1, 10, tzinfo=UTC)
    assert cargo.delivery.last_event_id == last_event.pk
    assert [leg.load_time for leg in cargo.itinerary.legs] == [
        datetime(2026, 11, 1, 10, tzinfo=UTC),
        datetime(2026, 11, 3, 10, tzinfo=UTC),
    ]
    assert cargo.itinerary.legs[0].load_location == Location(UnLocode('USNYC'), 'New York')
    assert cargo.itinerary.legs[0].unload_location == Location(UnLocode('NLRTM'), 'Rotterdam')
    assert cargo.itinerary.legs[0].voyage == Voyage(VoyageNumber('CM001'), Schedule.EMPTY)
    assert DjangoCargoRepository().find_all() == [cargo]


@pytest.mark.django_db
def test_repository_returns_none_for_unknown_tracking_id():
    assert DjangoCargoRepository().find(TrackingId('NOPE000')) is None


@pytest.mark.django_db
def test_repository_maps_cargo_without_optional_delivery_relations_or_legs():
    origin = LocationRecord.objects.create(unlocode='USNYC', name='New York')
    destination = LocationRecord.objects.create(unlocode='FIHEL', name='Helsinki')
    CargoRecord.objects.create(
        tracking_id='DEF789',
        origin=origin,
        spec_origin=origin,
        spec_destination=destination,
        spec_arrival_deadline=date(2026, 11, 12),
        transport_status='NOT_RECEIVED',
        misdirected=False,
        unloaded_at_dest=False,
        routing_status='NOT_ROUTED',
        calculated_at=datetime(2026, 11, 1, tzinfo=UTC),
    )

    cargo = DjangoCargoRepository().find(TrackingId('DEF789'))

    assert cargo is not None
    assert cargo.delivery.last_known_location is None
    assert cargo.delivery.current_voyage is None
    assert cargo.delivery.eta is None
    assert cargo.delivery.next_expected_activity is HandlingActivity.EMPTY
    assert cargo.delivery.last_event_id is None
    assert cargo.itinerary is Itinerary.EMPTY
