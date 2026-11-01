from cargotracker.cargo.domain.cargo import Cargo


def map_status_code(cargo: Cargo) -> str:
    if not cargo.itinerary.legs:
        return 'NOT_ROUTED'
    if cargo.delivery.unloaded_at_destination:
        return 'AT_DESTINATION'
    if cargo.delivery.misdirected:
        return 'MISDIRECTED'
    return cargo.delivery.transport_status.value
