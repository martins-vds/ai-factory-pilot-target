from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.infrastructure.attempt_submission_repository import (
    DjangoAttemptSubmissionRepository,
)


class DjangoAttemptProcessingRepository:
    def __init__(self):
        self._repository = DjangoAttemptSubmissionRepository()

    def claim_next(self) -> RegistrationAttempt | None:
        return self._repository.claim_next()

    def mark_registered(self, attempt_id: int) -> None:
        self._repository.mark_registered(attempt_id)

    def mark_rejected(self, attempt_id: int, reason: str) -> None:
        self._repository.mark_rejected(attempt_id, reason)
