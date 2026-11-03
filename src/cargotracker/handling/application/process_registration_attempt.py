import logging
import os
from dataclasses import replace
from time import monotonic, sleep

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction

from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.domain.handling_event import HandlingEvent
from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.infrastructure.attempt_processing_repository import (
    DjangoAttemptProcessingRepository,
)
from cargotracker.handling.infrastructure.repository import DjangoHandlingEventRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository

logger = logging.getLogger(__name__)
_RETRY_BACKOFF_SETTING = 'HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS'
_RETRY_LOG_AFTER_SECONDS = 15 * 60
_MAX_RETRY_BACKOFF_SECONDS = 60


class _PermanentRegistrationFailure(Exception):
    def __init__(self, reason_code: str, message: str):
        super().__init__(message)
        self.reason_code = reason_code

    def rejection_reason(self) -> str:
        return f'{self.reason_code}: {self}'


def process_registration_attempt() -> bool:
    delay = _retry_backoff_seconds()
    retry_started = None
    error_logged = False
    while True:
        try:
            return _process_registration_attempt_once()
        except (DatabaseError, TimeoutError, ConnectionError) as error:
            now = monotonic()
            if retry_started is None:
                retry_started = now
            if now - retry_started >= _RETRY_LOG_AFTER_SECONDS and not error_logged:
                logger.error('Handling attempt processing still failing after 15 minutes: %s', error)
                error_logged = True
            sleep(delay)
            delay = min(delay * 2, _MAX_RETRY_BACKOFF_SECONDS)


def _process_registration_attempt_once() -> bool:
    attempts = DjangoAttemptProcessingRepository()
    cargos = DjangoCargoRepository()
    events = DjangoHandlingEventRepository()
    outcome_logs = []
    with transaction.atomic():
        attempt = attempts.claim_next()
        if attempt is None:
            return False
        try:
            cargo, event = _resolve_event(attempt, cargos)
        except _PermanentRegistrationFailure as failure:
            attempts.mark_rejected(attempt.id, failure.rejection_reason())
            outcome_logs.append(
                ('warning', 'Registration attempt %s rejected: %s', (attempt.id, failure))
            )
        else:
            events.store(event)
            history = events.lookup_handling_history_of_cargo(attempt.tracking_id)
            delivery = Delivery.derived_from(
                cargo.route_specification,
                cargo.itinerary,
                history,
            )
            latest_event = history.most_recent_event
            if latest_event is not None:
                delivery = replace(delivery, last_event_id=latest_event.id)
            cargos.upsert(replace(cargo, delivery=delivery))
            attempts.mark_registered(attempt.id)
            if delivery.misdirected:
                outcome_logs.append(
                    ('info', 'Cargo %s is misdirected', (attempt.tracking_id.value,))
                )
            if delivery.unloaded_at_destination:
                outcome_logs.append(('info', 'Cargo %s delivered', (attempt.tracking_id.value,)))
    for level, message, args in outcome_logs:
        getattr(logger, level)(message, *args)
    return True


def _retry_backoff_seconds() -> float:
    delay = float(os.environ.get(_RETRY_BACKOFF_SETTING, '1'))
    if delay <= 0:
        raise ValueError(f'{_RETRY_BACKOFF_SETTING} must be greater than zero')
    return delay


def _resolve_event(
    attempt: RegistrationAttempt,
    cargos: DjangoCargoRepository,
) -> tuple[object, HandlingEvent]:
    cargo = cargos.find(attempt.tracking_id)
    if cargo is None:
        raise _PermanentRegistrationFailure(
            'UNKNOWN_CARGO', f'cargo {attempt.tracking_id.value} does not exist'
        )
    location = _resolve_location(attempt.location)
    voyage = _resolve_voyage(attempt)
    try:
        event = HandlingEvent(
            cargo,
            attempt.completion_time,
            attempt.registration_time,
            attempt.event_type,
            location,
            voyage,
        )
    except ValueError as error:
        raise _PermanentRegistrationFailure('INVALID_EVENT', str(error)) from error
    return cargo, event


def _resolve_location(un_locode) -> Location:
    try:
        return DjangoLocationRepository().find(un_locode)
    except ObjectDoesNotExist as error:
        raise _PermanentRegistrationFailure(
            'UNKNOWN_LOCATION', f'location {un_locode.value} does not exist'
        ) from error


def _resolve_voyage(attempt: RegistrationAttempt):
    if attempt.voyage_number is None:
        return None
    try:
        return DjangoVoyageRepository().find(attempt.voyage_number)
    except ObjectDoesNotExist as error:
        raise _PermanentRegistrationFailure(
            'UNKNOWN_VOYAGE', f'voyage {attempt.voyage_number.value} does not exist'
        ) from error
