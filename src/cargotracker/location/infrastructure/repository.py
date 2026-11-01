from cargotracker.location.domain.location import Location
from cargotracker.location.domain.repository import LocationRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord


class DjangoLocationRepository(LocationRepository):
    def find(self, unlocode: UnLocode) -> Location:
        record = LocationRecord.objects.get(unlocode=unlocode.value)
        return self._to_domain(record)

    def find_all(self) -> list[Location]:
        return [self._to_domain(record) for record in LocationRecord.objects.all()]

    @staticmethod
    def _to_domain(record: LocationRecord) -> Location:
        return Location(UnLocode(record.unlocode), record.name)
