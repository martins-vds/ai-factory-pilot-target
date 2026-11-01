from datetime import UTC

from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import TransportStatus


def format_eta(cargo: Cargo) -> str | None:
    delivery = cargo.delivery
    if delivery.transport_status is TransportStatus.CLAIMED:
        return None
    if delivery.eta is None:
        return '?'
    return delivery.eta.astimezone(UTC).strftime('%m/%d/%Y %I:%M %p UTC')
