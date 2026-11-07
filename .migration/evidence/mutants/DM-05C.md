# Surviving mutants: DM-05C

Written by `afs-mutation` on its last run (base `origin/main`): score 0.874, threshold 0.8, killed 264, survived 38. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/data_migration/loader.py:32 Mutant #22`

  ```diff
  @@ -29,7 +29,7 @@
           if value in mapping:
               result = mapping[value]
           elif str(value) in mapping:
  -            result = mapping[str(value)]
  +            result = None
           else:
               raise DataLoadError(f'no mapping for value {value!r}')
           return None if result is None else str(result)
  ```

- `src/cargotracker/data_migration/loader.py:54 Mutant #51`

  ```diff
  @@ -51,7 +51,7 @@
               return False
           raise DataLoadError(f'not a boolean: {value!r}')
       if transform in ('timestamp', 'date'):
  -        if transform == 'date' and len(value.strip()) <= 10:
  +        if transform == 'date' and len(value.strip()) <= 11:
               parsed = datetime.date.fromisoformat(value.strip())
               return parsed
           try:
  ```

- `src/cargotracker/data_migration/loader.py:61 Mutant #55`

  ```diff
  @@ -58,7 +58,7 @@
               parsed = datetime.datetime.fromisoformat(value.strip())
           except ValueError:
               for pattern in (
  -                '%Y-%m-%d %H:%M:%S.%f%z',
  +                'XX%Y-%m-%d %H:%M:%S.%f%zXX',
                   '%Y-%m-%d %H:%M:%S%z',
                   '%Y-%m-%d %H:%M',
               ):
  ```

- `src/cargotracker/data_migration/loader.py:62 Mutant #56`

  ```diff
  @@ -59,7 +59,7 @@
           except ValueError:
               for pattern in (
                   '%Y-%m-%d %H:%M:%S.%f%z',
  -                '%Y-%m-%d %H:%M:%S%z',
  +                'XX%Y-%m-%d %H:%M:%S%zXX',
                   '%Y-%m-%d %H:%M',
               ):
                   try:
  ```

- `src/cargotracker/data_migration/loader.py:71 Mutant #61`

  ```diff
  @@ -68,7 +68,7 @@
                   except ValueError:
                       continue
               else:
  -                raise DataLoadError(f'not a timestamp: {value!r}')
  +                raise DataLoadError(f'XXnot a timestamp: {value!r}XX')
           if parsed.tzinfo is None:
               parsed = parsed.replace(tzinfo=timezone)
           parsed = parsed.astimezone(datetime.UTC)
  ```

- `src/cargotracker/data_migration/loader.py:75 Mutant #66`

  ```diff
  @@ -72,7 +72,7 @@
           if parsed.tzinfo is None:
               parsed = parsed.replace(tzinfo=timezone)
           parsed = parsed.astimezone(datetime.UTC)
  -        if transform == 'date':
  +        if transform == 'XXdateXX':
               return parsed.date()
           return parsed
       raise DataLoadError(f'unknown transform {transform!r}')
  ```

- `src/cargotracker/data_migration/loader.py:89 Mutant #79`

  ```diff
  @@ -86,7 +86,7 @@
       for target_column, definition in columns.items():
           if isinstance(definition, dict):
               source_column = definition.get('from')
  -            transform = definition.get('as', 'identity')
  +            transform = definition.get('as', 'XXidentityXX')
           else:
               source_column = definition
               transform = 'identity'
  ```

- `src/cargotracker/data_migration/loader.py:92 Mutant #83`

  ```diff
  @@ -89,7 +89,7 @@
               transform = definition.get('as', 'identity')
           else:
               source_column = definition
  -            transform = 'identity'
  +            transform = None
           if not isinstance(source_column, str):
               raise DataLoadError(f'{target_column}: mapping must name a source column')
           result.append((target_column, source_column, transform))
  ```

- `src/cargotracker/data_migration/loader.py:103 Mutant #88`

  ```diff
  @@ -100,7 +100,7 @@
       return {
           model._meta.db_table: model
           for model in apps.get_models()
  -        if not model._meta.proxy and not model._meta.auto_created
  +        if not model._meta.proxy or not model._meta.auto_created
       }
  ```

- `src/cargotracker/data_migration/loader.py:111 Mutant #90`

  ```diff
  @@ -108,7 +108,7 @@
       for field in model._meta.concrete_fields:
           if column in (field.column, field.name, field.attname):
               return field
  -    raise DataLoadError(f'{model._meta.db_table}: no target column {column!r}')
  +    raise DataLoadError(f'XX{model._meta.db_table}: no target column {column!r}XX')
   def _read_manifest(snapshot):
  ```

- `src/cargotracker/data_migration/loader.py:140 Mutant #116`

  ```diff
  @@ -137,7 +137,7 @@
       ):
           raise DataLoadError(f'{source}: sha256 differs from the snapshot manifest')
  -    marker = manifest.get('null', '\\N')
  +    marker = manifest.get('XXnullXX', '\\N')
       try:
           with path.open(newline='', encoding='utf-8') as stream:
               reader = csv.reader(stream)
  ```

- `src/cargotracker/data_migration/loader.py:140 Mutant #117`

  ```diff
  @@ -137,7 +137,7 @@
       ):
           raise DataLoadError(f'{source}: sha256 differs from the snapshot manifest')
  -    marker = manifest.get('null', '\\N')
  +    marker = manifest.get('null', 'XX\\NXX')
       try:
           with path.open(newline='', encoding='utf-8') as stream:
               reader = csv.reader(stream)
  ```

- `src/cargotracker/data_migration/loader.py:159 Mutant #132`

  ```diff
  @@ -156,7 +156,7 @@
                       dict(zip(header, (None if value == marker else value for value in row)))
                   )
       except OSError as error:
  -        raise DataLoadError(f'{path}: {error}') from error
  +        raise DataLoadError(f'XX{path}: {error}XX') from error
       if 'rows' in metadata and len(rows) != metadata['rows']:
           raise DataLoadError(f'{source}: {len(rows)} rows, manifest says {metadata["rows"]}')
  ```

- `src/cargotracker/data_migration/loader.py:186 Mutant #163`

  ```diff
  @@ -183,7 +183,7 @@
           target = spec['target']
           model = models.get(target)
           if model is None:
  -            raise DataLoadError(f'{target}: no registered Django model for target table')
  +            raise DataLoadError(f'XX{target}: no registered Django model for target tableXX')
           columns = _column_specs(spec)
           fields = {name: _field_for_column(model, name) for name, _, _ in columns}
           if model._meta.pk not in fields.values():
  ```

- `src/cargotracker/data_migration/loader.py:203 Mutant #187`

  ```diff
  @@ -200,7 +200,7 @@
                       f'{entry["spec"]["target"]}: reference {column!r} is not mapped'
                   )
               try:
  -                table, referenced_column = reference.rsplit('.', 1)
  +                table, referenced_column = reference.rsplit('.', 2)
               except (AttributeError, ValueError) as error:
                   raise DataLoadError(f'{column}: invalid reference {reference!r}') from error
               referenced_entry = next(
  ```

- `src/cargotracker/data_migration/loader.py:220 Mutant #209`

  ```diff
  @@ -215,8 +215,7 @@
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

- `src/cargotracker/data_migration/loader.py:227 Mutant #215`

  ```diff
  @@ -224,7 +224,7 @@
               entry['refs'][column] = {
                   'target_index': target_indexes[table],
                   'field': field,
  -                'target_model': referenced_entry['model'],
  +                'XXtarget_modelXX': referenced_entry['model'],
               }
       return prepared
  ```

- `src/cargotracker/data_migration/loader.py:236 Mutant #222`

  ```diff
  @@ -233,7 +233,7 @@
       for index, entry in enumerate(prepared):
           model = entry['model']
           for column, reference in entry['refs'].items():
  -            if reference['target_index'] > index:
  +            if reference['target_index'] >= index:
                   if not reference['field'].null:
                       raise DataLoadError(
                           f'{entry["spec"]["target"]}.{column}: a forward reference must be nullable'
  ```

- `src/cargotracker/data_migration/loader.py:239 Mutant #225`

  ```diff
  @@ -236,7 +236,7 @@
               if reference['target_index'] > index:
                   if not reference['field'].null:
                       raise DataLoadError(
  -                        f'{entry["spec"]["target"]}.{column}: a forward reference must be nullable'
  +                        f'{entry["XXspecXX"]["target"]}.{column}: a forward reference must be nullable'
                       )
                   model._base_manager.all().update(**{reference['field'].attname: None})
       for entry in reversed(prepared):
  ```

- `src/cargotracker/data_migration/loader.py:239 Mutant #226`

  ```diff
  @@ -236,7 +236,7 @@
               if reference['target_index'] > index:
                   if not reference['field'].null:
                       raise DataLoadError(
  -                        f'{entry["spec"]["target"]}.{column}: a forward reference must be nullable'
  +                        f'{entry["spec"]["XXtargetXX"]}.{column}: a forward reference must be nullable'
                       )
                   model._base_manager.all().update(**{reference['field'].attname: None})
       for entry in reversed(prepared):
  ```

- `src/cargotracker/data_migration/loader.py:239 Mutant #227`

  ```diff
  @@ -236,7 +236,7 @@
               if reference['target_index'] > index:
                   if not reference['field'].null:
                       raise DataLoadError(
  -                        f'{entry["spec"]["target"]}.{column}: a forward reference must be nullable'
  +                        f'XX{entry["spec"]["target"]}.{column}: a forward reference must be nullableXX'
                       )
                   model._base_manager.all().update(**{reference['field'].attname: None})
       for entry in reversed(prepared):
  ```

- `src/cargotracker/data_migration/loader.py:253 Mutant #239`

  ```diff
  @@ -250,7 +250,7 @@
       missing = required_sources.difference(source_rows[0].keys()) if source_rows else set()
       if missing:
           raise DataLoadError(
  -            f'{spec["source"]}: no column(s) {", ".join(sorted(missing))} in its CSV header'
  +            f'{spec["source"]}: no column(s) {"XX, XX".join(sorted(missing))} in its CSV header'
           )
       return source_rows
  ```

- `src/cargotracker/data_migration/loader.py:269 Mutant #255`

  ```diff
  @@ -266,7 +266,7 @@
               field = entry['fields'][target_column]
               value = _transform(row[source_column], transform, timezone)
               reference = entry['refs'].get(target_column)
  -            if reference and reference['target_index'] > index and value is not None:
  +            if reference and reference['target_index'] >= index and value is not None:
                   pending.append((model, values, field, value))
                   value = None
               values[field.attname] = value
  ```

- `src/cargotracker/data_migration/loader.py:271 Mutant #258`

  ```diff
  @@ -268,7 +268,7 @@
               reference = entry['refs'].get(target_column)
               if reference and reference['target_index'] > index and value is not None:
                   pending.append((model, values, field, value))
  -                value = None
  +                value = ""
               values[field.attname] = value
           if values[model._meta.pk.attname] is None:
               raise DataLoadError(f'{spec["source"]}: primary key cannot be NULL')
  ```

- `src/cargotracker/data_migration/loader.py:274 Mutant #261`

  ```diff
  @@ -271,7 +271,7 @@
                   value = None
               values[field.attname] = value
           if values[model._meta.pk.attname] is None:
  -            raise DataLoadError(f'{spec["source"]}: primary key cannot be NULL')
  +            raise DataLoadError(f'{spec["XXsourceXX"]}: primary key cannot be NULL')
           objects.append(model(**values))
       model._base_manager.bulk_create(objects, batch_size=1000)
       return spec['target'], len(source_rows)
  ```

- `src/cargotracker/data_migration/loader.py:274 Mutant #262`

  ```diff
  @@ -271,7 +271,7 @@
                   value = None
               values[field.attname] = value
           if values[model._meta.pk.attname] is None:
  -            raise DataLoadError(f'{spec["source"]}: primary key cannot be NULL')
  +            raise DataLoadError(f'XX{spec["source"]}: primary key cannot be NULLXX')
           objects.append(model(**values))
       model._base_manager.bulk_create(objects, batch_size=1000)
       return spec['target'], len(source_rows)
  ```

- `src/cargotracker/data_migration/loader.py:276 Mutant #263`

  ```diff
  @@ -273,7 +273,7 @@
           if values[model._meta.pk.attname] is None:
               raise DataLoadError(f'{spec["source"]}: primary key cannot be NULL')
           objects.append(model(**values))
  -    model._base_manager.bulk_create(objects, batch_size=1000)
  +    model._base_manager.bulk_create(objects, batch_size=1001)
       return spec['target'], len(source_rows)
  ```

- `src/cargotracker/data_migration/loader.py:309 Mutant #272`

  ```diff
  @@ -306,7 +306,7 @@
   @transaction.atomic
   def load_snapshot(snapshot_path, mapping_path):
       if connection.vendor != 'postgresql':
  -        raise DataLoadError('load_data_snapshot requires PostgreSQL')
  +        raise DataLoadError('XXload_data_snapshot requires PostgreSQLXX')
       snapshot = Path(snapshot_path)
       mapping_file = Path(mapping_path)
       try:
  ```

- `src/cargotracker/data_migration/loader.py:315 Mutant #278`

  ```diff
  @@ -312,7 +312,7 @@
       try:
           mapping = yaml.safe_load(mapping_file.read_text(encoding='utf-8')) or {}
       except (OSError, yaml.YAMLError) as error:
  -        raise DataLoadError(f'{mapping_file}: unable to read mapping: {error}') from error
  +        raise DataLoadError(f'XX{mapping_file}: unable to read mapping: {error}XX') from error
       if not isinstance(mapping, dict):
           raise DataLoadError(f'{mapping_file}: mapping must be an object')
  ```

- `src/cargotracker/data_migration/loader.py:317 Mutant #280`

  ```diff
  @@ -314,7 +314,7 @@
       except (OSError, yaml.YAMLError) as error:
           raise DataLoadError(f'{mapping_file}: unable to read mapping: {error}') from error
       if not isinstance(mapping, dict):
  -        raise DataLoadError(f'{mapping_file}: mapping must be an object')
  +        raise DataLoadError(f'XX{mapping_file}: mapping must be an objectXX')
       manifest = _read_manifest(snapshot)
       timezone = _mapping_timezone(mapping)
  ```

- `src/cargotracker/data_migration/management/commands/load_data_snapshot.py:7 Mutant #1`

  ```diff
  @@ -4,7 +4,7 @@
   class Command(BaseCommand):
  -    help = 'Load a validated relational snapshot using its mapping.'
  +    help = 'XXLoad a validated relational snapshot using its mapping.XX'
       def add_arguments(self, parser):
           parser.add_argument('--snapshot', required=True)
  ```

- `src/cargotracker/data_migration/management/commands/load_data_snapshot.py:7 Mutant #2`

  ```diff
  @@ -4,7 +4,7 @@
   class Command(BaseCommand):
  -    help = 'Load a validated relational snapshot using its mapping.'
  +    help = None
       def add_arguments(self, parser):
           parser.add_argument('--snapshot', required=True)
  ```

- `src/cargotracker/data_migration/management/commands/load_data_snapshot.py:10 Mutant #4`

  ```diff
  @@ -7,7 +7,7 @@
       help = 'Load a validated relational snapshot using its mapping.'
       def add_arguments(self, parser):
  -        parser.add_argument('--snapshot', required=True)
  +        parser.add_argument('--snapshot', required=False)
           parser.add_argument('--mapping', required=True)
       def handle(self, *args, **options):
  ```

- `src/cargotracker/data_migration/management/commands/load_data_snapshot.py:11 Mutant #6`

  ```diff
  @@ -8,7 +8,7 @@
       def add_arguments(self, parser):
           parser.add_argument('--snapshot', required=True)
  -        parser.add_argument('--mapping', required=True)
  +        parser.add_argument('--mapping', required=False)
       def handle(self, *args, **options):
           try:
  ```

- `src/cargotracker/data_migration/management/commands/load_data_snapshot.py:18 Mutant #10`

  ```diff
  @@ -15,7 +15,7 @@
               loaded = load_snapshot(options['snapshot'], options['mapping'])
           except DataLoadError as error:
               raise CommandError(str(error)) from error
  -        total = sum(rows for _, rows in loaded)
  +        total = None
           self.stdout.write(
               self.style.SUCCESS(f'Loaded {total} rows across {len(loaded)} mapped tables.')
           )
  ```

- `src/cargotracker/data_migration/management/commands/load_data_snapshot.py:20 Mutant #11`

  ```diff
  @@ -17,6 +17,6 @@
               raise CommandError(str(error)) from error
           total = sum(rows for _, rows in loaded)
           self.stdout.write(
  -            self.style.SUCCESS(f'Loaded {total} rows across {len(loaded)} mapped tables.')
  +            self.style.SUCCESS(f'XXLoaded {total} rows across {len(loaded)} mapped tables.XX')
           )
  ```

- `src/cargotracker/data_migration/apps.py:5 Mutant #1`

  ```diff
  @@ -2,6 +2,6 @@
   class DataMigrationConfig(AppConfig):
  -    default_auto_field = 'django.db.models.BigAutoField'
  +    default_auto_field = 'XXdjango.db.models.BigAutoFieldXX'
       name = 'cargotracker.data_migration'
  ```

- `src/cargotracker/data_migration/apps.py:5 Mutant #2`

  ```diff
  @@ -2,6 +2,6 @@
   class DataMigrationConfig(AppConfig):
  -    default_auto_field = 'django.db.models.BigAutoField'
  +    default_auto_field = None
       name = 'cargotracker.data_migration'
  ```

