from datetime import UTC, datetime, time

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.handling.domain.handling_event import HandlingEvent, HandlingEventType
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.handling.domain.repository import HandlingEventRepository
from cargotracker.handling.infrastructure.models import HandlingEventRecord
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord


class DjangoHandlingEventRepository(HandlingEventRepository):
    def store(self, event: HandlingEvent) -> None:
        HandlingEventRecord.objects.create(
            cargo=CargoRecord.objects.get(tracking_id=event.cargo.tracking_id.value),
            location=LocationRecord.objects.get(unlocode=event.location.unlocode.value),
            voyage=(
                VoyageRecord.objects.get(voyage_number=event.voyage.voyage_number.value)
                if event.voyage is not None
                else None
            ),
            event_type=event.event_type.value,
            completion_time=event.completion_time.date(),
            registration_time=event.registration_time.date(),
        )

    def lookup_handling_history_of_cargo(self, tracking_id: TrackingId) -> HandlingHistory:
        records = HandlingEventRecord.objects.select_related('cargo', 'location', 'voyage').filter(
            cargo__tracking_id=tracking_id.value
        )
        return HandlingHistory([self._to_domain(record) for record in records])

    @staticmethod
    def _to_domain(record: HandlingEventRecord) -> HandlingEvent:
        cargo = DjangoCargoRepository().find(TrackingId(record.cargo.tracking_id))
        return HandlingEvent(
            cargo,
            datetime.combine(record.completion_time, time.min, tzinfo=UTC),
            datetime.combine(record.registration_time, time.min, tzinfo=UTC),
            HandlingEventType(record.event_type),
            Location(UnLocode(record.location.unlocode), record.location.name),
            (
                Voyage(VoyageNumber(record.voyage.voyage_number), Schedule.EMPTY)
                if record.voyage_id is not None
                else None
            ),
        )
