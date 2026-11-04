from collections.abc import Iterator
from contextlib import contextmanager

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction

from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.domain.repository import (
    TemporaryProcessingFailure,
    UnknownLocation,
    UnknownVoyage,
)
from cargotracker.handling.infrastructure.attempt_submission_repository import (
    DjangoAttemptSubmissionRepository,
)
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.repository import DjangoLocationRepository
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.repository import DjangoVoyageRepository


class DjangoAttemptProcessingRepository:
    def __init__(self):
        self._repository = DjangoAttemptSubmissionRepository()
        self._locations = DjangoLocationRepository()
        self._voyages = DjangoVoyageRepository()

    @contextmanager
    def atomic(self) -> Iterator[None]:
        try:
            with transaction.atomic():
                yield
        except (DatabaseError, TimeoutError, ConnectionError) as error:
            raise TemporaryProcessingFailure(str(error)) from error

    def find_location(self, un_locode: UnLocode) -> Location:
        try:
            return self._locations.find(un_locode)
        except ObjectDoesNotExist as error:
            raise UnknownLocation(un_locode.value) from error

    def find_voyage(self, voyage_number: VoyageNumber) -> Voyage:
        try:
            return self._voyages.find(voyage_number)
        except ObjectDoesNotExist as error:
            raise UnknownVoyage(voyage_number.value) from error

    def claim_next(self) -> RegistrationAttempt | None:
        return self._repository.claim_next()

    def mark_registered(self, attempt_id: int) -> None:
        self._repository.mark_registered(attempt_id)

    def mark_rejected(self, attempt_id: int, reason: str) -> None:
        self._repository.mark_rejected(attempt_id, reason)
