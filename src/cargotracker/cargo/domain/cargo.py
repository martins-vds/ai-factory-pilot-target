from dataclasses import dataclass, field

from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.location.domain.location import Location


@dataclass(eq=False)
class Cargo:
    tracking_id: TrackingId
    route_specification: RouteSpecification
    delivery: Delivery
    itinerary: Itinerary = field(default_factory=lambda: Itinerary.EMPTY)
    origin: Location | None = None

    def __post_init__(self):
        if not isinstance(self.tracking_id, TrackingId):
            raise TypeError('A cargo requires a tracking ID')
        if not isinstance(self.route_specification, RouteSpecification):
            raise TypeError('A cargo requires a route specification')
        if not isinstance(self.delivery, Delivery):
            raise TypeError('A cargo requires a delivery')
        if not isinstance(self.itinerary, Itinerary):
            raise TypeError('A cargo requires an itinerary')
        if self.origin is None:
            self.origin = self.route_specification.origin
        elif not isinstance(self.origin, Location):
            raise TypeError('A cargo origin must be a location')

    def __eq__(self, other):
        return isinstance(other, Cargo) and self.tracking_id == other.tracking_id

    def __hash__(self):
        return hash(self.tracking_id)
