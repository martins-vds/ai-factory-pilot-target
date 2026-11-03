from cargotracker.handling.domain.registration_attempt import (
    RegistrationAttempt,
    RegistrationAttemptStatus,
)
from cargotracker.handling.domain.repository import RegistrationAttemptRepository


def accept_registration(
    attempt: RegistrationAttempt, repository: RegistrationAttemptRepository
) -> RegistrationAttempt:
    if attempt.id is not None or attempt.status is not RegistrationAttemptStatus.ACCEPTED:
        raise ValueError('Only a new registration attempt can be accepted')
    return repository.submit(attempt)
