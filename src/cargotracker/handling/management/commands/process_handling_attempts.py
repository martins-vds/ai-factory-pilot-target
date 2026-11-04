import os
from math import isfinite
from time import sleep

from django.core.management.base import BaseCommand, CommandError

from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.application.process_registration_attempt import (
    process_registration_attempt,
)
from cargotracker.handling.infrastructure.attempt_processing_repository import (
    DjangoAttemptProcessingRepository,
)
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository


class Command(BaseCommand):
    help = 'Process accepted handling registration attempts.'

    def handle(self, *args, **options):
        poll_seconds = float(os.environ.get('HANDLING_ATTEMPT_POLL_SECONDS', '1'))
        if not isfinite(poll_seconds) or poll_seconds <= 0:
            raise CommandError('HANDLING_ATTEMPT_POLL_SECONDS must be greater than zero')
        try:
            retry_backoff_seconds = float(
                os.environ.get('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', '1')
            )
        except ValueError as error:
            raise CommandError(
                'HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be a positive number'
            ) from error
        if not isfinite(retry_backoff_seconds) or retry_backoff_seconds <= 0:
            raise CommandError('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be greater than zero')
        repositories = (
            DjangoAttemptProcessingRepository(),
            DjangoCargoRepository(),
            DjangoHandlingEventRepository(),
        )
        while True:
            if not process_registration_attempt(
                *repositories,
                retry_backoff_seconds=retry_backoff_seconds,
            ):
                sleep(poll_seconds)
