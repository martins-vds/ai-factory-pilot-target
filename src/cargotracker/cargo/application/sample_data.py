from datetime import date
from typing import Protocol

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


class SampleDataRepository(Protocol):
    def upsert_location(self, code: str, name: str) -> None: ...

    def upsert_voyage(self, number: str) -> None: ...

    def upsert_cargo(self, seed: dict[str, object], today: date) -> None: ...


class SampleDataSeeder:
    def __init__(self, repository: SampleDataRepository):
        self._repository = repository

    def seed(self, today: date) -> None:
        for code, name in LOCATIONS:
            self._repository.upsert_location(code, name)
        for number in VOYAGES:
            self._repository.upsert_voyage(number)
        for seed in SAMPLE_CARGOS:
            self._repository.upsert_cargo(seed, today)
