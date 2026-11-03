import logging
from dataclasses import replace
from math import isfinite
from time import monotonic, sleep

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.handling.domain.handling_event import HandlingEvent
from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.domain.repository import (
    HandlingEventRepository,
    RegistrationProcessingRepository,
    TemporaryProcessingFailure,
    UnknownLocation,
    UnknownVoyage,
)
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage import Voyage

logger = logging.getLogger(__name__)
_RETRY_LOG_AFTER_SECONDS = 15 * 60
_MAX_RETRY_BACKOFF_SECONDS = 60


class _PermanentRegistrationFailure(Exception):
    def __init__(self, reason_code: str, message: str):
        super().__init__(message)
        self.reason_code = reason_code

    def rejection_reason(self) -> str:
        return f'{self.reason_code}: {self}'


def process_registration_attempt(
    attempts: RegistrationProcessingRepository,
    cargos: CargoRepository,
    events: HandlingEventRepository,
    retry_backoff_seconds: float = 1.0,
) -> bool:
    if not isfinite(retry_backoff_seconds) or retry_backoff_seconds <= 0:
        raise ValueError('Retry backoff must be greater than zero')
    delay = min(retry_backoff_seconds, _MAX_RETRY_BACKOFF_SECONDS)
    retry_started = None
    error_logged = False
    while True:
        try:
            return _process_registration_attempt_once(attempts, cargos, events)
        except TemporaryProcessingFailure as error:
            now = monotonic()
            if retry_started is None:
                retry_started = now
            if now - retry_started >= _RETRY_LOG_AFTER_SECONDS and not error_logged:
                logger.error(
                    'Handling attempt processing still failing after 15 minutes: %s', error
                )
                error_logged = True
            sleep(delay)
            delay = min(delay * 2, _MAX_RETRY_BACKOFF_SECONDS)


def _process_registration_attempt_once(
    attempts: RegistrationProcessingRepository,
    cargos: CargoRepository,
    events: HandlingEventRepository,
) -> bool:
    outcome_logs = []
    with attempts.atomic():
        attempt = attempts.claim_next()
        if attempt is None:
            return False
        try:
            cargo, event = _resolve_event(attempt, cargos, attempts)
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
                delivery = replace(delivery, last_event_id=history.most_recent_event_id)
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


def _resolve_event(
    attempt: RegistrationAttempt,
    cargos: CargoRepository,
    attempts: RegistrationProcessingRepository,
) -> tuple[Cargo, HandlingEvent]:
    cargo = cargos.find(attempt.tracking_id)
    if cargo is None:
        raise _PermanentRegistrationFailure(
            'UNKNOWN_CARGO', f'cargo {attempt.tracking_id.value} does not exist'
        )
    location = _resolve_location(attempt.location, attempts)
    voyage = _resolve_voyage(attempt, attempts)
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


def _resolve_location(
    un_locode: UnLocode,
    attempts: RegistrationProcessingRepository,
) -> Location:
    try:
        return attempts.find_location(un_locode)
    except UnknownLocation as error:
        raise _PermanentRegistrationFailure(
            'UNKNOWN_LOCATION', f'location {un_locode.value} does not exist'
        ) from error


def _resolve_voyage(
    attempt: RegistrationAttempt,
    attempts: RegistrationProcessingRepository,
) -> Voyage | None:
    if attempt.voyage_number is None:
        return None
    try:
        return attempts.find_voyage(attempt.voyage_number)
    except UnknownVoyage as error:
        raise _PermanentRegistrationFailure(
            'UNKNOWN_VOYAGE', f'voyage {attempt.voyage_number.value} does not exist'
        ) from error
