from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.handling.domain.registration_attempt import (
    RegistrationAttempt,
    RegistrationAttemptStatus,
)
from cargotracker.handling.domain.repository import RegistrationAttemptRepository
from cargotracker.handling.infrastructure.models import RegistrationAttemptRecord
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


class DjangoAttemptSubmissionRepository(RegistrationAttemptRepository):
    def submit(self, attempt: RegistrationAttempt) -> RegistrationAttempt:
        if attempt.id is not None or attempt.status is not RegistrationAttemptStatus.ACCEPTED:
            raise ValueError('Only a new registration attempt can be submitted')

        record = RegistrationAttemptRecord.objects.create(
            tracking_id=attempt.tracking_id.value,
            completion_time=attempt.completion_time,
            registration_time=attempt.registration_time,
            event_type=attempt.event_type.value,
            un_locode=attempt.location.value,
            voyage_number=attempt.voyage_number.value if attempt.voyage_number else None,
            status=attempt.status.value,
        )
        return self._to_domain(record)

    def claim_next(self) -> RegistrationAttempt | None:
        """Lock one accepted attempt until the caller's transaction ends."""
        record = (
            RegistrationAttemptRecord.objects.select_for_update(skip_locked=True)
            .filter(status=RegistrationAttemptStatus.ACCEPTED.value)
            .first()
        )
        return self._to_domain(record) if record is not None else None

    def mark_registered(self, attempt_id: int) -> None:
        self._mark_terminal(attempt_id, RegistrationAttemptStatus.REGISTERED)

    def mark_rejected(self, attempt_id: int, reason: str) -> None:
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError('A rejected registration attempt requires a reason')
        self._mark_terminal(attempt_id, RegistrationAttemptStatus.REJECTED, reason)

    @staticmethod
    def _mark_terminal(
        attempt_id: int, status: RegistrationAttemptStatus, reason: str | None = None
    ) -> None:
        updated = RegistrationAttemptRecord.objects.filter(
            pk=attempt_id, status=RegistrationAttemptStatus.ACCEPTED.value
        ).update(status=status.value, rejection_reason=reason)
        if updated != 1:
            raise ValueError(f'Registration attempt {attempt_id} is not accepted')

    @staticmethod
    def _to_domain(record: RegistrationAttemptRecord) -> RegistrationAttempt:
        return RegistrationAttempt(
            id=record.pk,
            tracking_id=TrackingId(record.tracking_id),
            completion_time=record.completion_time,
            registration_time=record.registration_time,
            event_type=HandlingEventType(record.event_type),
            location=UnLocode(record.un_locode),
            voyage_number=(
                VoyageNumber(record.voyage_number) if record.voyage_number is not None else None
            ),
            status=RegistrationAttemptStatus(record.status),
            rejection_reason=record.rejection_reason,
        )
