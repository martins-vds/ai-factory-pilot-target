import re
from datetime import UTC, datetime

import pytest

from cargotracker.booking.application.registration import CargoRegistration
from cargotracker.cargo.domain.delivery import RoutingStatus, TransportStatus
from cargotracker.cargo.domain.handling_activity import HandlingActivity
from cargotracker.cargo.domain.itinerary import Itinerary
from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.cargo.infrastructure.models import CargoRecord
from cargotracker.cargo.infrastructure.repository import DjangoCargoRepository
from cargotracker.location.domain.location import Location
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.location.infrastructure.models import LocationRecord


@pytest.mark.django_db
def test_registration_persists_new_cargo_with_generated_id_and_empty_itinerary(caplog):
    caplog.set_level('INFO')
    origin = Location(UnLocode('USNYC'), 'New York')
    destination = Location(UnLocode('FIHEL'), 'Helsinki')
    LocationRecord.objects.create(unlocode='USNYC', name='New York')
    LocationRecord.objects.create(unlocode='FIHEL', name='Helsinki')
    deadline = datetime(2030, 11, 12, tzinfo=UTC)
    repository = DjangoCargoRepository()

    tracking_id = CargoRegistration(repository).register(origin, destination, deadline)

    assert f'Booked new cargo with tracking ID {tracking_id.value}' in caplog.messages
    assert isinstance(tracking_id, TrackingId)
    assert re.fullmatch(r'[0-9A-F]{8}', tracking_id.value)
    record = CargoRecord.objects.get(tracking_id=tracking_id.value)
    assert record.origin.unlocode == 'USNYC'
    assert record.spec_origin.unlocode == 'USNYC'
    assert record.spec_destination.unlocode == 'FIHEL'
    assert record.spec_arrival_deadline.isoformat() == '2030-11-12'
    assert record.transport_status == TransportStatus.NOT_RECEIVED.value
    assert record.routing_status == RoutingStatus.NOT_ROUTED.value
    assert record.last_known_location is None
    assert record.current_voyage is None
    assert not record.misdirected
    assert not record.unloaded_at_dest
    assert record.eta is None
    assert record.next_expected_handling_event_type is None
    assert record.next_expected_location is None
    assert record.next_expected_voyage is None

    cargo = repository.find(tracking_id)
    assert cargo is not None
    assert cargo.delivery.next_expected_activity is HandlingActivity.EMPTY
    assert cargo.itinerary is Itinerary.EMPTY
