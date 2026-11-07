from django.core.management.base import BaseCommand, CommandError

from cargotracker.data_migration.exporter import DataExportError, export_snapshot


class Command(BaseCommand):
    help = 'Export mapped target tables as a relational snapshot.'

    def add_arguments(self, parser):
        parser.add_argument('--mapping', required=True)
        parser.add_argument('--out', required=True)

    def handle(self, *args, **options):
        try:
            exported = export_snapshot(options['mapping'], options['out'])
        except DataExportError as error:
            raise CommandError(str(error)) from error
        total = sum(rows for _, rows in exported)
        self.stdout.write(
            self.style.SUCCESS(f'Exported {total} rows across {len(exported)} mapped tables.')
        )
