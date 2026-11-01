package org.eclipse.cargotracker.domain.model.cargo;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.util.Arrays;
import java.util.Collections;
import java.util.Date;

import org.eclipse.cargotracker.domain.model.handling.HandlingEvent;
import org.eclipse.cargotracker.domain.model.handling.HandlingHistory;
import org.eclipse.cargotracker.domain.model.location.Location;
import org.eclipse.cargotracker.domain.model.location.SampleLocations;
import org.eclipse.cargotracker.domain.model.voyage.Voyage;
import org.eclipse.cargotracker.domain.model.voyage.VoyageNumber;
import org.junit.Test;

public class TrackCargoCharacterizationTest {

    private final Location origin = SampleLocations.SHANGHAI;
    private final Location midpoint = SampleLocations.ROTTERDAM;
    private final Location destination = SampleLocations.GOTHENBURG;
    private final Voyage firstVoyage = voyage("V1", origin, midpoint);
    private final Voyage secondVoyage = voyage("V2", midpoint, destination);
    private final Itinerary itinerary = new Itinerary(Arrays.asList(
            leg(firstVoyage, origin, midpoint, 10, 20),
            leg(secondVoyage, midpoint, destination, 30, 40)));

    @Test
    public void emptyItineraryAcceptsEveryHandlingType() {
        Cargo cargo = cargo(origin, destination, new Itinerary());
        for (HandlingEvent.Type type : HandlingEvent.Type.values()) {
            assertTrue(type.name(), new Itinerary().isExpected(
                    event(cargo, type, origin, type == HandlingEvent.Type.LOAD
                            || type == HandlingEvent.Type.UNLOAD ? firstVoyage : null)));
        }
    }

    @Test
    public void transportStatusUsesTheLastEventType() {
        Cargo withoutEvents = cargo(origin, destination, new Itinerary());
        assertEquals(TransportStatus.NOT_RECEIVED, withoutEvents.getDelivery().getTransportStatus());
        assertEquals(TransportStatus.ONBOARD_CARRIER, status(HandlingEvent.Type.LOAD, origin, firstVoyage));
        assertEquals(TransportStatus.IN_PORT, status(HandlingEvent.Type.UNLOAD, midpoint, firstVoyage));
        assertEquals(TransportStatus.IN_PORT, status(HandlingEvent.Type.RECEIVE, origin, null));
        assertEquals(TransportStatus.IN_PORT, status(HandlingEvent.Type.CUSTOMS, origin, null));
        assertEquals(TransportStatus.CLAIMED, status(HandlingEvent.Type.CLAIM, destination, null));
    }

    @Test
    public void nextActivityForNoEventAndReceive() {
        Cargo cargo = cargo(origin, destination, itinerary);
        assertActivity(cargo.getDelivery().getNextExpectedActivity(), HandlingEvent.Type.RECEIVE,
                origin, null);

        derive(cargo, event(cargo, HandlingEvent.Type.RECEIVE, origin, null));
        assertActivity(cargo.getDelivery().getNextExpectedActivity(), HandlingEvent.Type.LOAD,
                origin, firstVoyage);
    }

    @Test
    public void nextActivityAfterLoadAndUnload() {
        Cargo cargo = cargo(origin, destination, itinerary);
        derive(cargo, event(cargo, HandlingEvent.Type.LOAD, origin, firstVoyage));
        assertActivity(cargo.getDelivery().getNextExpectedActivity(), HandlingEvent.Type.UNLOAD,
                midpoint, firstVoyage);

        derive(cargo, event(cargo, HandlingEvent.Type.UNLOAD, midpoint, firstVoyage));
        assertActivity(cargo.getDelivery().getNextExpectedActivity(), HandlingEvent.Type.LOAD,
                midpoint, secondVoyage);

        derive(cargo, event(cargo, HandlingEvent.Type.UNLOAD, destination, secondVoyage));
        assertActivity(cargo.getDelivery().getNextExpectedActivity(), HandlingEvent.Type.CLAIM,
                destination, null);

        derive(cargo, event(cargo, HandlingEvent.Type.CLAIM, destination, null));
        assertTrue(cargo.getDelivery().getNextExpectedActivity().isEmpty());
    }

    @Test
    public void offTrackAndUnroutedCargoHaveNoNextActivity() {
        Cargo unrouted = cargo(origin, destination, new Itinerary());
        assertTrue(unrouted.getDelivery().getNextExpectedActivity().isEmpty());

        Cargo offTrack = cargo(origin, destination, itinerary);
        derive(offTrack, event(offTrack, HandlingEvent.Type.RECEIVE, midpoint, null));
        assertTrue(offTrack.getDelivery().isMisdirected());
        assertTrue(offTrack.getDelivery().getNextExpectedActivity().isEmpty());
    }

    private TransportStatus status(HandlingEvent.Type type, Location location, Voyage voyage) {
        Cargo cargo = cargo(origin, destination, new Itinerary());
        derive(cargo, event(cargo, type, location, voyage));
        return cargo.getDelivery().getTransportStatus();
    }

    private Cargo cargo(Location routeOrigin, Location routeDestination, Itinerary route) {
        RouteSpecification specification = new RouteSpecification(
                routeOrigin, routeDestination, new Date(Long.MAX_VALUE));
        Cargo cargo = new Cargo(new TrackingId("TIERB"), specification);
        if (!route.getLegs().isEmpty()) {
            cargo.assignToRoute(route);
        }
        return cargo;
    }

    private void derive(Cargo cargo, HandlingEvent event) {
        cargo.deriveDeliveryProgress(new HandlingHistory(Collections.singletonList(event)));
    }

    private HandlingEvent event(
            Cargo cargo, HandlingEvent.Type type, Location location, Voyage voyage) {
        if (type == HandlingEvent.Type.LOAD || type == HandlingEvent.Type.UNLOAD) {
            return new HandlingEvent(cargo, new Date(1), new Date(2), type, location, voyage);
        }
        return new HandlingEvent(cargo, new Date(1), new Date(2), type, location);
    }

    private void assertActivity(
            HandlingActivity activity, HandlingEvent.Type type, Location location, Voyage voyage) {
        assertEquals(type, activity.getType());
        assertEquals(location, activity.getLocation());
        assertEquals(voyage, activity.getVoyage());
    }

    private static Voyage voyage(String number, Location from, Location to) {
        return new Voyage.Builder(new VoyageNumber(number), from)
                .addMovement(to, new Date(1), new Date(2))
                .build();
    }

    private static Leg leg(
            Voyage voyage, Location from, Location to, long loadTime, long unloadTime) {
        return new Leg(voyage, from, to, new Date(loadTime), new Date(unloadTime));
    }
}
