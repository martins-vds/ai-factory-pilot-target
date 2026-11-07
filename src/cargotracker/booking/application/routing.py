from django.http import Http404

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import Delivery
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.leg import Leg
from cargotracker.cargo.domain.repository import CargoRepository
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.domain.repository import HandlingEventRepository
from cargotracker.location.domain.repository import LocationRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.pathfinder.application.routing import RoutingService
from cargotracker.pathfinder.domain.transit_path import TransitPath
from cargotracker.voyage.domain.repository import VoyageRepository
from cargotracker.voyage.domain.voyage_number import VoyageNumber


class CargoRouting:
    def __init__(
        self,
        cargo_repository: CargoRepository,
        location_repository: LocationRepository,
        voyage_repository: VoyageRepository,
        handling_events: HandlingEventRepository,
        routing_service: RoutingService,
    ):
        self._cargo_repository = cargo_repository
        self._location_repository = location_repository
        self._voyage_repository = voyage_repository
        self._handling_events = handling_events
        self._routing_service = routing_service

    def route_candidates(self, tracking_id: TrackingId) -> tuple[Itinerary, ...]:
        cargo = self._find_cargo(tracking_id)
        route_specification = cargo.route_specification
        paths = self._routing_service.find_shortest_paths(
            route_specification.origin.unlocode.value,
            route_specification.destination.unlocode.value,
        )
        return tuple(
            itinerary
            for path in paths
            if route_specification.is_satisfied_by(itinerary := self._to_itinerary(path))
        )

    def assign_route(self, tracking_id: TrackingId, itinerary: Itinerary) -> Cargo:
        cargo = self._find_cargo(tracking_id)
        delivery = Delivery.derived_from(
            cargo.route_specification,
            itinerary,
            self._handling_events.lookup_handling_history_of_cargo(cargo.tracking_id),
        )
        updated_cargo = Cargo(
            cargo.tracking_id,
            cargo.route_specification,
            delivery,
            itinerary,
            cargo.origin,
        )
        self._cargo_repository.upsert(updated_cargo)
        return updated_cargo

    def _find_cargo(self, tracking_id: TrackingId) -> Cargo:
        cargo = self._cargo_repository.find(tracking_id)
        if cargo is None:
            raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
        return cargo

    def _to_itinerary(self, path: TransitPath) -> Itinerary:
        return Itinerary(
            tuple(
                Leg(
                    self._voyage_repository.find(VoyageNumber(edge.voyage_number)),
                    self._location_repository.find(UnLocode(edge.from_port)),
                    self._location_repository.find(UnLocode(edge.to_port)),
                    edge.from_date,
                    edge.to_date,
                )
                for edge in path.transit_edges
            )
        )
