# Surviving mutants: BK-ACCEPT

Written by `afs-mutation` on its last run (base `all`): score 0.931, threshold 0.8, killed 2065, survived 153. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/data_migration/loader.py:52 Mutant #49`

  ```diff
  @@ -49,7 +49,7 @@
               return False
           raise DataLoadError(f'not a boolean: {value!r}')
       if transform in ('timestamp', 'date'):
  -        if transform == 'date' and len(value.strip()) <= 10:
  +        if transform == 'date' and len(value.strip()) <= 11:
               parsed = datetime.date.fromisoformat(value.strip())
               return parsed
           try:
  ```

- `src/cargotracker/data_migration/loader.py:90 Mutant #81`

  ```diff
  @@ -87,7 +87,7 @@
               transform = definition.get('as', 'identity')
           else:
               source_column = definition
  -            transform = 'identity'
  +            transform = None
           if not isinstance(source_column, str):
               raise DataLoadError(f'{target_column}: mapping must name a source column')
           result.append((target_column, source_column, transform))
  ```

- `src/cargotracker/data_migration/loader.py:101 Mutant #86`

  ```diff
  @@ -98,7 +98,7 @@
       return {
           model._meta.db_table: model
           for model in apps.get_models()
  -        if not model._meta.proxy and not model._meta.auto_created
  +        if not model._meta.proxy or not model._meta.auto_created
       }
  ```

- `src/cargotracker/data_migration/loader.py:218 Mutant #207`

  ```diff
  @@ -213,8 +213,7 @@
                       f'{entry["spec"]["target"]}.{column}: reference does not match the model'
                   )
               if not any(
  -                candidate.column == referenced_column
  -                or candidate.name == referenced_column
  +                candidate.column == referenced_column and candidate.name == referenced_column
                   or candidate.attname == referenced_column
                   for candidate in referenced_entry['model']._meta.concrete_fields
               ):
  ```

- `src/cargotracker/data_migration/loader.py:233 Mutant #218`

  ```diff
  @@ -230,7 +230,7 @@
       for index, entry in enumerate(prepared):
           model = entry['model']
           for column, reference in entry['refs'].items():
  -            if reference['target_index'] > index:
  +            if reference['target_index'] >= index:
                   if not reference['field'].null:
                       raise DataLoadError(
                           f'{entry["spec"]["target"]}.{column}: a forward reference must be nullable'
  ```

- `src/cargotracker/data_migration/loader.py:266 Mutant #251`

  ```diff
  @@ -263,7 +263,7 @@
               field = entry['fields'][target_column]
               value = _transform(row[source_column], transform, timezone)
               reference = entry['refs'].get(target_column)
  -            if reference and reference['target_index'] > index and value is not None:
  +            if reference and reference['target_index'] >= index and value is not None:
                   pending.append((model, values, field, value))
                   value = None
               values[field.attname] = value
  ```

- `src/cargotracker/data_migration/loader.py:268 Mutant #254`

  ```diff
  @@ -265,7 +265,7 @@
               reference = entry['refs'].get(target_column)
               if reference and reference['target_index'] > index and value is not None:
                   pending.append((model, values, field, value))
  -                value = None
  +                value = ""
               values[field.attname] = value
           if values[model._meta.pk.attname] is None:
               raise DataLoadError(f'{spec["source"]}: primary key cannot be NULL')
  ```

- `src/cargotracker/data_migration/loader.py:273 Mutant #259`

  ```diff
  @@ -270,7 +270,7 @@
           if values[model._meta.pk.attname] is None:
               raise DataLoadError(f'{spec["source"]}: primary key cannot be NULL')
           objects.append(model(**values))
  -    model._base_manager.bulk_create(objects, batch_size=1000)
  +    model._base_manager.bulk_create(objects, batch_size=1001)
       return spec['target'], len(source_rows)
  ```

- `src/cargotracker/data_migration/exporter.py:59 Mutant #328`

  ```diff
  @@ -56,7 +56,7 @@
                   'model': model,
                   'columns': list(columns),
                   'fields': fields,
  -                'key_fields': key_fields,
  +                'XXkey_fieldsXX': key_fields,
               }
           )
       return prepared
  ```

- `src/cargotracker/data_migration/exporter.py:95 Mutant #355`

  ```diff
  @@ -92,7 +92,7 @@
           with path.open('w', newline='', encoding='utf-8') as stream:
               writer = csv.writer(stream)
               writer.writerow(table['columns'])
  -            rows = model._base_manager.order_by(*ordering).iterator(chunk_size=1000)
  +            rows = model._base_manager.order_by(*ordering).iterator(chunk_size=1001)
               writer.writerows(
                   [
                       _format_value(getattr(row, table['fields'][column].attname), timezone)
  ```

- `src/cargotracker/handling/infrastructure/attempt_submission_repository.py:16 Mutant #379`

  ```diff
  @@ -13,7 +13,7 @@
   class DjangoAttemptSubmissionRepository(RegistrationAttemptRepository):
       def submit(self, attempt: RegistrationAttempt) -> RegistrationAttempt:
           if attempt.id is not None or attempt.status is not RegistrationAttemptStatus.ACCEPTED:
  -            raise ValueError('Only a new registration attempt can be submitted')
  +            raise ValueError('XXOnly a new registration attempt can be submittedXX')
           record = RegistrationAttemptRecord.objects.create(
               tracking_id=attempt.tracking_id.value,
  ```

- `src/cargotracker/handling/infrastructure/attempt_submission_repository.py:43 Mutant #387`

  ```diff
  @@ -40,7 +40,7 @@
       def mark_rejected(self, attempt_id: int, reason: str) -> None:
           if not isinstance(reason, str) or not reason.strip():
  -            raise ValueError('A rejected registration attempt requires a reason')
  +            raise ValueError('XXA rejected registration attempt requires a reasonXX')
           self._mark_terminal(attempt_id, RegistrationAttemptStatus.REJECTED, reason)
       @staticmethod
  ```

- `src/cargotracker/handling/infrastructure/attempt_submission_repository.py:54 Mutant #392`

  ```diff
  @@ -51,7 +51,7 @@
               pk=attempt_id, status=RegistrationAttemptStatus.ACCEPTED.value
           ).update(status=status.value, rejection_reason=reason)
           if updated != 1:
  -            raise ValueError(f'Registration attempt {attempt_id} is not accepted')
  +            raise ValueError(f'XXRegistration attempt {attempt_id} is not acceptedXX')
       @staticmethod
       def _to_domain(record: RegistrationAttemptRecord) -> RegistrationAttempt:
  ```

- `src/cargotracker/pathfinder/application/routing.py:44 Mutant #428`

  ```diff
  @@ -41,7 +41,7 @@
               self._random_source.shuffle(available_ports)
               intermediate_count = (
                   self._random_source.randint(1, 5)
  -                if len(available_ports) > 4
  +                if len(available_ports) >= 4
                   else len(available_ports)
               )
               available_ports = available_ports[:intermediate_count]
  ```

- `src/cargotracker/pathfinder/application/routing.py:72 Mutant #441`

  ```diff
  @@ -69,7 +69,7 @@
           return tuple(paths)
       def _next_date(self, value: datetime) -> datetime:
  -        return value + timedelta(days=1, hours=self._random_source.randint(-8, 8))
  +        return value + timedelta(days=1, hours=self._random_source.randint(+8, 8))
   def _as_utc(value: datetime) -> datetime:
  ```

- `src/cargotracker/pathfinder/application/routing.py:72 Mutant #442`

  ```diff
  @@ -69,7 +69,7 @@
           return tuple(paths)
       def _next_date(self, value: datetime) -> datetime:
  -        return value + timedelta(days=1, hours=self._random_source.randint(-8, 8))
  +        return value + timedelta(days=1, hours=self._random_source.randint(-9, 8))
   def _as_utc(value: datetime) -> datetime:
  ```

- `src/cargotracker/pathfinder/interfaces/api.py:12 Mutant #450`

  ```diff
  @@ -8,8 +8,6 @@
   routing_service = RoutingService()
  -
  -@require_GET
   def shortest_path(request: HttpRequest) -> HttpResponse:
       origin = request.GET.get('origin')
       if origin is None or len(origin) != 5:
  ```

- `src/cargotracker/pathfinder/interfaces/api.py:59 Mutant #487`

  ```diff
  @@ -56,6 +56,6 @@
   def _format_route_date(value: datetime) -> str:
  -    utc_value = value.replace(tzinfo=UTC) if value.utcoffset() is None else value.astimezone(UTC)
  +    utc_value = value.replace(tzinfo=UTC) if value.utcoffset() is not None else value.astimezone(UTC)
       return utc_value.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
  ```

- `src/cargotracker/cargo/domain/route_specification.py:26 Mutant #500`

  ```diff
  @@ -23,7 +23,7 @@
           if self.origin == self.destination:
               raise ValueError("Origin and destination can't be the same")
           object.__setattr__(
  -            self, 'arrival_deadline', as_utc(self.arrival_deadline, 'arrival deadline')
  +            self, 'XXarrival_deadlineXX', as_utc(self.arrival_deadline, 'arrival deadline')
           )
       def is_satisfied_by(self, itinerary: 'Itinerary') -> bool:
  ```

- `src/cargotracker/cargo/management/commands/seed_sample_data.py:15 Mutant #513`

  ```diff
  @@ -12,7 +12,7 @@
   class Command(BaseCommand):
  -    help = 'Seed the characterized Cargo Tracker sample data.'
  +    help = 'XXSeed the characterized Cargo Tracker sample data.XX'
       @transaction.atomic
       def handle(self, *args, **options):
  ```

- `src/cargotracker/cargo/management/commands/seed_sample_data.py:15 Mutant #514`

  ```diff
  @@ -12,7 +12,7 @@
   class Command(BaseCommand):
  -    help = 'Seed the characterized Cargo Tracker sample data.'
  +    help = None
       @transaction.atomic
       def handle(self, *args, **options):
  ```

- `src/cargotracker/cargo/management/commands/seed_sample_data.py:17 Mutant #515`

  ```diff
  @@ -14,7 +14,6 @@
   class Command(BaseCommand):
       help = 'Seed the characterized Cargo Tracker sample data.'
  -    @transaction.atomic
       def handle(self, *args, **options):
           today = timezone.now().astimezone(UTC).date()
           SampleDataSeeder(
  ```

- `src/cargotracker/cargo/management/commands/seed_sample_data.py:26 Mutant #517`

  ```diff
  @@ -23,5 +23,5 @@
               DjangoCargoRepository(),
               DjangoHandlingEventRepository(),
           ).seed(today)
  -        self.stdout.write(self.style.SUCCESS('Seeded characterized sample data.'))
  +        self.stdout.write(self.style.SUCCESS('XXSeeded characterized sample data.XX'))
  ```

- `src/cargotracker/cargo/domain/handling_activity.py:22 Mutant #537`

  ```diff
  @@ -19,7 +19,7 @@
           if not isinstance(self.event_type, str):
               raise TypeError('A handling activity requires an event type')
           if not isinstance(self.location, Location):
  -            raise TypeError('A handling activity requires a location')
  +            raise TypeError('XXA handling activity requires a locationXX')
           if self.voyage is not None and not isinstance(self.voyage, Voyage):
               raise TypeError('A handling activity voyage must be a voyage')
  ```

- `src/cargotracker/cargo/domain/handling_activity.py:24 Mutant #541`

  ```diff
  @@ -21,7 +21,7 @@
           if not isinstance(self.location, Location):
               raise TypeError('A handling activity requires a location')
           if self.voyage is not None and not isinstance(self.voyage, Voyage):
  -            raise TypeError('A handling activity voyage must be a voyage')
  +            raise TypeError('XXA handling activity voyage must be a voyageXX')
   HandlingActivity.EMPTY = HandlingActivity()
  ```

- `src/cargotracker/location/domain/un_locode.py:16 Mutant #568`

  ```diff
  @@ -13,7 +13,7 @@
               raise TypeError('A UN/LOCODE must be a string')
           if not _VALID_UN_LOCODE.fullmatch(self.value):
               raise ValueError(f'{self.value!r} is not a valid UN/LOCODE')
  -        object.__setattr__(self, 'value', self.value.upper())
  +        object.__setattr__(self, 'XXvalueXX', self.value.upper())
       def __str__(self):
           return self.value
  ```

- `src/cargotracker/cargo/domain/delivery.py:76 Mutant #27`

  ```diff
  @@ -73,7 +73,6 @@
               calculated_at=cls._calculate_time(calculated_at),
           )
  -    @staticmethod
       def _validate_derivation_inputs(
           route_specification: RouteSpecification,
           itinerary: Itinerary,
  ```

- `src/cargotracker/cargo/domain/delivery.py:85 Mutant #29`

  ```diff
  @@ -82,7 +82,7 @@
           from cargotracker.handling.domain.handling_history import HandlingHistory
           if not isinstance(route_specification, RouteSpecification):
  -            raise TypeError('A delivery requires a route specification')
  +            raise TypeError('XXA delivery requires a route specificationXX')
           if not isinstance(itinerary, Itinerary):
               raise TypeError('A delivery requires an itinerary')
           if not isinstance(handling_history, HandlingHistory):
  ```

- `src/cargotracker/cargo/domain/delivery.py:87 Mutant #31`

  ```diff
  @@ -84,7 +84,7 @@
           if not isinstance(route_specification, RouteSpecification):
               raise TypeError('A delivery requires a route specification')
           if not isinstance(itinerary, Itinerary):
  -            raise TypeError('A delivery requires an itinerary')
  +            raise TypeError('XXA delivery requires an itineraryXX')
           if not isinstance(handling_history, HandlingHistory):
               raise TypeError('A delivery requires a handling history')
  ```

- `src/cargotracker/cargo/domain/delivery.py:89 Mutant #33`

  ```diff
  @@ -86,7 +86,7 @@
           if not isinstance(itinerary, Itinerary):
               raise TypeError('A delivery requires an itinerary')
           if not isinstance(handling_history, HandlingHistory):
  -            raise TypeError('A delivery requires a handling history')
  +            raise TypeError('XXA delivery requires a handling historyXX')
       @staticmethod
       def _calculate_time(calculated_at: datetime | None) -> datetime:
  ```

- `src/cargotracker/cargo/domain/delivery.py:91 Mutant #34`

  ```diff
  @@ -88,7 +88,6 @@
           if not isinstance(handling_history, HandlingHistory):
               raise TypeError('A delivery requires a handling history')
  -    @staticmethod
       def _calculate_time(calculated_at: datetime | None) -> datetime:
           return calculated_at if calculated_at is not None else datetime.now(UTC)
  ```

- `src/cargotracker/cargo/domain/delivery.py:95 Mutant #36`

  ```diff
  @@ -92,7 +92,6 @@
       def _calculate_time(calculated_at: datetime | None) -> datetime:
           return calculated_at if calculated_at is not None else datetime.now(UTC)
  -    @staticmethod
       def _calculate_last_known_location(latest_event: 'HandlingEvent | None') -> Location | None:
           return latest_event.location if latest_event is not None else None
  ```

- `src/cargotracker/cargo/domain/delivery.py:99 Mutant #38`

  ```diff
  @@ -96,7 +96,6 @@
       def _calculate_last_known_location(latest_event: 'HandlingEvent | None') -> Location | None:
           return latest_event.location if latest_event is not None else None
  -    @staticmethod
       def _calculate_current_voyage(
           transport_status: TransportStatus, latest_event: 'HandlingEvent | None'
       ) -> Voyage | None:
  ```

- `src/cargotracker/cargo/domain/delivery.py:105 Mutant #40`

  ```diff
  @@ -102,7 +102,6 @@
       ) -> Voyage | None:
           return latest_event.voyage if transport_status is TransportStatus.ONBOARD_CARRIER else None
  -    @staticmethod
       def _is_on_track(routing_status: RoutingStatus, misdirected: bool) -> bool:
           return routing_status is RoutingStatus.ROUTED and not misdirected
  ```

- `src/cargotracker/cargo/domain/delivery.py:121 Mutant #57`

  ```diff
  @@ -118,7 +118,7 @@
           if not isinstance(self.misdirected, bool):
               raise TypeError('A delivery misdirected flag must be a boolean')
           if self.eta is not None:
  -            object.__setattr__(self, 'eta', as_utc(self.eta, 'ETA'))
  +            object.__setattr__(self, 'XXetaXX', as_utc(self.eta, 'ETA'))
           if not isinstance(self.next_expected_activity, HandlingActivity):
               raise TypeError('A delivery requires a next expected activity')
           if not isinstance(self.unloaded_at_destination, bool):
  ```

- `src/cargotracker/cargo/domain/delivery.py:128 Mutant #65`

  ```diff
  @@ -125,7 +125,7 @@
               raise TypeError('A delivery unloaded-at-destination flag must be a boolean')
           if not isinstance(self.routing_status, RoutingStatus):
               raise TypeError('A delivery requires a routing status')
  -        object.__setattr__(self, 'calculated_at', as_utc(self.calculated_at, 'calculated time'))
  +        object.__setattr__(self, 'XXcalculated_atXX', as_utc(self.calculated_at, 'calculated time'))
           if self.last_event_id is not None and (
               not isinstance(self.last_event_id, int) or isinstance(self.last_event_id, bool)
           ):
  ```

- `src/cargotracker/cargo/domain/delivery.py:134 Mutant #72`

  ```diff
  @@ -131,7 +131,6 @@
           ):
               raise TypeError('A delivery last event ID must be an integer')
  -    @staticmethod
       def _calculate_transport_status(latest_event: 'HandlingEvent | None') -> TransportStatus:
           if latest_event is None:
               return TransportStatus.NOT_RECEIVED
  ```

- `src/cargotracker/cargo/domain/delivery.py:146 Mutant #79`

  ```diff
  @@ -143,7 +143,6 @@
               'CLAIM': TransportStatus.CLAIMED,
           }.get(latest_event.event_type, TransportStatus.UNKNOWN)
  -    @staticmethod
       def _calculate_misdirection_status(
           itinerary: Itinerary, latest_event: 'HandlingEvent | None'
       ) -> bool:
  ```

- `src/cargotracker/cargo/domain/delivery.py:152 Mutant #83`

  ```diff
  @@ -149,7 +149,6 @@
       ) -> bool:
           return latest_event is not None and not itinerary.is_expected(latest_event)
  -    @staticmethod
       def _calculate_routing_status(
           route_specification: RouteSpecification, itinerary: Itinerary
       ) -> RoutingStatus:
  ```

- `src/cargotracker/cargo/domain/delivery.py:162 Mutant #85`

  ```diff
  @@ -159,7 +159,6 @@
               return RoutingStatus.ROUTED
           return RoutingStatus.MISROUTED
  -    @staticmethod
       def _calculate_eta(itinerary: Itinerary, on_track: bool) -> datetime | None:
           return itinerary.legs[-1].unload_time if on_track else None
  ```

- `src/cargotracker/cargo/domain/delivery.py:190 Mutant #98`

  ```diff
  @@ -187,7 +187,6 @@
               else HandlingActivity.EMPTY
           )
  -    @staticmethod
       def _after_receive(itinerary: Itinerary, _latest_event: 'HandlingEvent') -> HandlingActivity:
           first_leg = itinerary.legs[0]
           return HandlingActivity('LOAD', first_leg.load_location, first_leg.voyage)
  ```

- `src/cargotracker/cargo/domain/delivery.py:195 Mutant #102`

  ```diff
  @@ -192,7 +192,6 @@
           first_leg = itinerary.legs[0]
           return HandlingActivity('LOAD', first_leg.load_location, first_leg.voyage)
  -    @staticmethod
       def _after_load(itinerary: Itinerary, latest_event: 'HandlingEvent') -> HandlingActivity:
           leg = next(
               (leg for leg in itinerary.legs if leg.load_location == latest_event.location),
  ```

- `src/cargotracker/cargo/domain/delivery.py:205 Mutant #107`

  ```diff
  @@ -202,7 +202,6 @@
               return HandlingActivity.EMPTY
           return HandlingActivity('UNLOAD', leg.unload_location, leg.voyage)
  -    @staticmethod
       def _after_unload(itinerary: Itinerary, latest_event: 'HandlingEvent') -> HandlingActivity:
           for index, leg in enumerate(itinerary.legs):
               if leg.unload_location == latest_event.location:
  ```

- `src/cargotracker/cargo/domain/delivery.py:215 Mutant #117`

  ```diff
  @@ -212,7 +212,6 @@
                   return HandlingActivity('CLAIM', leg.unload_location)
           return HandlingActivity.EMPTY
  -    @staticmethod
       def _calculate_unloaded_at_destination(
           route_specification: RouteSpecification, latest_event: 'HandlingEvent | None'
       ) -> bool:
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:22 Mutant #123`

  ```diff
  @@ -19,7 +19,7 @@
   from cargotracker.voyage.domain.voyage import Voyage
   from cargotracker.voyage.domain.voyage_number import VoyageNumber
  -_CANDIDATE_SALT = 'booking.route_selection'
  +_CANDIDATE_SALT = 'XXbooking.route_selectionXX'
   def create_route_selection_views(
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:22 Mutant #124`

  ```diff
  @@ -19,7 +19,7 @@
   from cargotracker.voyage.domain.voyage import Voyage
   from cargotracker.voyage.domain.voyage_number import VoyageNumber
  -_CANDIDATE_SALT = 'booking.route_selection'
  +_CANDIDATE_SALT = None
   def create_route_selection_views(
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:34 Mutant #132`

  ```diff
  @@ -31,7 +31,7 @@
           if request.method == 'POST':
               cargo = cargo_dashboard.get_cargo_details(TrackingId(tracking_id))
               if cargo is None:
  -                raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +                raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
               itinerary = _selected_itinerary(request, tracking_id)
               if not cargo.route_specification.is_satisfied_by(itinerary):
                   raise Http404('The selected route no longer satisfies the route specification.')
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:37 Mutant #135`

  ```diff
  @@ -34,7 +34,7 @@
                   raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
               itinerary = _selected_itinerary(request, tracking_id)
               if not cargo.route_specification.is_satisfied_by(itinerary):
  -                raise Http404('The selected route no longer satisfies the route specification.')
  +                raise Http404('XXThe selected route no longer satisfies the route specification.XX')
               cargo_routing.assign_route(TrackingId(tracking_id), itinerary)
               return redirect(f'/admin/cargo/{quote(tracking_id, safe="")}/')
           context = _selection_context(
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:39 Mutant #136`

  ```diff
  @@ -36,7 +36,7 @@
               if not cargo.route_specification.is_satisfied_by(itinerary):
                   raise Http404('The selected route no longer satisfies the route specification.')
               cargo_routing.assign_route(TrackingId(tracking_id), itinerary)
  -            return redirect(f'/admin/cargo/{quote(tracking_id, safe="")}/')
  +            return redirect(f'/admin/cargo/{quote(tracking_id, safe="XXXX")}/')
           context = _selection_context(
               cargo_routing,
               cargo_dashboard,
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:70 Mutant #149`

  ```diff
  @@ -67,7 +67,7 @@
       tracking_id = TrackingId(tracking_id_value)
       cargo = cargo_dashboard.get_cargo_details(tracking_id)
       if cargo is None:
  -        raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +        raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
       itineraries = cargo_routing.route_candidates(tracking_id)
       return {
           'cargo': cargo,
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:95 Mutant #162`

  ```diff
  @@ -92,7 +92,7 @@
   def _selected_itinerary(request: HttpRequest, tracking_id: str) -> Itinerary:
       try:
  -        candidate = signing.loads(request.POST.get('candidate', ''), salt=_CANDIDATE_SALT)
  +        candidate = signing.loads(request.POST.get('candidate', 'XXXX'), salt=_CANDIDATE_SALT)
           if candidate['tracking_id'] != tracking_id:
               raise BadSignature('Candidate belongs to another cargo.')
           return _deserialize_itinerary(candidate['legs'])
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:97 Mutant #166`

  ```diff
  @@ -94,7 +94,7 @@
       try:
           candidate = signing.loads(request.POST.get('candidate', ''), salt=_CANDIDATE_SALT)
           if candidate['tracking_id'] != tracking_id:
  -            raise BadSignature('Candidate belongs to another cargo.')
  +            raise BadSignature('XXCandidate belongs to another cargo.XX')
           return _deserialize_itinerary(candidate['legs'])
       except (BadSignature, KeyError, TypeError, ValueError) as error:
           raise Http404('The selected route is invalid.') from error
  ```

- `src/cargotracker/booking/interfaces/route_selection/views.py:100 Mutant #168`

  ```diff
  @@ -97,7 +97,7 @@
               raise BadSignature('Candidate belongs to another cargo.')
           return _deserialize_itinerary(candidate['legs'])
       except (BadSignature, KeyError, TypeError, ValueError) as error:
  -        raise Http404('The selected route is invalid.') from error
  +        raise Http404('XXThe selected route is invalid.XX') from error
   def _serialize_itinerary(itinerary: Itinerary) -> list[dict]:
  ```

- `src/cargotracker/booking/application/routing.py:66 Mutant #211`

  ```diff
  @@ -63,7 +63,7 @@
       def _find_cargo(self, tracking_id: TrackingId) -> Cargo:
           cargo = self._cargo_repository.find(tracking_id)
           if cargo is None:
  -            raise Http404(f'Cargo with tracking ID {tracking_id} not found.')
  +            raise Http404(f'XXCargo with tracking ID {tracking_id} not found.XX')
           return cargo
       def _to_itinerary(self, path: TransitPath) -> Itinerary:
  ```

- `src/cargotracker/handling/domain/handling_history.py:8 Mutant #213`

  ```diff
  @@ -5,7 +5,7 @@
   from cargotracker.handling.domain.handling_event import HandlingEvent
  -@dataclass(frozen=True, init=False)
  +@dataclass(frozen=True, init=True)
   class HandlingHistory:
       events: tuple[HandlingEvent, ...]
       _event_ids: tuple[int | None, ...] = field(compare=False, repr=False)
  ```

- `src/cargotracker/handling/domain/handling_history.py:21 Mutant #220`

  ```diff
  @@ -18,7 +18,7 @@
           event_ids: Iterable[int | None] | None = None,
       ):
           if events is None:
  -            raise TypeError('Handling events are required')
  +            raise TypeError('XXHandling events are requiredXX')
           handling_events = tuple(events)
           if any(not isinstance(event, HandlingEvent) for event in handling_events):
               raise TypeError('Handling history requires handling events')
  ```

- `src/cargotracker/handling/domain/handling_history.py:24 Mutant #223`

  ```diff
  @@ -21,7 +21,7 @@
               raise TypeError('Handling events are required')
           handling_events = tuple(events)
           if any(not isinstance(event, HandlingEvent) for event in handling_events):
  -            raise TypeError('Handling history requires handling events')
  +            raise TypeError('XXHandling history requires handling eventsXX')
           identifiers = tuple(event_ids) if event_ids is not None else (None,) * len(handling_events)
           if len(identifiers) != len(handling_events):
               raise ValueError('Handling event IDs must match the history events')
  ```

- `src/cargotracker/handling/domain/handling_history.py:35 Mutant #237`

  ```diff
  @@ -32,7 +32,7 @@
           ):
               raise ValueError('Handling event IDs must be positive integers')
           distinct_events = {}
  -        for event, identifier in zip(handling_events, identifiers, strict=True):
  +        for event, identifier in zip(handling_events, identifiers, strict=False):
               current = distinct_events.get(event)
               if current is None or (identifier or 0) > (current[1] or 0):
                   distinct_events[event] = (event, identifier)
  ```

- `src/cargotracker/handling/domain/handling_history.py:36 Mutant #238`

  ```diff
  @@ -33,7 +33,7 @@
               raise ValueError('Handling event IDs must be positive integers')
           distinct_events = {}
           for event, identifier in zip(handling_events, identifiers, strict=True):
  -            current = distinct_events.get(event)
  +            current = None
               if current is None or (identifier or 0) > (current[1] or 0):
                   distinct_events[event] = (event, identifier)
           ordered_events = sorted(
  ```

- `src/cargotracker/handling/domain/handling_history.py:37 Mutant #240`

  ```diff
  @@ -34,7 +34,7 @@
           distinct_events = {}
           for event, identifier in zip(handling_events, identifiers, strict=True):
               current = distinct_events.get(event)
  -            if current is None or (identifier or 0) > (current[1] or 0):
  +            if current is None or (identifier or 1) > (current[1] or 0):
                   distinct_events[event] = (event, identifier)
           ordered_events = sorted(
               distinct_events.values(),
  ```

- `src/cargotracker/handling/domain/handling_history.py:37 Mutant #242`

  ```diff
  @@ -34,7 +34,7 @@
           distinct_events = {}
           for event, identifier in zip(handling_events, identifiers, strict=True):
               current = distinct_events.get(event)
  -            if current is None or (identifier or 0) > (current[1] or 0):
  +            if current is None or (identifier or 0) >= (current[1] or 0):
                   distinct_events[event] = (event, identifier)
           ordered_events = sorted(
               distinct_events.values(),
  ```

- `src/cargotracker/handling/domain/handling_history.py:37 Mutant #244`

  ```diff
  @@ -34,7 +34,7 @@
           distinct_events = {}
           for event, identifier in zip(handling_events, identifiers, strict=True):
               current = distinct_events.get(event)
  -            if current is None or (identifier or 0) > (current[1] or 0):
  +            if current is None or (identifier or 0) > (current[1] or 1):
                   distinct_events[event] = (event, identifier)
           ordered_events = sorted(
               distinct_events.values(),
  ```

- `src/cargotracker/handling/domain/handling_history.py:44 Mutant #251`

  ```diff
  @@ -41,7 +41,7 @@
               key=lambda item: (
                   item[0].completion_time,
                   item[0].registration_time,
  -                item[1] or 0,
  +                item[1] or 1,
               ),
           )
           object.__setattr__(self, 'events', tuple(event for event, _ in ordered_events))
  ```

- `src/cargotracker/handling/management/commands/process_handling_attempts.py:18 Mutant #284`

  ```diff
  @@ -15,7 +15,7 @@
   class Command(BaseCommand):
  -    help = 'Process accepted handling registration attempts.'
  +    help = 'XXProcess accepted handling registration attempts.XX'
       def handle(self, *args, **options):
           poll_seconds = float(os.environ.get('HANDLING_ATTEMPT_POLL_SECONDS', '1'))
  ```

- `src/cargotracker/handling/management/commands/process_handling_attempts.py:18 Mutant #285`

  ```diff
  @@ -15,7 +15,7 @@
   class Command(BaseCommand):
  -    help = 'Process accepted handling registration attempts.'
  +    help = None
       def handle(self, *args, **options):
           poll_seconds = float(os.environ.get('HANDLING_ATTEMPT_POLL_SECONDS', '1'))
  ```

- `src/cargotracker/handling/management/commands/process_handling_attempts.py:23 Mutant #293`

  ```diff
  @@ -20,7 +20,7 @@
       def handle(self, *args, **options):
           poll_seconds = float(os.environ.get('HANDLING_ATTEMPT_POLL_SECONDS', '1'))
           if not isfinite(poll_seconds) or poll_seconds <= 0:
  -            raise CommandError('HANDLING_ATTEMPT_POLL_SECONDS must be greater than zero')
  +            raise CommandError('XXHANDLING_ATTEMPT_POLL_SECONDS must be greater than zeroXX')
           try:
               retry_backoff_seconds = float(
                   os.environ.get('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS', '1')
  ```

- `src/cargotracker/handling/management/commands/process_handling_attempts.py:30 Mutant #297`

  ```diff
  @@ -27,7 +27,7 @@
               )
           except ValueError as error:
               raise CommandError(
  -                'HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be a positive number'
  +                'XXHANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be a positive numberXX'
               ) from error
           if not isfinite(retry_backoff_seconds) or retry_backoff_seconds <= 0:
               raise CommandError('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be greater than zero')
  ```

- `src/cargotracker/handling/management/commands/process_handling_attempts.py:33 Mutant #302`

  ```diff
  @@ -30,7 +30,7 @@
                   'HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be a positive number'
               ) from error
           if not isfinite(retry_backoff_seconds) or retry_backoff_seconds <= 0:
  -            raise CommandError('HANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be greater than zero')
  +            raise CommandError('XXHANDLING_ATTEMPT_RETRY_BACKOFF_SECONDS must be greater than zeroXX')
           repositories = (
               DjangoAttemptProcessingRepository(),
               DjangoCargoRepository(),
  ```

- `src/cargotracker/handling/management/commands/process_handling_attempts.py:40 Mutant #305`

  ```diff
  @@ -37,7 +37,7 @@
               DjangoHandlingEventRepository(),
           )
           while True:
  -            if not process_registration_attempt(
  +            if  process_registration_attempt(
                   *repositories,
                   retry_backoff_seconds=retry_backoff_seconds,
               ):
  ```

- `src/cargotracker/cargo/domain/cargo.py:10 Mutant #307`

  ```diff
  @@ -7,7 +7,7 @@
   from cargotracker.location.domain.location import Location
  -@dataclass(eq=False)
  +@dataclass(eq=True)
   class Cargo:
       tracking_id: TrackingId
       route_specification: RouteSpecification
  ```

- `src/cargotracker/cargo/interfaces/tracking/history.py:6 Mutant #334`

  ```diff
  @@ -3,7 +3,7 @@
   from cargotracker.handling.domain.handling_history import HandlingHistory
   _EVENT_DESCRIPTIONS = {
  -    HandlingEventType.RECEIVE: 'Received in {location}',
  +    HandlingEventType.RECEIVE: 'XXReceived in {location}XX',
       HandlingEventType.LOAD: 'Loaded onto voyage {voyage} in {location}',
       HandlingEventType.UNLOAD: 'Unloaded off voyage {voyage} in {location}',
       HandlingEventType.CLAIM: 'Claimed in {location}',
  ```

- `src/cargotracker/cargo/interfaces/tracking/history.py:7 Mutant #335`

  ```diff
  @@ -4,7 +4,7 @@
   _EVENT_DESCRIPTIONS = {
       HandlingEventType.RECEIVE: 'Received in {location}',
  -    HandlingEventType.LOAD: 'Loaded onto voyage {voyage} in {location}',
  +    HandlingEventType.LOAD: 'XXLoaded onto voyage {voyage} in {location}XX',
       HandlingEventType.UNLOAD: 'Unloaded off voyage {voyage} in {location}',
       HandlingEventType.CLAIM: 'Claimed in {location}',
       HandlingEventType.CUSTOMS: 'Cleared customs in {location}',
  ```

- `src/cargotracker/cargo/interfaces/tracking/history.py:8 Mutant #336`

  ```diff
  @@ -5,7 +5,7 @@
   _EVENT_DESCRIPTIONS = {
       HandlingEventType.RECEIVE: 'Received in {location}',
       HandlingEventType.LOAD: 'Loaded onto voyage {voyage} in {location}',
  -    HandlingEventType.UNLOAD: 'Unloaded off voyage {voyage} in {location}',
  +    HandlingEventType.UNLOAD: 'XXUnloaded off voyage {voyage} in {location}XX',
       HandlingEventType.CLAIM: 'Claimed in {location}',
       HandlingEventType.CUSTOMS: 'Cleared customs in {location}',
   }
  ```

- `src/cargotracker/cargo/interfaces/tracking/history.py:9 Mutant #337`

  ```diff
  @@ -6,7 +6,7 @@
       HandlingEventType.RECEIVE: 'Received in {location}',
       HandlingEventType.LOAD: 'Loaded onto voyage {voyage} in {location}',
       HandlingEventType.UNLOAD: 'Unloaded off voyage {voyage} in {location}',
  -    HandlingEventType.CLAIM: 'Claimed in {location}',
  +    HandlingEventType.CLAIM: 'XXClaimed in {location}XX',
       HandlingEventType.CUSTOMS: 'Cleared customs in {location}',
   }
  ```

- `src/cargotracker/cargo/interfaces/tracking/history.py:10 Mutant #338`

  ```diff
  @@ -7,7 +7,7 @@
       HandlingEventType.LOAD: 'Loaded onto voyage {voyage} in {location}',
       HandlingEventType.UNLOAD: 'Unloaded off voyage {voyage} in {location}',
       HandlingEventType.CLAIM: 'Claimed in {location}',
  -    HandlingEventType.CUSTOMS: 'Cleared customs in {location}',
  +    HandlingEventType.CUSTOMS: 'XXCleared customs in {location}XX',
   }
  ```

- `src/cargotracker/cargo/interfaces/tracking/history.py:17 Mutant #341`

  ```diff
  @@ -14,7 +14,7 @@
   def get_event_description(event: HandlingEvent) -> str:
       return _EVENT_DESCRIPTIONS[event.event_type].format(
           location=event.location.name,
  -        voyage=event.voyage.voyage_number.value if event.voyage is not None else '',
  +        voyage=event.voyage.voyage_number.value if event.voyage is not None else 'XXXX',
       )
  ```

- `src/cargotracker/cargo/interfaces/tracking/map/adapter.py:24 Mutant #364`

  ```diff
  @@ -21,7 +21,7 @@
       if last_known_location is not None:
           locations['lastKnownLocation'] = last_known_location
       for role, location in locations.items():
  -        query[f'{role}Code'] = location.unlocode.value if location is not None else ''
  +        query[f'{role}Code'] = location.unlocode.value if location is not None else 'XXXX'
           query[f'{role}Name'] = location.name if location is not None else ''
       return f'{reverse("cargo_map_frame")}?{urlencode(query)}'
  ```

- `src/cargotracker/cargo/interfaces/tracking/map/adapter.py:25 Mutant #368`

  ```diff
  @@ -22,6 +22,6 @@
           locations['lastKnownLocation'] = last_known_location
       for role, location in locations.items():
           query[f'{role}Code'] = location.unlocode.value if location is not None else ''
  -        query[f'{role}Name'] = location.name if location is not None else ''
  +        query[f'{role}Name'] = location.name if location is not None else 'XXXX'
       return f'{reverse("cargo_map_frame")}?{urlencode(query)}'
  ```

- `src/cargotracker/voyage/domain/voyage.py:31 Mutant #381`

  ```diff
  @@ -28,5 +28,5 @@
           return f'Voyage {self.voyage_number}'
  -Voyage.NONE = Voyage(VoyageNumber(''), Schedule.EMPTY)
  +Voyage.NONE = Voyage(VoyageNumber('XXXX'), Schedule.EMPTY)
  ```

- `src/cargotracker/voyage/domain/voyage.py:31 Mutant #382`

  ```diff
  @@ -28,5 +28,5 @@
           return f'Voyage {self.voyage_number}'
  -Voyage.NONE = Voyage(VoyageNumber(''), Schedule.EMPTY)
  +Voyage.NONE = None
  ```

- `src/cargotracker/cargo/interfaces/tracking/next_activity.py:16 Mutant #396`

  ```diff
  @@ -13,7 +13,7 @@
           return None
       description = _ACTIVITY_DESCRIPTIONS[activity.event_type].format(
           location=activity.location.name,
  -        voyage=activity.voyage.voyage_number.value if activity.voyage is not None else '',
  +        voyage=activity.voyage.voyage_number.value if activity.voyage is not None else 'XXXX',
       )
       return f'Next expected activity is to {description}'
  ```

- `src/cargotracker/cargo/infrastructure/repository.py:112 Mutant #48`

  ```diff
  @@ -109,7 +109,7 @@
           event_type = record.next_expected_handling_event_type
           location = record.next_expected_location
           voyage = record.next_expected_voyage
  -        if event_type is None and location is None and voyage is None:
  +        if event_type is None or location is None and voyage is None:
               activity = HandlingActivity.EMPTY
           else:
               activity = HandlingActivity(
  ```

- `src/cargotracker/cargo/infrastructure/repository.py:156 Mutant #57`

  ```diff
  @@ -153,7 +153,7 @@
           if isinstance(value, datetime):
               return (
                   value.astimezone(UTC)
  -                if value.utcoffset() is not None
  +                if value.utcoffset() is  None
                   else value.replace(tzinfo=UTC)
               )
           return datetime.combine(value, time.min, tzinfo=UTC)
  ```

- `src/cargotracker/handling/application/process_registration_attempt.py:43 Mutant #80`

  ```diff
  @@ -40,7 +40,7 @@
       retry_backoff_seconds: float = 1.0,
   ) -> bool:
       if not isfinite(retry_backoff_seconds) or retry_backoff_seconds <= 0:
  -        raise ValueError('Retry backoff must be greater than zero')
  +        raise ValueError('XXRetry backoff must be greater than zeroXX')
       delay = min(retry_backoff_seconds, _MAX_RETRY_BACKOFF_SECONDS)
       retry_started = None
       error_logged = False
  ```

- `src/cargotracker/handling/application/process_registration_attempt.py:46 Mutant #84`

  ```diff
  @@ -43,7 +43,7 @@
           raise ValueError('Retry backoff must be greater than zero')
       delay = min(retry_backoff_seconds, _MAX_RETRY_BACKOFF_SECONDS)
       retry_started = None
  -    error_logged = False
  +    error_logged = None
       while True:
           try:
               return _process_registration_attempt_once(attempts, cargos, events)
  ```

- `src/cargotracker/handling/application/process_registration_attempt.py:56 Mutant #93`

  ```diff
  @@ -53,7 +53,7 @@
                   retry_started = now
               if now - retry_started >= _RETRY_LOG_AFTER_SECONDS and not error_logged:
                   logger.error(
  -                    'Handling attempt processing still failing after 15 minutes: %s', error
  +                    'XXHandling attempt processing still failing after 15 minutes: %sXX', error
                   )
                   error_logged = True
               sleep(delay)
  ```

- `src/cargotracker/handling/interfaces/rest.py:25 Mutant #133`

  ```diff
  @@ -22,7 +22,7 @@
           if value in self.empty_values:
               return self.empty_value
           if not isinstance(value, str):
  -            raise ValidationError('Enter a valid string.', code='invalid')
  +            raise ValidationError('Enter a valid string.', code='XXinvalidXX')
           return super().to_python(value)
  ```

- `src/cargotracker/handling/interfaces/rest.py:41 Mutant #159`

  ```diff
  @@ -38,7 +38,7 @@
           try:
               completion_time = datetime.strptime(value, '%Y-%m-%d %H:%M')
           except ValueError as exc:
  -            raise ValidationError('Enter a valid completion time.', code='invalid') from exc
  +            raise ValidationError('Enter a valid completion time.', code='XXinvalidXX') from exc
           if completion_time.isoformat(sep=' ', timespec='minutes') != value:
               raise ValidationError('Enter a valid completion time.', code='invalid')
           return completion_time.replace(tzinfo=UTC)
  ```

- `src/cargotracker/handling/interfaces/rest.py:43 Mutant #164`

  ```diff
  @@ -40,7 +40,7 @@
           except ValueError as exc:
               raise ValidationError('Enter a valid completion time.', code='invalid') from exc
           if completion_time.isoformat(sep=' ', timespec='minutes') != value:
  -            raise ValidationError('Enter a valid completion time.', code='invalid')
  +            raise ValidationError('Enter a valid completion time.', code='XXinvalidXX')
           return completion_time.replace(tzinfo=UTC)
       def clean_trackingId(self):
  ```

- `src/cargotracker/handling/interfaces/rest.py:54 Mutant #169`

  ```diff
  @@ -51,7 +51,7 @@
           try:
               return HandlingEventType(value)
           except ValueError as exc:
  -            raise ValidationError('Select a valid event type.', code='invalid') from exc
  +            raise ValidationError('Select a valid event type.', code='XXinvalidXX') from exc
       def clean_unLocode(self):
           value = self.cleaned_data['unLocode']
  ```

- `src/cargotracker/handling/interfaces/rest.py:61 Mutant #173`

  ```diff
  @@ -58,7 +58,7 @@
           try:
               return UnLocode(value)
           except ValueError as exc:
  -            raise ValidationError('Enter a valid UN/LOCODE.', code='invalid') from exc
  +            raise ValidationError('Enter a valid UN/LOCODE.', code='XXinvalidXX') from exc
       def clean_voyageNumber(self):
           value = self.cleaned_data['voyageNumber']
  ```

- `src/cargotracker/handling/interfaces/rest.py:68 Mutant #182`

  ```diff
  @@ -65,7 +65,7 @@
           if not value:
               if 'voyageNumber' in self.data and self.data['voyageNumber'] is not None:
                   raise ValidationError(
  -                    'Ensure this value has at least 4 characters.', code='min_length'
  +                    'XXEnsure this value has at least 4 characters.XX', code='min_length'
                   )
               return None
           return VoyageNumber(value)
  ```

- `src/cargotracker/handling/interfaces/rest.py:68 Mutant #183`

  ```diff
  @@ -65,7 +65,7 @@
           if not value:
               if 'voyageNumber' in self.data and self.data['voyageNumber'] is not None:
                   raise ValidationError(
  -                    'Ensure this value has at least 4 characters.', code='min_length'
  +                    'Ensure this value has at least 4 characters.', code='XXmin_lengthXX'
                   )
               return None
           return VoyageNumber(value)
  ```

- `src/cargotracker/handling/interfaces/rest.py:82 Mutant #187`

  ```diff
  @@ -79,7 +79,7 @@
       repository: RegistrationAttemptRepository,
   ) -> Callable[[HttpRequest], HttpResponse]:
       @csrf_exempt
  -    @require_POST
  +
       def submit_handling_report(request):
           try:
               report = json.loads(request.body)
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:14 Mutant #297`

  ```diff
  @@ -11,7 +11,7 @@
   class RegistrationAttemptStatus(StrEnum):
       ACCEPTED = 'accepted'
  -    REGISTERED = 'registered'
  +    REGISTERED = 'XXregisteredXX'
       REJECTED = 'rejected'
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:32 Mutant #311`

  ```diff
  @@ -29,7 +29,7 @@
       def __post_init__(self):
           if not isinstance(self.tracking_id, TrackingId):
  -            raise TypeError('A registration attempt requires a tracking ID')
  +            raise TypeError('XXA registration attempt requires a tracking IDXX')
           object.__setattr__(self, 'completion_time', as_utc(self.completion_time, 'completion time'))
           object.__setattr__(
               self, 'registration_time', as_utc(self.registration_time, 'registration time')
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:38 Mutant #317`

  ```diff
  @@ -35,7 +35,7 @@
               self, 'registration_time', as_utc(self.registration_time, 'registration time')
           )
           if not isinstance(self.event_type, HandlingEventType):
  -            raise TypeError('A registration attempt requires an event type')
  +            raise TypeError('XXA registration attempt requires an event typeXX')
           if not isinstance(self.location, UnLocode):
               raise TypeError('A registration attempt requires a UN/LOCODE')
           if self.voyage_number is not None and not isinstance(self.voyage_number, VoyageNumber):
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:40 Mutant #319`

  ```diff
  @@ -37,7 +37,7 @@
           if not isinstance(self.event_type, HandlingEventType):
               raise TypeError('A registration attempt requires an event type')
           if not isinstance(self.location, UnLocode):
  -            raise TypeError('A registration attempt requires a UN/LOCODE')
  +            raise TypeError('XXA registration attempt requires a UN/LOCODEXX')
           if self.voyage_number is not None and not isinstance(self.voyage_number, VoyageNumber):
               raise TypeError('A registration attempt voyage number must be a voyage number')
           if self.id is not None and (
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:42 Mutant #323`

  ```diff
  @@ -39,7 +39,7 @@
           if not isinstance(self.location, UnLocode):
               raise TypeError('A registration attempt requires a UN/LOCODE')
           if self.voyage_number is not None and not isinstance(self.voyage_number, VoyageNumber):
  -            raise TypeError('A registration attempt voyage number must be a voyage number')
  +            raise TypeError('XXA registration attempt voyage number must be a voyage numberXX')
           if self.id is not None and (
               not isinstance(self.id, int) or isinstance(self.id, bool) or self.id < 1
           ):
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:46 Mutant #330`

  ```diff
  @@ -43,7 +43,7 @@
           if self.id is not None and (
               not isinstance(self.id, int) or isinstance(self.id, bool) or self.id < 1
           ):
  -            raise ValueError('A registration attempt ID must be a positive integer')
  +            raise ValueError('XXA registration attempt ID must be a positive integerXX')
           if not isinstance(self.status, RegistrationAttemptStatus):
               raise TypeError('A registration attempt requires a status')
           if self.status is RegistrationAttemptStatus.REJECTED:
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:48 Mutant #332`

  ```diff
  @@ -45,7 +45,7 @@
           ):
               raise ValueError('A registration attempt ID must be a positive integer')
           if not isinstance(self.status, RegistrationAttemptStatus):
  -            raise TypeError('A registration attempt requires a status')
  +            raise TypeError('XXA registration attempt requires a statusXX')
           if self.status is RegistrationAttemptStatus.REJECTED:
               if not isinstance(self.rejection_reason, str) or not self.rejection_reason.strip():
                   raise ValueError('A rejected registration attempt requires a reason')
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:51 Mutant #337`

  ```diff
  @@ -48,7 +48,7 @@
               raise TypeError('A registration attempt requires a status')
           if self.status is RegistrationAttemptStatus.REJECTED:
               if not isinstance(self.rejection_reason, str) or not self.rejection_reason.strip():
  -                raise ValueError('A rejected registration attempt requires a reason')
  +                raise ValueError('XXA rejected registration attempt requires a reasonXX')
           elif self.rejection_reason is not None:
               raise ValueError('Only a rejected registration attempt may have a reason')
  ```

- `src/cargotracker/handling/domain/registration_attempt.py:53 Mutant #339`

  ```diff
  @@ -50,5 +50,5 @@
               if not isinstance(self.rejection_reason, str) or not self.rejection_reason.strip():
                   raise ValueError('A rejected registration attempt requires a reason')
           elif self.rejection_reason is not None:
  -            raise ValueError('Only a rejected registration attempt may have a reason')
  +            raise ValueError('XXOnly a rejected registration attempt may have a reasonXX')
  ```

- `src/cargotracker/handling/domain/handling_event.py:35 Mutant #362`

  ```diff
  @@ -32,7 +32,7 @@
       def __post_init__(self):
           if not isinstance(self.cargo, Cargo):
  -            raise TypeError('A handling event requires a cargo')
  +            raise TypeError('XXA handling event requires a cargoXX')
           object.__setattr__(self, 'completion_time', as_utc(self.completion_time, 'completion time'))
           object.__setattr__(
               self, 'registration_time', as_utc(self.registration_time, 'registration time')
  ```

- `src/cargotracker/handling/domain/handling_event.py:36 Mutant #363`

  ```diff
  @@ -33,7 +33,7 @@
       def __post_init__(self):
           if not isinstance(self.cargo, Cargo):
               raise TypeError('A handling event requires a cargo')
  -        object.__setattr__(self, 'completion_time', as_utc(self.completion_time, 'completion time'))
  +        object.__setattr__(self, 'XXcompletion_timeXX', as_utc(self.completion_time, 'completion time'))
           object.__setattr__(
               self, 'registration_time', as_utc(self.registration_time, 'registration time')
           )
  ```

- `src/cargotracker/handling/domain/handling_event.py:38 Mutant #365`

  ```diff
  @@ -35,7 +35,7 @@
               raise TypeError('A handling event requires a cargo')
           object.__setattr__(self, 'completion_time', as_utc(self.completion_time, 'completion time'))
           object.__setattr__(
  -            self, 'registration_time', as_utc(self.registration_time, 'registration time')
  +            self, 'XXregistration_timeXX', as_utc(self.registration_time, 'registration time')
           )
           if not isinstance(self.event_type, HandlingEventType):
               raise TypeError('A handling event requires an event type')
  ```

- `src/cargotracker/handling/domain/handling_event.py:41 Mutant #368`

  ```diff
  @@ -38,7 +38,7 @@
               self, 'registration_time', as_utc(self.registration_time, 'registration time')
           )
           if not isinstance(self.event_type, HandlingEventType):
  -            raise TypeError('A handling event requires an event type')
  +            raise TypeError('XXA handling event requires an event typeXX')
           if not isinstance(self.location, Location):
               raise TypeError('A handling event requires a location')
           if self.voyage is not None and not isinstance(self.voyage, Voyage):
  ```

- `src/cargotracker/handling/domain/handling_event.py:43 Mutant #370`

  ```diff
  @@ -40,7 +40,7 @@
           if not isinstance(self.event_type, HandlingEventType):
               raise TypeError('A handling event requires an event type')
           if not isinstance(self.location, Location):
  -            raise TypeError('A handling event requires a location')
  +            raise TypeError('XXA handling event requires a locationXX')
           if self.voyage is not None and not isinstance(self.voyage, Voyage):
               raise TypeError('A handling event voyage must be a voyage')
           if self.id is not None and (
  ```

- `src/cargotracker/handling/domain/handling_event.py:45 Mutant #374`

  ```diff
  @@ -42,7 +42,7 @@
           if not isinstance(self.location, Location):
               raise TypeError('A handling event requires a location')
           if self.voyage is not None and not isinstance(self.voyage, Voyage):
  -            raise TypeError('A handling event voyage must be a voyage')
  +            raise TypeError('XXA handling event voyage must be a voyageXX')
           if self.id is not None and (
               not isinstance(self.id, int) or isinstance(self.id, bool) or self.id < 1
           ):
  ```

- `src/cargotracker/handling/domain/handling_event.py:47 Mutant #379`

  ```diff
  @@ -44,7 +44,7 @@
           if self.voyage is not None and not isinstance(self.voyage, Voyage):
               raise TypeError('A handling event voyage must be a voyage')
           if self.id is not None and (
  -            not isinstance(self.id, int) or isinstance(self.id, bool) or self.id < 1
  +            not isinstance(self.id, int) and isinstance(self.id, bool) or self.id < 1
           ):
               raise ValueError('A handling event ID must be a positive integer')
           if self.event_type.requires_voyage and self.voyage is None:
  ```

- `src/cargotracker/handling/domain/handling_event.py:49 Mutant #381`

  ```diff
  @@ -46,7 +46,7 @@
           if self.id is not None and (
               not isinstance(self.id, int) or isinstance(self.id, bool) or self.id < 1
           ):
  -            raise ValueError('A handling event ID must be a positive integer')
  +            raise ValueError('XXA handling event ID must be a positive integerXX')
           if self.event_type.requires_voyage and self.voyage is None:
               raise ValueError(f'Voyage is required for event type {self.event_type}')
           if not self.event_type.requires_voyage and self.voyage is not None:
  ```

- `src/cargotracker/handling/domain/handling_event.py:53 Mutant #388`

  ```diff
  @@ -50,5 +50,5 @@
           if self.event_type.requires_voyage and self.voyage is None:
               raise ValueError(f'Voyage is required for event type {self.event_type}')
           if not self.event_type.requires_voyage and self.voyage is not None:
  -            raise ValueError(f'Voyage is not allowed with event type {self.event_type}')
  +            raise ValueError(f'XXVoyage is not allowed with event type {self.event_type}XX')
  ```

- `src/cargotracker/cargo/domain/itinerary.py:10 Mutant #390`

  ```diff
  @@ -7,7 +7,7 @@
       from cargotracker.handling.domain.handling_event import HandlingEvent
  -@dataclass(frozen=True, init=False)
  +@dataclass(frozen=True, init=True)
   class Itinerary:
       legs: tuple[Leg, ...]
  ```

- `src/cargotracker/cargo/domain/itinerary.py:39 Mutant #412`

  ```diff
  @@ -36,7 +36,7 @@
               'CLAIM': self._claim_matches_destination,
           }
           checker = checkers.get(event.event_type)
  -        return checker(event) if checker is not None else False
  +        return checker(event) if checker is not None else True
       def _receive_matches_first_leg(self, event: 'HandlingEvent') -> bool:
           return self.legs[0].load_location == event.location
  ```

- `src/cargotracker/handling/application/accept_registration.py:12 Mutant #507`

  ```diff
  @@ -9,6 +9,6 @@
       attempt: RegistrationAttempt, repository: RegistrationAttemptRepository
   ) -> RegistrationAttempt:
       if attempt.id is not None or attempt.status is not RegistrationAttemptStatus.ACCEPTED:
  -        raise ValueError('Only a new registration attempt can be accepted')
  +        raise ValueError('XXOnly a new registration attempt can be acceptedXX')
       return repository.submit(attempt)
  ```

- `src/cargotracker/cargo/application/map_status.py:8 Mutant #510`

  ```diff
  @@ -5,7 +5,7 @@
       if not cargo.itinerary.legs:
           return 'NOT_ROUTED'
       if cargo.delivery.unloaded_at_destination:
  -        return 'AT_DESTINATION'
  +        return 'XXAT_DESTINATIONXX'
       if cargo.delivery.misdirected:
           return 'MISDIRECTED'
       return cargo.delivery.transport_status.value
  ```

- `src/cargotracker/cargo/application/sample_data.py:41 Mutant #34`

  ```diff
  @@ -38,7 +38,7 @@
   VOYAGES = ('0100S', '0200T', '0300A', '0400S', '0301S')
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class _LegSeed:
       voyage: str
       load_location: str
  ```

- `src/cargotracker/cargo/application/sample_data.py:50 Mutant #36`

  ```diff
  @@ -47,7 +47,7 @@
       unload_offset: int
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class _EventSeed:
       event_type: HandlingEventType
       location: str
  ```

- `src/cargotracker/cargo/application/sample_data.py:58 Mutant #38`

  ```diff
  @@ -55,7 +55,7 @@
       completion_offset: int
  -@dataclass(frozen=True)
  +@dataclass(frozen=False)
   class _CargoSeed:
       tracking_id: str
       origin: str
  ```

- `src/cargotracker/cargo/application/sample_data.py:65 Mutant #41`

  ```diff
  @@ -62,7 +62,7 @@
       destination: str
       legs: tuple[_LegSeed, ...]
       events: tuple[_EventSeed, ...]
  -    deadline_days: int | None = None
  +    deadline_days: int | None = ""
       deadline_months: int | None = None
  ```

- `src/cargotracker/cargo/application/sample_data.py:84 Mutant #75`

  ```diff
  @@ -81,7 +81,7 @@
               _EventSeed(HandlingEventType.LOAD, 'CNHKG', '0100S', -7),
               _EventSeed(HandlingEventType.UNLOAD, 'USNYC', '0100S', -1),
           ),
  -        deadline_days=15,
  +        deadline_days=16,
       ),
       _CargoSeed(
           'JKL567',
  ```

- `src/cargotracker/cargo/application/sample_data.py:101 Mutant #112`

  ```diff
  @@ -98,7 +98,7 @@
               _EventSeed(HandlingEventType.UNLOAD, 'USNYC', '0100S', -3),
               _EventSeed(HandlingEventType.LOAD, 'USNYC', '0100S', -2),
           ),
  -        deadline_days=18,
  +        deadline_days=19,
       ),
       _CargoSeed(
           'DEF789',
  ```

- `src/cargotracker/cargo/application/sample_data.py:130 Mutant #153`

  ```diff
  @@ -127,7 +127,7 @@
   def _add_months(value: date, months: int) -> date:
       month_index = value.month - 1 + months
  -    year = value.year + month_index // 12
  +    year = value.year + month_index // 13
       month = month_index % 12 + 1
       return value.replace(
           year=year,
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:31 Mutant #188`

  ```diff
  @@ -28,7 +28,7 @@
       try:
           deadline = date.fromisoformat(value)
       except ValueError:
  -        return None, None, 'Enter a valid arrival deadline.'
  +        return None, None, 'XXEnter a valid arrival deadline.XX'
       if deadline < today:
           return None, None, 'Arrival deadline cannot be before today.'
       duration = timedelta(days=(deadline - today).days, hours=4).days
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:33 Mutant #190`

  ```diff
  @@ -30,7 +30,7 @@
       except ValueError:
           return None, None, 'Enter a valid arrival deadline.'
       if deadline < today:
  -        return None, None, 'Arrival deadline cannot be before today.'
  +        return None, None, 'XXArrival deadline cannot be before today.XX'
       duration = timedelta(days=(deadline - today).days, hours=4).days
       return deadline, duration, ''
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:34 Mutant #192`

  ```diff
  @@ -31,7 +31,7 @@
           return None, None, 'Enter a valid arrival deadline.'
       if deadline < today:
           return None, None, 'Arrival deadline cannot be before today.'
  -    duration = timedelta(days=(deadline - today).days, hours=4).days
  +    duration = timedelta(days=(deadline - today).days, hours=5).days
       return deadline, duration, ''
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:61 Mutant #205`

  ```diff
  @@ -58,7 +58,7 @@
       locations: list[Location],
       origin: Location | None,
       destination: Location | None,
  -    deadline_value: str = '',
  +    deadline_value: str = 'XXXX',
       error: str = '',
   ) -> HttpResponse:
       context = {
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:98 Mutant #233`

  ```diff
  @@ -95,7 +95,7 @@
   ) -> HttpResponse:
       deadline_value = request.POST.get('deadline', '')
       context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
  -    context['validation_error'] = ''
  +    context['XXvalidation_errorXX'] = ''
       if request.POST.get('action') == 'book':
           if origin is None or destination is None:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:98 Mutant #235`

  ```diff
  @@ -95,7 +95,7 @@
   ) -> HttpResponse:
       deadline_value = request.POST.get('deadline', '')
       context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
  -    context['validation_error'] = ''
  +    context['validation_error'] = None
       if request.POST.get('action') == 'book':
           if origin is None or destination is None:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:102 Mutant #243`

  ```diff
  @@ -99,7 +99,7 @@
       if request.POST.get('action') == 'book':
           if origin is None or destination is None:
  -            context['validation_error'] = 'Choose an origin and destination.'
  +            context['validation_error'] = 'XXChoose an origin and destination.XX'
           elif origin == destination:
               context['validation_error'] = 'Origin and destination cannot be the same.'
           elif context['deadline'] is None:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:104 Mutant #247`

  ```diff
  @@ -101,7 +101,7 @@
           if origin is None or destination is None:
               context['validation_error'] = 'Choose an origin and destination.'
           elif origin == destination:
  -            context['validation_error'] = 'Origin and destination cannot be the same.'
  +            context['validation_error'] = 'XXOrigin and destination cannot be the same.XX'
           elif context['deadline'] is None:
               context['validation_error'] = context['deadline_error'] or 'Choose an arrival deadline.'
           elif context['bookable']:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:106 Mutant #253`

  ```diff
  @@ -103,7 +103,7 @@
           elif origin == destination:
               context['validation_error'] = 'Origin and destination cannot be the same.'
           elif context['deadline'] is None:
  -            context['validation_error'] = context['deadline_error'] or 'Choose an arrival deadline.'
  +            context['validation_error'] = context['deadline_error'] or 'XXChoose an arrival deadline.XX'
           elif context['bookable']:
               registration.register(
                   origin,
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:131 Mutant #269`

  ```diff
  @@ -128,7 +128,7 @@
           available_locations = list_shipping_locations()
           location_by_code = {location.unlocode.value: location for location in available_locations}
           data = request.POST
  -        origin = location_by_code.get(data.get('origin', ''))
  +        origin = location_by_code.get(data.get('origin', 'XXXX'))
           destination = location_by_code.get(data.get('destination', ''))
           deadline_value = data.get('deadline', '')
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:132 Mutant #272`

  ```diff
  @@ -129,7 +129,7 @@
           location_by_code = {location.unlocode.value: location for location in available_locations}
           data = request.POST
           origin = location_by_code.get(data.get('origin', ''))
  -        destination = location_by_code.get(data.get('destination', ''))
  +        destination = location_by_code.get(data.get('destination', 'XXXX'))
           deadline_value = data.get('deadline', '')
           if request.method != 'POST':
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #284`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('XXstepXX') == 'destination' and data.get('action') == 'back':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #286`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('step') == 'XXdestinationXX' and data.get('action') == 'back':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #287`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('step') == 'destination' and data.get('XXactionXX') == 'back':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:143 Mutant #289`

  ```diff
  @@ -140,7 +140,7 @@
               )
           if data.get('action') == 'cancel':
               return redirect('/admin/dashboard/')
  -        if data.get('step') == 'destination' and data.get('action') == 'back':
  +        if data.get('step') == 'destination' and data.get('action') == 'XXbackXX':
               return _origin_step(request, available_locations, origin, destination, deadline_value)
           if data.get('step') == 'deadline' and data.get('action') == 'back':
               return _destination_step(
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:150 Mutant #301`

  ```diff
  @@ -147,7 +147,7 @@
                   request, available_locations, origin, destination, deadline_value
               )
           if (
  -            data.get('step') in {'origin', 'destination'}
  +            data.get('step') in {'origin', 'XXdestinationXX'}
               and data.get('action') == 'next'
               and origin is None
           ):
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:160 Mutant #307`

  ```diff
  @@ -157,7 +157,7 @@
                   None,
                   destination,
                   deadline_value,
  -                'Select a valid origin.',
  +                'XXSelect a valid origin.XX',
               )
           if data.get('step') == 'origin' and data.get('action') == 'next':
               if destination is None or destination == origin:
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:168 Mutant #326`

  ```diff
  @@ -165,7 +165,7 @@
               return _destination_step(
                   request, available_locations, origin, destination, deadline_value
               )
  -        if data.get('step') == 'destination' and data.get('action') == 'next':
  +        if data.get('step') == 'destination' or data.get('action') == 'next':
               if destination is None:
                   return _destination_step(
                       request,
  ```

- `src/cargotracker/booking/interfaces/wizard/views.py:176 Mutant #328`

  ```diff
  @@ -173,7 +173,7 @@
                       origin,
                       None,
                       deadline_value,
  -                    'Select a valid destination.',
  +                    'XXSelect a valid destination.XX',
                   )
               context = _deadline_context(origin, destination, deadline_value, timezone.localdate())
               return render(request, 'booking/wizard/deadline.html', context)
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:49 Mutant #354`

  ```diff
  @@ -46,7 +46,7 @@
           destination_value = (
               request.POST.get('destination')
               if request.method == 'POST'
  -            else (destinations[0].unlocode.value if destinations else '')
  +            else (destinations[0].unlocode.value if destinations else 'XXXX')
           )
           destination_error = ''
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:51 Mutant #357`

  ```diff
  @@ -48,7 +48,7 @@
               if request.method == 'POST'
               else (destinations[0].unlocode.value if destinations else '')
           )
  -        destination_error = ''
  +        destination_error = None
           if request.method == 'POST':
               destination_by_code = {location.unlocode.value: location for location in destinations}
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:57 Mutant #363`

  ```diff
  @@ -54,7 +54,7 @@
               destination_by_code = {location.unlocode.value: location for location in destinations}
               destination = destination_by_code.get(destination_value)
               if destination is None:
  -                destination_error = 'Select a valid destination.'
  +                destination_error = 'XXSelect a valid destination.XX'
               else:
                   cargo_specification.change_destination(TrackingId(tracking_id), destination)
                   return _complete_dialog_update(request)
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:80 Mutant #377`

  ```diff
  @@ -77,7 +77,7 @@
               if request.method == 'POST'
               else cargo.route_specification.arrival_deadline.date().isoformat()
           )
  -        deadline_error = ''
  +        deadline_error = None
           if request.method == 'POST':
               try:
  ```

- `src/cargotracker/booking/interfaces/dialogs/views.py:86 Mutant #381`

  ```diff
  @@ -83,7 +83,7 @@
               try:
                   arrival_date = date.fromisoformat(deadline_value)
               except ValueError:
  -                deadline_error = 'Enter a valid arrival deadline.'
  +                deadline_error = 'XXEnter a valid arrival deadline.XX'
               else:
                   arrival_deadline = timezone.make_aware(datetime.combine(arrival_date, time.min))
                   cargo_specification.change_deadline(TrackingId(tracking_id), arrival_deadline)
  ```

- `src/cargotracker/booking/application/specification.py:57 Mutant #401`

  ```diff
  @@ -54,7 +54,7 @@
       def _find_cargo(self, tracking_id: TrackingId) -> Cargo:
           cargo = self._cargo_repository.find(tracking_id)
           if cargo is None:
  -            raise LookupError(f'Cargo {tracking_id} not found')
  +            raise LookupError(f'XXCargo {tracking_id} not foundXX')
           return cargo
       def _update(self, cargo: Cargo, specification: RouteSpecification) -> Cargo:
  ```

- `src/cargotracker/cargo/interfaces/tracking/map/views.py:11 Mutant #525`

  ```diff
  @@ -8,7 +8,7 @@
       'NOT_RECEIVED': 'gold',
       'IN_PORT': 'green',
       'ONBOARD_CARRIER': 'green',
  -    'MISDIRECTED': 'red',
  +    'XXMISDIRECTEDXX': 'red',
       'AT_DESTINATION': 'black',
       'CLAIMED': 'black',
       'UNKNOWN': 'red',
  ```

- `src/cargotracker/cargo/interfaces/tracking/map/views.py:14 Mutant #531`

  ```diff
  @@ -11,7 +11,7 @@
       'MISDIRECTED': 'red',
       'AT_DESTINATION': 'black',
       'CLAIMED': 'black',
  -    'UNKNOWN': 'red',
  +    'XXUNKNOWNXX': 'red',
   }
  ```

- `src/cargotracker/cargo/interfaces/tracking/map/views.py:20 Mutant #536`

  ```diff
  @@ -17,7 +17,7 @@
   @xframe_options_sameorigin
   def map_frame(request):
  -    status_code = request.GET.get('statusCode', 'UNKNOWN')
  +    status_code = request.GET.get('statusCode', 'XXUNKNOWNXX')
       locations = {
           role: _location_data(request, role)
           for role in ('origin', 'destination', 'lastKnownLocation')
  ```

- `src/cargotracker/cargo/interfaces/tracking/map/views.py:45 Mutant #560`

  ```diff
  @@ -42,7 +42,7 @@
   def _location_data(request, role):
  -    code = request.GET.get(f'{role}Code', '')
  +    code = request.GET.get(f'{role}Code', 'XXXX')
       return {
           'code': code,
           'name': request.GET.get(f'{role}Name', ''),
  ```

- `src/cargotracker/cargo/interfaces/tracking/map/views.py:48 Mutant #565`

  ```diff
  @@ -45,6 +45,6 @@
       code = request.GET.get(f'{role}Code', '')
       return {
           'code': code,
  -        'name': request.GET.get(f'{role}Name', ''),
  +        'name': request.GET.get(f'{role}Name', 'XXXX'),
       }
  ```

