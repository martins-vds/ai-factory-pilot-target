package org.eclipse.cargotracker.application.internal;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.logging.Logger;

import javax.enterprise.event.Event;
import javax.jms.Destination;
import javax.jms.JMSContext;
import javax.jms.JMSProducer;

import org.eclipse.cargotracker.application.ApplicationEvents;
import org.eclipse.cargotracker.domain.model.cargo.Cargo;
import org.eclipse.cargotracker.domain.model.cargo.CargoRepository;
import org.eclipse.cargotracker.domain.model.cargo.Itinerary;
import org.eclipse.cargotracker.domain.model.cargo.Leg;
import org.eclipse.cargotracker.domain.model.cargo.RouteSpecification;
import org.eclipse.cargotracker.domain.model.cargo.TrackingId;
import org.eclipse.cargotracker.domain.model.handling.CannotCreateHandlingEventException;
import org.eclipse.cargotracker.domain.model.handling.HandlingEvent;
import org.eclipse.cargotracker.domain.model.handling.HandlingEventFactory;
import org.eclipse.cargotracker.domain.model.handling.HandlingEventRepository;
import org.eclipse.cargotracker.domain.model.handling.HandlingHistory;
import org.eclipse.cargotracker.domain.model.location.Location;
import org.eclipse.cargotracker.domain.model.location.LocationRepository;
import org.eclipse.cargotracker.domain.model.location.SampleLocations;
import org.eclipse.cargotracker.domain.model.location.UnLocode;
import org.eclipse.cargotracker.domain.model.voyage.SampleVoyages;
import org.eclipse.cargotracker.domain.model.voyage.Voyage;
import org.eclipse.cargotracker.domain.model.voyage.VoyageNumber;
import org.eclipse.cargotracker.domain.model.voyage.VoyageRepository;
import org.eclipse.cargotracker.infrastructure.messaging.jms.JmsApplicationEvents;
import org.eclipse.cargotracker.interfaces.handling.HandlingEventRegistrationAttempt;
import org.junit.Test;

public class HandlingRegistrationCharacterizationTest {

	@Test
	public void inspectionReturnsWithoutSideEffectsWhenCargoIsMissing() {
		InspectionFixture fixture = new InspectionFixture(null, new HandlingHistory(Collections.<HandlingEvent>emptyList()));

		fixture.service.inspectCargo(new TrackingId("MISSING"));

		assertEquals(0, fixture.cargoRepository.stores);
		assertEquals(0, fixture.handlingEventRepository.lookups);
		assertEquals(0, fixture.applicationEvents.misdirected);
		assertEquals(0, fixture.applicationEvents.arrived);
		assertEquals(0, fixture.inspected.size());
	}

	@Test
	public void inspectionPersistsCargoAndFiresInspectedEvent() {
		Cargo cargo = cargo();
		HandlingEvent receive = event(cargo, HandlingEvent.Type.RECEIVE, SampleLocations.HONGKONG, null);
		InspectionFixture fixture = new InspectionFixture(cargo, history(receive));

		fixture.service.inspectCargo(cargo.getTrackingId());

		assertEquals(1, fixture.cargoRepository.stores);
		assertEquals(1, fixture.handlingEventRepository.lookups);
		assertEquals(1, fixture.inspected.size());
		assertEquals(cargo, fixture.inspected.get(0));
		assertEquals(0, fixture.applicationEvents.misdirected);
		assertEquals(0, fixture.applicationEvents.arrived);
	}

	@Test
	public void inspectionNotifiesWhenCargoIsMisdirected() {
		Cargo cargo = cargo();
		HandlingEvent unload = event(
				cargo, HandlingEvent.Type.UNLOAD, SampleLocations.TOKYO, SampleVoyages.HONGKONG_TO_NEW_YORK);
		InspectionFixture fixture = new InspectionFixture(cargo, history(unload));

		fixture.service.inspectCargo(cargo.getTrackingId());

		assertEquals(1, fixture.applicationEvents.misdirected);
		assertEquals(0, fixture.applicationEvents.arrived);
		assertEquals(1, fixture.cargoRepository.stores);
	}

	@Test
	public void inspectionNotifiesWhenCargoIsUnloadedAtDestination() {
		Cargo cargo = cargo();
		HandlingEvent unload = event(
				cargo, HandlingEvent.Type.UNLOAD, SampleLocations.HELSINKI, SampleVoyages.DALLAS_TO_HELSINKI);
		InspectionFixture fixture = new InspectionFixture(cargo, history(unload));

		fixture.service.inspectCargo(cargo.getTrackingId());

		assertEquals(0, fixture.applicationEvents.misdirected);
		assertEquals(1, fixture.applicationEvents.arrived);
		assertEquals(1, fixture.cargoRepository.stores);
	}

	@Test
	public void factoryResolvesKnownCargoVoyageAndLocation() throws Exception {
		FactoryFixture fixture = new FactoryFixture();

		HandlingEvent event = fixture.factory.createHandlingEvent(
				new Date(), new Date(), fixture.cargo.getTrackingId(), null,
				SampleLocations.HONGKONG.getUnLocode(), HandlingEvent.Type.RECEIVE);

		assertEquals(fixture.cargo, event.getCargo());
		assertEquals(SampleLocations.HONGKONG, event.getLocation());
		assertEquals(Voyage.NONE, event.getVoyage());
	}

	@Test
	public void factoryRejectsUnknownCargo() throws Exception {
		final FactoryFixture fixture = new FactoryFixture();
		fixture.cargoRepository.cargo = null;

		assertFailureType(
				"UnknownCargoException",
				new FactoryCall(fixture) {
					@Override
					void invoke() throws Exception {
						fixture.factory.createHandlingEvent(
								new Date(), new Date(), new TrackingId("UNKNOWN"), null,
								SampleLocations.HONGKONG.getUnLocode(), HandlingEvent.Type.RECEIVE);
					}
				});
	}

	@Test
	public void factoryRejectsUnknownVoyage() throws Exception {
		final FactoryFixture fixture = new FactoryFixture();

		assertFailureType(
				"UnknownVoyageException",
				new FactoryCall(fixture) {
					@Override
					void invoke() throws Exception {
						fixture.factory.createHandlingEvent(
								new Date(), new Date(), fixture.cargo.getTrackingId(),
								new VoyageNumber("9999Z"), SampleLocations.HONGKONG.getUnLocode(),
								HandlingEvent.Type.LOAD);
					}
				});
	}

	@Test
	public void factoryRejectsUnknownLocation() throws Exception {
		final FactoryFixture fixture = new FactoryFixture();

		assertFailureType(
				"UnknownLocationException",
				new FactoryCall(fixture) {
					@Override
					void invoke() throws Exception {
						fixture.factory.createHandlingEvent(
								new Date(), new Date(), fixture.cargo.getTrackingId(), null,
								new UnLocode("ZZZZZ"), HandlingEvent.Type.RECEIVE);
					}
				});
	}

	@Test
	public void factoryRejectsLoadWithoutVoyage() throws Exception {
		final FactoryFixture fixture = new FactoryFixture();

		assertFailureType(
				CannotCreateHandlingEventException.class.getSimpleName(),
				new FactoryCall(fixture) {
					@Override
					void invoke() throws Exception {
						fixture.factory.createHandlingEvent(
								new Date(), new Date(), fixture.cargo.getTrackingId(), null,
								SampleLocations.HONGKONG.getUnLocode(), HandlingEvent.Type.LOAD);
					}
				});
	}

	@Test
	public void quirk94AttemptTtlIsOneSecond() throws Exception {
		final long[] observedTtl = { -1L };
		final JMSProducer producer = (JMSProducer) Proxy.newProxyInstance(
				JMSProducer.class.getClassLoader(), new Class<?>[] { JMSProducer.class },
				new InvocationHandler() {
					@Override
					public Object invoke(Object proxy, Method method, Object[] arguments) {
						if ("setTimeToLive".equals(method.getName())) {
							observedTtl[0] = ((Long) arguments[0]).longValue();
						}
						return method.getReturnType() == JMSProducer.class ? proxy : null;
					}
				});
		JMSContext context = (JMSContext) Proxy.newProxyInstance(
				JMSContext.class.getClassLoader(), new Class<?>[] { JMSContext.class },
				new InvocationHandler() {
					@Override
					public Object invoke(Object proxy, Method method, Object[] arguments) {
						return "createProducer".equals(method.getName()) ? producer : null;
					}
				});
		Destination destination = (Destination) Proxy.newProxyInstance(
				Destination.class.getClassLoader(), new Class<?>[] { Destination.class },
				new InvocationHandler() {
					@Override
					public Object invoke(Object proxy, Method method, Object[] arguments) {
						return null;
					}
				});

		JmsApplicationEvents events = new JmsApplicationEvents();
		setField(events, "jmsContext", context);
		setField(events, "handlingEventQueue", destination);
		setField(events, "logger", Logger.getAnonymousLogger());
		events.receivedHandlingEventRegistrationAttempt(new HandlingEventRegistrationAttempt(
				new Date(), new Date(), new TrackingId("ABC123"), null,
				HandlingEvent.Type.RECEIVE, SampleLocations.HONGKONG.getUnLocode()));

		assertEquals(1000L, observedTtl[0]);
		String webXml = new String(
				Files.readAllBytes(Paths.get("src/main/webapp/WEB-INF/web.xml")),
				StandardCharsets.UTF_8);
		assertTrue(webXml.contains("HandlingEventRegistrationAttemptQueue"));
	}

	private static void assertFailureType(String expected, FactoryCall call) throws Exception {
		try {
			call.invoke();
			fail("Expected " + expected);
		} catch (Exception error) {
			assertEquals(expected, error.getClass().getSimpleName());
		}
	}

	private abstract static class FactoryCall {
		FactoryCall(FactoryFixture fixture) {
		}

		abstract void invoke() throws Exception;
	}

	private static HandlingHistory history(HandlingEvent event) {
		return new HandlingHistory(Collections.singletonList(event));
	}

	private static HandlingEvent event(
			Cargo cargo, HandlingEvent.Type type, Location location, Voyage voyage) {
		if (voyage == null) {
			return new HandlingEvent(cargo, new Date(), new Date(), type, location);
		}
		return new HandlingEvent(cargo, new Date(), new Date(), type, location, voyage);
	}

	private static Cargo cargo() {
		Date now = new Date();
		Cargo cargo = new Cargo(
				new TrackingId("HR123"),
				new RouteSpecification(SampleLocations.HONGKONG, SampleLocations.HELSINKI,
						new Date(now.getTime() + 86400000L)));
		cargo.assignToRoute(new Itinerary(Arrays.asList(
				new Leg(SampleVoyages.HONGKONG_TO_NEW_YORK, SampleLocations.HONGKONG,
						SampleLocations.NEWYORK, now, new Date(now.getTime() + 86400000L)),
				new Leg(SampleVoyages.NEW_YORK_TO_DALLAS, SampleLocations.NEWYORK,
						SampleLocations.DALLAS, now, new Date(now.getTime() + 86400000L)),
				new Leg(SampleVoyages.DALLAS_TO_HELSINKI, SampleLocations.DALLAS,
						SampleLocations.HELSINKI, now, new Date(now.getTime() + 86400000L)))));
		return cargo;
	}

	private static void setField(Object target, String name, Object value) throws Exception {
		Field field = target.getClass().getDeclaredField(name);
		field.setAccessible(true);
		field.set(target, value);
	}

	private static class InspectionFixture {
		final FakeCargoRepository cargoRepository = new FakeCargoRepository();
		final FakeHandlingEventRepository handlingEventRepository;
		final RecordingApplicationEvents applicationEvents = new RecordingApplicationEvents();
		final List<Cargo> inspected = new ArrayList<Cargo>();
		final DefaultCargoInspectionService service = new DefaultCargoInspectionService();

		InspectionFixture(Cargo cargo, HandlingHistory history) {
			cargoRepository.cargo = cargo;
			handlingEventRepository = new FakeHandlingEventRepository(history);
			try {
				setField(service, "applicationEvents", applicationEvents);
				setField(service, "cargoRepository", cargoRepository);
				setField(service, "handlingEventRepository", handlingEventRepository);
				setField(service, "cargoInspected", inspectedEvent());
				setField(service, "logger", Logger.getAnonymousLogger());
			} catch (Exception error) {
				throw new AssertionError(error);
			}
		}

		@SuppressWarnings("unchecked")
		private Event<Cargo> inspectedEvent() {
			return (Event<Cargo>) Proxy.newProxyInstance(
					Event.class.getClassLoader(), new Class<?>[] { Event.class },
					new InvocationHandler() {
						@Override
						public Object invoke(Object proxy, Method method, Object[] arguments) {
							if ("fire".equals(method.getName())) {
								inspected.add((Cargo) arguments[0]);
							}
							return method.getReturnType().isInstance(proxy) ? proxy : null;
						}
					});
		}
	}

	private static class FactoryFixture {
		final Cargo cargo = cargo();
		final FakeCargoRepository cargoRepository = new FakeCargoRepository();
		final VoyageRepository voyageRepository = new VoyageRepository() {
			@Override
			public Voyage find(VoyageNumber voyageNumber) {
				return null;
			}

			@Override
			public List<Voyage> findAll() {
				return Collections.emptyList();
			}
		};
		final LocationRepository locationRepository = new LocationRepository() {
			@Override
			public Location find(UnLocode unLocode) {
				return "CNHKG".equals(unLocode.getIdString()) ? SampleLocations.HONGKONG : null;
			}

			@Override
			public List<Location> findAll() {
				return Collections.emptyList();
			}
		};
		final HandlingEventFactory factory = new HandlingEventFactory();

		FactoryFixture() throws Exception {
			cargoRepository.cargo = cargo;
			setField(factory, "cargoRepository", cargoRepository);
			setField(factory, "voyageRepository", voyageRepository);
			setField(factory, "locationRepository", locationRepository);
		}
	}

	private static class FakeCargoRepository implements CargoRepository {
		Cargo cargo;
		int stores;

		@Override
		public Cargo find(TrackingId trackingId) {
			return cargo != null && cargo.getTrackingId().equals(trackingId) ? cargo : null;
		}

		@Override
		public List<Cargo> findAll() {
			return cargo == null ? Collections.<Cargo>emptyList() : Collections.singletonList(cargo);
		}

		@Override
		public void store(Cargo value) {
			stores++;
		}

		@Override
		public TrackingId nextTrackingId() {
			return new TrackingId("NEXT");
		}
	}

	private static class FakeHandlingEventRepository implements HandlingEventRepository {
		final HandlingHistory history;
		int lookups;

		FakeHandlingEventRepository(HandlingHistory history) {
			this.history = history;
		}

		@Override
		public void store(HandlingEvent event) {
		}

		@Override
		public HandlingHistory lookupHandlingHistoryOfCargo(TrackingId trackingId) {
			lookups++;
			return history;
		}
	}

	private static class RecordingApplicationEvents implements ApplicationEvents {
		int misdirected;
		int arrived;

		@Override
		public void cargoWasHandled(HandlingEvent event) {
		}

		@Override
		public void cargoWasMisdirected(Cargo cargo) {
			misdirected++;
		}

		@Override
		public void cargoHasArrived(Cargo cargo) {
			arrived++;
		}

		@Override
		public void receivedHandlingEventRegistrationAttempt(HandlingEventRegistrationAttempt attempt) {
		}
	}
}
