from cargotracker.cargo.domain.cargo import Cargo
from cargotracker.cargo.domain.delivery import TransportStatus

UNKNOWN_STATUS_TEXT = '[Unknown status]'

_STATUS_TEXTS = {
    TransportStatus.NOT_RECEIVED: 'Not received',
    TransportStatus.CLAIMED: 'Claimed',
    TransportStatus.UNKNOWN: UNKNOWN_STATUS_TEXT,
}


def get_status_text(cargo: Cargo) -> str:
    status = cargo.delivery.transport_status
    if status is TransportStatus.IN_PORT:
        return _in_port_status_text(cargo)
    if status is TransportStatus.ONBOARD_CARRIER:
        return _onboard_status_text(cargo)
    return _STATUS_TEXTS.get(status, UNKNOWN_STATUS_TEXT)


def _in_port_status_text(cargo: Cargo) -> str:
    location = cargo.delivery.last_known_location
    return f'In port {location.name}' if location is not None else UNKNOWN_STATUS_TEXT


def _onboard_status_text(cargo: Cargo) -> str:
    voyage = cargo.delivery.current_voyage
    return (
        f'Onboard voyage {voyage.voyage_number.value}'
        if voyage is not None
        else UNKNOWN_STATUS_TEXT
    )
