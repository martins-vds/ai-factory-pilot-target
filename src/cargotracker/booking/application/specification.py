import logging
from datetime import datetime

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.route_specification import RouteSpecification
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.repository import HandlingEventRepository
from cargotracker.location.domain.location import Location


logger = logging.getLogger(__name__)


class CargoSpecification:
    def __init__(
        self,
        cargo_repository: CargoRepository,
        handling_events: HandlingEventRepository,
    ):
        self._cargo_repository = cargo_repository
        self._handling_events = handling_events

    def change_destination(self, tracking_id: TrackingId, destination: Location) -> Cargo:
        cargo = self._find_cargo(tracking_id)
        specification = RouteSpecification(
            cargo.route_specification.origin,
            destination,
            cargo.route_specification.arrival_deadline,
        )
        updated_cargo = self._update(cargo, specification)
        logger.info(
            'Changed destination for cargo %s to %s',
            tracking_id,
            updated_cargo.route_specification.destination,
        )
        return updated_cargo

    def change_deadline(self, tracking_id: TrackingId, arrival_deadline: datetime) -> Cargo:
        cargo = self._find_cargo(tracking_id)
        specification = RouteSpecification(
            cargo.route_specification.origin,
            cargo.route_specification.destination,
            arrival_deadline,
        )
        updated_cargo = self._update(cargo, specification)
        logger.info(
            'Changed deadline for cargo %s to %s',
            tracking_id,
            arrival_deadline,
        )
        return updated_cargo

    def _find_cargo(self, tracking_id: TrackingId) -> Cargo:
        cargo = self._cargo_repository.find(tracking_id)
        if cargo is None:
            raise LookupError(f'Cargo {tracking_id} not found')
        return cargo

    def _update(self, cargo: Cargo, specification: RouteSpecification) -> Cargo:
        delivery = Delivery.derived_from(
            specification,
            cargo.itinerary,
            self._handling_events.lookup_handling_history_of_cargo(cargo.tracking_id),
        )
        updated_cargo = Cargo(
            cargo.tracking_id,
            specification,
            delivery,
            cargo.itinerary,
            cargo.origin,
        )
        self._cargo_repository.upsert(updated_cargo)
        return updated_cargo
