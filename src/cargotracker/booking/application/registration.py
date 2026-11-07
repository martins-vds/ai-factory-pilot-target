import logging
import uuid
from datetime import datetime

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.handling_history import HandlingHistory
from cargotracker.location.domain.location import Location


logger = logging.getLogger(__name__)


class CargoRegistration:
    def __init__(self, cargo_repository: CargoRepository):
        self._cargo_repository = cargo_repository

    def register(
        self,
        origin: Location,
        destination: Location,
        arrival_deadline: datetime,
    ) -> TrackingId:
        tracking_id = TrackingId(uuid.uuid4().hex[:8].upper())
        specification = RouteSpecification(origin, destination, arrival_deadline)
        itinerary = Itinerary.EMPTY
        delivery = Delivery.derived_from(specification, itinerary, HandlingHistory.EMPTY)
        cargo = Cargo(tracking_id, specification, delivery, itinerary)
        self._cargo_repository.upsert(cargo)
        logger.info('Booked new cargo with tracking ID %s', tracking_id)
        return tracking_id
