import os
from time import sleep

from django.core.management.base import BaseCommand, CommandError

from cargotracker.handling.application.process_registration_attempt import (
    process_registration_attempt,
)


class Command(BaseCommand):
    help = 'Process accepted handling registration attempts.'

    def handle(self, *args, **options):
        poll_seconds = float(os.environ.get('HANDLING_ATTEMPT_POLL_SECONDS', '1'))
        if poll_seconds <= 0:
            raise CommandError('HANDLING_ATTEMPT_POLL_SECONDS must be greater than zero')
        while True:
            if not process_registration_attempt():
                sleep(poll_seconds)
