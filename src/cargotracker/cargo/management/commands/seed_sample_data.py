from datetime import UTC

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from cargotracker.cargo.application.sample_data import SampleDataSeeder
from cargotracker.cargo.infrastructure.sample_data_repository import DjangoSampleDataRepository


class Command(BaseCommand):
    help = 'Seed the characterized Cargo Tracker sample data.'

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.now().astimezone(UTC).date()
        SampleDataSeeder(DjangoSampleDataRepository()).seed(today)
        self.stdout.write(self.style.SUCCESS('Seeded characterized sample data.'))
