from django.core.management.base import BaseCommand, CommandError

from cargotracker.data_migration.loader import DataLoadError, load_snapshot


class Command(BaseCommand):
    help = 'Load a validated relational snapshot using its mapping.'

    def add_arguments(self, parser):
        parser.add_argument('--snapshot', required=True)
        parser.add_argument('--mapping', required=True)

    def handle(self, *args, **options):
        try:
            loaded = load_snapshot(options['snapshot'], options['mapping'])
        except DataLoadError as error:
            raise CommandError(str(error)) from error
        total = sum(rows for _, rows in loaded)
        self.stdout.write(
            self.style.SUCCESS(f'Loaded {total} rows across {len(loaded)} mapped tables.')
        )
