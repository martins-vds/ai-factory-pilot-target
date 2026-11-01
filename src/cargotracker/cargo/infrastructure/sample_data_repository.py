import calendar
from datetime import UTC, date, datetime, time, timedelta

from django.utils import timezone

from cargotracker.cargo.infrastructure.models import CargoRecord, LegRecord
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.infrastructure.models import VoyageRecord


def _add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


def _date_with_offset(today: date, days: int) -> date:
    return today + timedelta(days=days)


def _datetime_with_offset(today: date, days: int) -> datetime:
    return datetime.combine(_date_with_offset(today, days), time.min, tzinfo=UTC)


class DjangoSampleDataRepository:
    def __init__(self):
        self._locations = {}
        self._voyages = {}

    def upsert_location(self, code: str, name: str) -> None:
        self._locations[code] = LocationRecord.objects.update_or_create(
            unlocode=code, defaults={'name': name}
        )[0]

    def upsert_voyage(self, number: str) -> None:
        self._voyages[number] = VoyageRecord.objects.update_or_create(
            voyage_number=number, defaults={}
        )[0]

    def upsert_cargo(self, seed: dict[str, object], today: date) -> None:
        cargo, _ = CargoRecord.objects.update_or_create(
            tracking_id=seed['tracking_id'],
            defaults=self._cargo_defaults(seed, today),
        )
        events = self._upsert_events(cargo, seed['events'], today)
        self._upsert_legs(cargo, seed['legs'], today)
        cargo.last_event = events[-1] if events else None
        cargo.save(update_fields=['last_event'])

    def _cargo_defaults(self, seed, today):
        deadline = (
            _add_months(today, seed['deadline_months'])
            if 'deadline_months' in seed
            else _date_with_offset(today, seed['deadline_days'])
        )
        next_event, next_location, next_voyage = seed.get('next_expected', (None, None, None))
        return {
            'origin': self._locations[seed['origin']],
            'spec_origin': self._locations[seed['origin']],
            'spec_destination': self._locations[seed['destination']],
            'spec_arrival_deadline': deadline,
            'transport_status': seed['transport_status'],
            'last_known_location': self._locations.get(seed.get('last_known_location')),
            'current_voyage': self._voyages.get(seed.get('current_voyage')),
            'misdirected': seed['misdirected'],
            'eta': (_date_with_offset(today, seed['eta_days']) if 'eta_days' in seed else None),
            'next_expected_handling_event_type': next_event,
            'next_expected_location': self._locations.get(next_location),
            'next_expected_voyage': self._voyages.get(next_voyage),
            'unloaded_at_dest': seed.get('unloaded_at_dest', False),
            'routing_status': seed['routing_status'],
            'calculated_at': timezone.now().astimezone(UTC),
            'last_event': None,
        }

    def _upsert_events(self, cargo, seeds, today):
        events = []
        for event_type, location, voyage, offset in seeds:
            event, _ = HandlingEventRecord.objects.update_or_create(
                cargo=cargo,
                event_type=event_type,
                location=self._locations[location],
                voyage=self._voyages.get(voyage),
                defaults={
                    'completion_time': _date_with_offset(today, offset),
                    'registration_time': today,
                },
            )
            events.append(event)
        return events

    def _upsert_legs(self, cargo, seeds, today):
        for voyage, load_location, unload_location, load_offset, unload_offset in seeds:
            LegRecord.objects.update_or_create(
                cargo=cargo,
                voyage=self._voyages[voyage],
                load_location=self._locations[load_location],
                unload_location=self._locations[unload_location],
                defaults={
                    'load_time': _datetime_with_offset(today, load_offset),
                    'unload_time': _datetime_with_offset(today, unload_offset),
                },
            )
