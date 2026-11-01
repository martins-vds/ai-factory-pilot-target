from cargotracker.voyage.domain.repository import VoyageRepository
from cargotracker.voyage.domain.schedule import Schedule
from cargotracker.voyage.domain.voyage import Voyage
from cargotracker.voyage.domain.voyage_number import VoyageNumber
from cargotracker.voyage.infrastructure.models import VoyageRecord


class DjangoVoyageRepository(VoyageRepository):
    def upsert(self, voyage: Voyage) -> None:
        VoyageRecord.objects.update_or_create(
            voyage_number=voyage.voyage_number.value,
            defaults={},
        )

    def find(self, voyage_number: VoyageNumber) -> Voyage:
        record = VoyageRecord.objects.get(voyage_number=voyage_number.value)
        return self._to_domain(record)

    def find_all(self) -> list[Voyage]:
        records = VoyageRecord.objects.order_by('voyage_number')
        return [self._to_domain(record) for record in records]

    @staticmethod
    def _to_domain(record: VoyageRecord) -> Voyage:
        return Voyage(VoyageNumber(record.voyage_number), Schedule.EMPTY)
