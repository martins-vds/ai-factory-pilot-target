import calendar
from datetime import UTC, datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.infrastructure.models import VoyageRecord

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
SAMPLE_CARGOS = (
    {
        'tracking_id': 'ABC123',
        'origin': 'CNHKG',
        'destination': 'FIHEL',
        'deadline_days': 15,
        'transport_status': 'IN_PORT',
        'last_known_location': 'USNYC',
        'misdirected': False,
        'eta_days': 14,
        'routing_status': 'ROUTED',
        'next_expected': ('LOAD', 'USNYC', '0200T'),
        'legs': (
            ('0100S', 'CNHKG', 'USNYC', -7, -1),
            ('0200T', 'USNYC', 'USDAL', 2, 6),
            ('0300A', 'USDAL', 'FIHEL', 8, 14),
        ),
        'events': (
            ('RECEIVE', 'CNHKG', None, -10),
            ('LOAD', 'CNHKG', '0100S', -7),
            ('UNLOAD', 'USNYC', '0100S', -1),
        ),
    },
    {
        'tracking_id': 'JKL567',
        'origin': 'CNHGH',
        'destination': 'SESTO',
        'deadline_days': 18,
        'transport_status': 'ONBOARD_CARRIER',
        'last_known_location': 'USNYC',
        'current_voyage': '0100S',
        'misdirected': True,
        'routing_status': 'ROUTED',
        'legs': (
            ('0100S', 'CNHGH', 'USNYC', -10, -3),
            ('0200T', 'USNYC', 'USDAL', -2, 2),
            ('0300A', 'USDAL', 'SESTO', 6, 15),
        ),
        'events': (
            ('RECEIVE', 'CNHGH', None, -15),
            ('LOAD', 'CNHGH', '0100S', -10),
            ('UNLOAD', 'USNYC', '0100S', -3),
            ('LOAD', 'USNYC', '0100S', -2),
        ),
    },
    {
        'tracking_id': 'DEF789',
        'origin': 'CNHKG',
        'destination': 'AUMEL',
        'deadline_months': 2,
        'transport_status': 'NOT_RECEIVED',
        'misdirected': False,
        'routing_status': 'NOT_ROUTED',
        'legs': (),
        'events': (),
    },
    {
        'tracking_id': 'MNO456',
        'origin': 'USNYC',
        'destination': 'USDAL',
        'deadline_days': -24,
        'transport_status': 'CLAIMED',
        'last_known_location': 'USDAL',
        'misdirected': False,
        'eta_days': -28,
        'routing_status': 'ROUTED',
        'unloaded_at_dest': True,
        'legs': (('0200T', 'USNYC', 'USDAL', -34, -28),),
        'events': (
            ('RECEIVE', 'USNYC', None, -37),
            ('LOAD', 'USNYC', '0200T', -34),
            ('UNLOAD', 'USDAL', '0200T', -28),
            ('CUSTOMS', 'USDAL', None, -27),
            ('CLAIM', 'USDAL', None, -26),
        ),
    },
)


def _add_months(value, months):
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def _date_with_offset(today, days):
    return today + timedelta(days=days)


def _datetime_with_offset(today, days):
    return datetime.combine(_date_with_offset(today, days), time.min, tzinfo=UTC)


def _cargo_defaults(seed, locations, voyages, today):
    deadline = (
        _add_months(today, seed['deadline_months'])
        if 'deadline_months' in seed
        else _date_with_offset(today, seed['deadline_days'])
    )
    next_event, next_location, next_voyage = seed.get('next_expected', (None, None, None))
    return {
        'origin': locations[seed['origin']],
        'spec_origin': locations[seed['origin']],
        'spec_destination': locations[seed['destination']],
        'spec_arrival_deadline': deadline,
        'transport_status': seed['transport_status'],
        'last_known_location': locations.get(seed.get('last_known_location')),
        'current_voyage': voyages.get(seed.get('current_voyage')),
        'misdirected': seed['misdirected'],
        'eta': (_date_with_offset(today, seed['eta_days']) if 'eta_days' in seed else None),
        'next_expected_handling_event_type': next_event,
        'next_expected_location': locations.get(next_location),
        'next_expected_voyage': voyages.get(next_voyage),
        'unloaded_at_dest': seed.get('unloaded_at_dest', False),
        'routing_status': seed['routing_status'],
        'calculated_at': timezone.now().astimezone(UTC),
        'last_event': None,
    }


def _seed_cargo(seed, locations, voyages, today):
    cargo, _ = CargoRecord.objects.update_or_create(
        tracking_id=seed['tracking_id'],
        defaults=_cargo_defaults(seed, locations, voyages, today),
    )
    events = []
    for event_type, location, voyage, offset in seed['events']:
        event, _ = HandlingEventRecord.objects.update_or_create(
            cargo=cargo,
            event_type=event_type,
            location=locations[location],
            voyage=voyages.get(voyage),
            completion_time=_date_with_offset(today, offset),
            defaults={'registration_time': today},
        )
        events.append(event)
    for voyage, load_location, unload_location, load_offset, unload_offset in seed['legs']:
        LegRecord.objects.update_or_create(
            cargo=cargo,
            load_time=_datetime_with_offset(today, load_offset),
            defaults={
                'voyage': voyages[voyage],
                'load_location': locations[load_location],
                'unload_location': locations[unload_location],
                'unload_time': _datetime_with_offset(today, unload_offset),
            },
        )
    cargo.last_event = events[-1] if events else None
    cargo.save(update_fields=['last_event'])


class Command(BaseCommand):
    help = 'Seed the characterized Cargo Tracker sample data.'

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.now().astimezone(UTC).date()
        locations = {
            code: LocationRecord.objects.update_or_create(unlocode=code, defaults={'name': name})[0]
            for code, name in LOCATIONS
        }
        voyages = {
            number: VoyageRecord.objects.update_or_create(voyage_number=number, defaults={})[0]
            for number in VOYAGES
        }
        for seed in SAMPLE_CARGOS:
            _seed_cargo(seed, locations, voyages, today)
        self.stdout.write(self.style.SUCCESS('Seeded characterized sample data.'))
