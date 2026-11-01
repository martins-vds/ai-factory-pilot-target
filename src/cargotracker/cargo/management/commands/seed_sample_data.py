from datetime import UTC

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from cargotracker.cargo.application.sample_data import SampleDataSeeder
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository


class Command(BaseCommand):
    help = 'Seed the characterized Cargo Tracker sample data.'

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.now().astimezone(UTC).date()
        SampleDataSeeder(
            DjangoLocationRepository(),
            DjangoVoyageRepository(),
            DjangoCargoRepository(),
            DjangoHandlingEventRepository(),
        ).seed(today)
        self.stdout.write(self.style.SUCCESS('Seeded characterized sample data.'))
