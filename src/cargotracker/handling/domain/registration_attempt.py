from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from cargotracker.cargo.domain.dates import as_utc
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


class RegistrationAttemptStatus(StrEnum):
    ACCEPTED = 'accepted'
    REGISTERED = 'registered'
    REJECTED = 'rejected'


@dataclass(frozen=True)
class RegistrationAttempt:
    tracking_id: TrackingId
    completion_time: datetime
    registration_time: datetime
    event_type: HandlingEventType
    location: UnLocode
    voyage_number: VoyageNumber | None = None
    id: int | None = None
    status: RegistrationAttemptStatus = RegistrationAttemptStatus.ACCEPTED
    rejection_reason: str | None = None

    def __post_init__(self):
        if not isinstance(self.tracking_id, TrackingId):
            raise TypeError('A registration attempt requires a tracking ID')
        object.__setattr__(self, 'completion_time', as_utc(self.completion_time, 'completion time'))
        object.__setattr__(
            self, 'registration_time', as_utc(self.registration_time, 'registration time')
        )
        if not isinstance(self.event_type, HandlingEventType):
            raise TypeError('A registration attempt requires an event type')
        if not isinstance(self.location, UnLocode):
            raise TypeError('A registration attempt requires a UN/LOCODE')
        if self.voyage_number is not None and not isinstance(self.voyage_number, VoyageNumber):
            raise TypeError('A registration attempt voyage number must be a voyage number')
        if self.id is not None and (
            not isinstance(self.id, int) or isinstance(self.id, bool) or self.id < 1
        ):
            raise ValueError('A registration attempt ID must be a positive integer')
        if not isinstance(self.status, RegistrationAttemptStatus):
            raise TypeError('A registration attempt requires a status')
        if self.status is RegistrationAttemptStatus.REJECTED:
            if not isinstance(self.rejection_reason, str) or not self.rejection_reason.strip():
                raise ValueError('A rejected registration attempt requires a reason')
        elif self.rejection_reason is not None:
            raise ValueError('Only a rejected registration attempt may have a reason')
