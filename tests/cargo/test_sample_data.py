from dataclasses import fields, replace
from datetime import UTC, date, datetime, timedelta

import pytest
from django.core.management import call_command

from cargotracker.cargo.application.sample_data import SAMPLE_CARGOS, SampleDataSeeder
from cargotracker.cargo.domain.delivery import Delivery, TransportStatus
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository
from cargotracker.voyage.infrastructure.models import VoyageRecord


def test_sample_cargo_definitions_do_not_include_delivery_snapshots():
    delivery_snapshot_fields = {
        'transport_status',
        'routing_status',
        'last_known_location',
        'current_voyage',
        'misdirected',
        'eta_days',
        'next_activity',
        'unloaded_at_destination',
    }

    assert delivery_snapshot_fields.isdisjoint(field.name for field in fields(SAMPLE_CARGOS[0]))


@pytest.mark.django_db
def test_seeded_deliveries_match_their_handling_histories():
    call_command('seed_sample_data')
    cargo_repository = DjangoCargoRepository()
    handling_event_repository = DjangoHandlingEventRepository()

    for seed in SAMPLE_CARGOS:
        cargo = cargo_repository.find(TrackingId(seed.tracking_id))
        history = handling_event_repository.lookup_handling_history_of_cargo(cargo.tracking_id)
        derived_delivery = Delivery.derived_from(
            cargo.route_specification,
            cargo.itinerary,
            history,
            calculated_at=cargo.delivery.calculated_at,
        )

        assert (
            replace(derived_delivery, last_event_id=cargo.delivery.last_event_id) == cargo.delivery
        )


@pytest.mark.django_db
def test_seed_sample_data_is_idempotent_and_supports_golden_lookups():
    call_command('seed_sample_data')
    for event in HandlingEventRecord.objects.all():
        event.completion_time -= timedelta(days=1)
        event.save(update_fields=['completion_time'])
    for leg in LegRecord.objects.all():
        leg.load_time -= timedelta(days=1)
        leg.unload_time -= timedelta(days=1)
        leg.save(update_fields=['load_time', 'unload_time'])
    call_command('seed_sample_data')

    today = datetime.now(UTC).date()
    assert LocationRecord.objects.count() == 13
    assert VoyageRecord.objects.count() == 5
    assert CargoRecord.objects.count() == 4
    assert LegRecord.objects.count() == 7
    assert HandlingEventRecord.objects.count() == 12
    assert set(LocationRecord.objects.values_list('unlocode', 'name')) == {
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
    }
    assert set(VoyageRecord.objects.values_list('voyage_number', flat=True)) == {
        '0100S',
        '0200T',
        '0300A',
        '0400S',
        '0301S',
    }

    cargos = {
        tracking_id: DjangoCargoRepository().find(TrackingId(tracking_id))
        for tracking_id in ('ABC123', 'JKL567', 'DEF789', 'MNO456')
    }
    assert all(cargo is not None for cargo in cargos.values())
    assert cargos['MNO456'].delivery.unloaded_at_destination is False

    expected_cargo_data = {
        'ABC123': ('CNHKG', 'FIHEL', TransportStatus.IN_PORT, False, 14),
        'JKL567': ('CNHGH', 'SESTO', TransportStatus.ONBOARD_CARRIER, True, None),
        'DEF789': ('CNHKG', 'AUMEL', TransportStatus.NOT_RECEIVED, False, None),
        'MNO456': ('USNYC', 'USDAL', TransportStatus.CLAIMED, False, -28),
    }
    for tracking_id, (
        origin,
        destination,
        status,
        misdirected,
        eta_offset,
    ) in expected_cargo_data.items():
        cargo = cargos[tracking_id]
        assert cargo.route_specification.origin.unlocode.value == origin
        assert cargo.route_specification.destination.unlocode.value == destination
        assert cargo.delivery.transport_status is status
        assert cargo.delivery.misdirected is misdirected
        assert cargo.delivery.eta == (
            datetime.combine(today + timedelta(days=eta_offset), datetime.min.time(), tzinfo=UTC)
            if eta_offset is not None
            else None
        )

    expected_itineraries = {
        'ABC123': [
            ('0100S', 'CNHKG', 'USNYC', -7, -1),
            ('0200T', 'USNYC', 'USDAL', 2, 6),
            ('0300A', 'USDAL', 'FIHEL', 8, 14),
        ],
        'JKL567': [
            ('0100S', 'CNHGH', 'USNYC', -10, -3),
            ('0200T', 'USNYC', 'USDAL', -2, 2),
            ('0300A', 'USDAL', 'SESTO', 6, 15),
        ],
        'DEF789': [],
        'MNO456': [('0200T', 'USNYC', 'USDAL', -34, -28)],
    }
    for tracking_id, expected_legs in expected_itineraries.items():
        assert [
            (
                leg.voyage.voyage_number.value,
                leg.load_location.unlocode.value,
                leg.unload_location.unlocode.value,
                (leg.load_time.date() - today).days,
                (leg.unload_time.date() - today).days,
            )
            for leg in cargos[tracking_id].itinerary.legs
        ] == expected_legs

    expected_histories = {
        'ABC123': [
            (HandlingEventType.RECEIVE, 'CNHKG', None, -10),
            (HandlingEventType.LOAD, 'CNHKG', '0100S', -7),
            (HandlingEventType.UNLOAD, 'USNYC', '0100S', -1),
        ],
        'JKL567': [
            (HandlingEventType.RECEIVE, 'CNHGH', None, -15),
            (HandlingEventType.LOAD, 'CNHGH', '0100S', -10),
            (HandlingEventType.UNLOAD, 'USNYC', '0100S', -3),
            (HandlingEventType.LOAD, 'USNYC', '0100S', -2),
        ],
        'DEF789': [],
        'MNO456': [
            (HandlingEventType.RECEIVE, 'USNYC', None, -37),
            (HandlingEventType.LOAD, 'USNYC', '0200T', -34),
            (HandlingEventType.UNLOAD, 'USDAL', '0200T', -28),
            (HandlingEventType.CUSTOMS, 'USDAL', None, -27),
            (HandlingEventType.CLAIM, 'USDAL', None, -26),
        ],
    }
    for tracking_id, expected_events in expected_histories.items():
        history = DjangoHandlingEventRepository().lookup_handling_history_of_cargo(
            TrackingId(tracking_id)
        )
        assert [
            (
                event.event_type,
                event.location.unlocode.value,
                event.voyage.voyage_number.value if event.voyage else None,
                event.completion_time.date(),
            )
            for event in history.events
        ] == [
            (event_type, location, voyage, today + timedelta(days=offset))
            for event_type, location, voyage, offset in expected_events
        ]
        latest_event = (
            HandlingEventRecord.objects.filter(cargo__tracking_id=tracking_id)
            .order_by('completion_time')
            .last()
        )
        assert cargos[tracking_id].delivery.last_event_id == (
            latest_event.pk if latest_event else None
        )


@pytest.mark.django_db
def test_month_based_deadline_rolls_over_leap_year_and_clamps_to_month_end():
    SampleDataSeeder(
        DjangoLocationRepository(),
        DjangoVoyageRepository(),
        DjangoCargoRepository(),
        DjangoHandlingEventRepository(),
    ).seed(date(2023, 12, 31))

    cargo = DjangoCargoRepository().find(TrackingId('DEF789'))

    assert cargo is not None
    assert cargo.route_specification.arrival_deadline == datetime(2024, 2, 29, tzinfo=UTC)
