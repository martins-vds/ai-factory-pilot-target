# Surviving mutants: DM-05D

Written by `afs-mutation` on its last run (base `origin/main`): score 0.660, threshold 0.8, killed 68, survived 35. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/data_migration/exporter.py:18 Mutant #3`

  ```diff
  @@ -15,7 +15,7 @@
       return {
           model._meta.db_table: model
           for model in apps.get_models()
  -        if not model._meta.proxy and not model._meta.auto_created
  +        if not model._meta.proxy or not model._meta.auto_created
       }
  ```

- `src/cargotracker/data_migration/exporter.py:26 Mutant #5`

  ```diff
  @@ -23,7 +23,7 @@
       for field in model._meta.concrete_fields:
           if column in (field.column, field.name, field.attname):
               return field
  -    raise DataExportError(f'{model._meta.db_table}: no target column {column!r}')
  +    raise DataExportError(f'XX{model._meta.db_table}: no target column {column!r}XX')
   def _prepare_tables(mapping, models):
  ```

- `src/cargotracker/data_migration/exporter.py:31 Mutant #10`

  ```diff
  @@ -28,7 +28,7 @@
   def _prepare_tables(mapping, models):
       specs = mapping.get('tables')
  -    if not isinstance(specs, list) or not specs:
  +    if not isinstance(specs, list) and not specs:
           raise DataExportError('mapping has no tables')
       targets = [spec.get('target') if isinstance(spec, dict) else None for spec in specs]
       if any(not isinstance(target, str) for target in targets) or len(targets) != len(set(targets)):
  ```

- `src/cargotracker/data_migration/exporter.py:32 Mutant #11`

  ```diff
  @@ -29,7 +29,7 @@
   def _prepare_tables(mapping, models):
       specs = mapping.get('tables')
       if not isinstance(specs, list) or not specs:
  -        raise DataExportError('mapping has no tables')
  +        raise DataExportError('XXmapping has no tablesXX')
       targets = [spec.get('target') if isinstance(spec, dict) else None for spec in specs]
       if any(not isinstance(target, str) for target in targets) or len(targets) != len(set(targets)):
           raise DataExportError('mapping targets must be unique table names')
  ```

- `src/cargotracker/data_migration/exporter.py:34 Mutant #16`

  ```diff
  @@ -31,7 +31,7 @@
       if not isinstance(specs, list) or not specs:
           raise DataExportError('mapping has no tables')
       targets = [spec.get('target') if isinstance(spec, dict) else None for spec in specs]
  -    if any(not isinstance(target, str) for target in targets) or len(targets) != len(set(targets)):
  +    if any(not isinstance(target, str) for target in targets) and len(targets) != len(set(targets)):
           raise DataExportError('mapping targets must be unique table names')
       prepared = []
  ```

- `src/cargotracker/data_migration/exporter.py:35 Mutant #17`

  ```diff
  @@ -32,7 +32,7 @@
           raise DataExportError('mapping has no tables')
       targets = [spec.get('target') if isinstance(spec, dict) else None for spec in specs]
       if any(not isinstance(target, str) for target in targets) or len(targets) != len(set(targets)):
  -        raise DataExportError('mapping targets must be unique table names')
  +        raise DataExportError('XXmapping targets must be unique table namesXX')
       prepared = []
       for spec in specs:
  ```

- `src/cargotracker/data_migration/exporter.py:42 Mutant #23`

  ```diff
  @@ -39,7 +39,7 @@
           target = spec['target']
           model = models.get(target)
           if model is None:
  -            raise DataExportError(f'{target}: no registered Django model for target table')
  +            raise DataExportError(f'XX{target}: no registered Django model for target tableXX')
           columns = spec.get('columns')
           if not isinstance(columns, dict) or not columns:
               raise DataExportError(f'{target}: mapping has no columns')
  ```

- `src/cargotracker/data_migration/exporter.py:44 Mutant #28`

  ```diff
  @@ -41,7 +41,7 @@
           if model is None:
               raise DataExportError(f'{target}: no registered Django model for target table')
           columns = spec.get('columns')
  -        if not isinstance(columns, dict) or not columns:
  +        if not isinstance(columns, dict) and not columns:
               raise DataExportError(f'{target}: mapping has no columns')
           fields = {column: _field_for_column(model, column) for column in columns}
           key = spec.get('key')
  ```

- `src/cargotracker/data_migration/exporter.py:45 Mutant #29`

  ```diff
  @@ -42,7 +42,7 @@
               raise DataExportError(f'{target}: no registered Django model for target table')
           columns = spec.get('columns')
           if not isinstance(columns, dict) or not columns:
  -            raise DataExportError(f'{target}: mapping has no columns')
  +            raise DataExportError(f'XX{target}: mapping has no columnsXX')
           fields = {column: _field_for_column(model, column) for column in columns}
           key = spec.get('key')
           if not isinstance(key, list) or not key or any(column not in fields for column in key):
  ```

- `src/cargotracker/data_migration/exporter.py:48 Mutant #36`

  ```diff
  @@ -45,7 +45,7 @@
               raise DataExportError(f'{target}: mapping has no columns')
           fields = {column: _field_for_column(model, column) for column in columns}
           key = spec.get('key')
  -        if not isinstance(key, list) or not key or any(column not in fields for column in key):
  +        if not isinstance(key, list) and not key or any(column not in fields for column in key):
               raise DataExportError(f'{target}: mapping key must name mapped target columns')
           key_fields = [fields[column] for column in key]
           if model._meta.pk not in key_fields:
  ```

- `src/cargotracker/data_migration/exporter.py:49 Mutant #37`

  ```diff
  @@ -46,7 +46,7 @@
           fields = {column: _field_for_column(model, column) for column in columns}
           key = spec.get('key')
           if not isinstance(key, list) or not key or any(column not in fields for column in key):
  -            raise DataExportError(f'{target}: mapping key must name mapped target columns')
  +            raise DataExportError(f'XX{target}: mapping key must name mapped target columnsXX')
           key_fields = [fields[column] for column in key]
           if model._meta.pk not in key_fields:
               raise DataExportError(f'{target}: mapping key must include the primary key')
  ```

- `src/cargotracker/data_migration/exporter.py:52 Mutant #40`

  ```diff
  @@ -49,7 +49,7 @@
               raise DataExportError(f'{target}: mapping key must name mapped target columns')
           key_fields = [fields[column] for column in key]
           if model._meta.pk not in key_fields:
  -            raise DataExportError(f'{target}: mapping key must include the primary key')
  +            raise DataExportError(f'XX{target}: mapping key must include the primary keyXX')
           prepared.append(
               {
                   'target': target,
  ```

- `src/cargotracker/data_migration/exporter.py:66 Mutant #46`

  ```diff
  @@ -63,7 +63,7 @@
   def _timestamp_timezone(mapping):
  -    zone = (mapping.get('defaults') or {}).get('timestamp_tz', 'UTC')
  +    zone = (mapping.get('XXdefaultsXX') or {}).get('timestamp_tz', 'UTC')
       try:
           return ZoneInfo(zone)
       except (TypeError, ZoneInfoNotFoundError) as error:
  ```

- `src/cargotracker/data_migration/exporter.py:66 Mutant #48`

  ```diff
  @@ -63,7 +63,7 @@
   def _timestamp_timezone(mapping):
  -    zone = (mapping.get('defaults') or {}).get('timestamp_tz', 'UTC')
  +    zone = (mapping.get('defaults') or {}).get('XXtimestamp_tzXX', 'UTC')
       try:
           return ZoneInfo(zone)
       except (TypeError, ZoneInfoNotFoundError) as error:
  ```

- `src/cargotracker/data_migration/exporter.py:70 Mutant #51`

  ```diff
  @@ -67,7 +67,7 @@
       try:
           return ZoneInfo(zone)
       except (TypeError, ZoneInfoNotFoundError) as error:
  -        raise DataExportError(f'unknown timestamp timezone {zone!r}') from error
  +        raise DataExportError(f'XXunknown timestamp timezone {zone!r}XX') from error
   def _format_value(value, timezone):
  ```

- `src/cargotracker/data_migration/exporter.py:77 Mutant #54`

  ```diff
  @@ -74,7 +74,7 @@
       if value is None:
           return r'\N'
       if isinstance(value, datetime.datetime):
  -        if value.tzinfo is None or value.utcoffset() is None:
  +        if value.tzinfo is not None or value.utcoffset() is None:
               value = value.replace(tzinfo=timezone)
           return value.astimezone(datetime.UTC).isoformat()
       if isinstance(value, datetime.date):
  ```

- `src/cargotracker/data_migration/exporter.py:77 Mutant #55`

  ```diff
  @@ -74,7 +74,7 @@
       if value is None:
           return r'\N'
       if isinstance(value, datetime.datetime):
  -        if value.tzinfo is None or value.utcoffset() is None:
  +        if value.tzinfo is None or value.utcoffset() is not None:
               value = value.replace(tzinfo=timezone)
           return value.astimezone(datetime.UTC).isoformat()
       if isinstance(value, datetime.date):
  ```

- `src/cargotracker/data_migration/exporter.py:77 Mutant #56`

  ```diff
  @@ -74,7 +74,7 @@
       if value is None:
           return r'\N'
       if isinstance(value, datetime.datetime):
  -        if value.tzinfo is None or value.utcoffset() is None:
  +        if value.tzinfo is None and value.utcoffset() is None:
               value = value.replace(tzinfo=timezone)
           return value.astimezone(datetime.UTC).isoformat()
       if isinstance(value, datetime.date):
  ```

- `src/cargotracker/data_migration/exporter.py:78 Mutant #57`

  ```diff
  @@ -75,7 +75,7 @@
           return r'\N'
       if isinstance(value, datetime.datetime):
           if value.tzinfo is None or value.utcoffset() is None:
  -            value = value.replace(tzinfo=timezone)
  +            value = None
           return value.astimezone(datetime.UTC).isoformat()
       if isinstance(value, datetime.date):
           return value.isoformat()
  ```

- `src/cargotracker/data_migration/exporter.py:83 Mutant #58`

  ```diff
  @@ -80,7 +80,7 @@
       if isinstance(value, datetime.date):
           return value.isoformat()
       if isinstance(value, bool):
  -        return 'true' if value else 'false'
  +        return 'XXtrueXX' if value else 'false'
       return str(value)
  ```

- `src/cargotracker/data_migration/exporter.py:83 Mutant #59`

  ```diff
  @@ -80,7 +80,7 @@
       if isinstance(value, datetime.date):
           return value.isoformat()
       if isinstance(value, bool):
  -        return 'true' if value else 'false'
  +        return 'true' if value else 'XXfalseXX'
       return str(value)
  ```

- `src/cargotracker/data_migration/exporter.py:95 Mutant #73`

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

- `src/cargotracker/data_migration/exporter.py:104 Mutant #77`

  ```diff
  @@ -101,7 +101,7 @@
                   for row in rows
               )
       except OSError as error:
  -        raise DataExportError(f'{path}: {error}') from error
  +        raise DataExportError(f'XX{path}: {error}XX') from error
   def export_snapshot(mapping_path, output_path):
  ```

- `src/cargotracker/data_migration/exporter.py:112 Mutant #82`

  ```diff
  @@ -109,7 +109,7 @@
       try:
           mapping = yaml.safe_load(mapping_file.read_text(encoding='utf-8')) or {}
       except (OSError, yaml.YAMLError) as error:
  -        raise DataExportError(f'{mapping_file}: unable to read mapping: {error}') from error
  +        raise DataExportError(f'XX{mapping_file}: unable to read mapping: {error}XX') from error
       if not isinstance(mapping, dict):
           raise DataExportError(f'{mapping_file}: mapping must be an object')
  ```

- `src/cargotracker/data_migration/exporter.py:114 Mutant #84`

  ```diff
  @@ -111,7 +111,7 @@
       except (OSError, yaml.YAMLError) as error:
           raise DataExportError(f'{mapping_file}: unable to read mapping: {error}') from error
       if not isinstance(mapping, dict):
  -        raise DataExportError(f'{mapping_file}: mapping must be an object')
  +        raise DataExportError(f'XX{mapping_file}: mapping must be an objectXX')
       timezone = _timestamp_timezone(mapping)
       tables = _prepare_tables(mapping, _model_index())
  ```

- `src/cargotracker/data_migration/exporter.py:116 Mutant #85`

  ```diff
  @@ -113,7 +113,7 @@
       if not isinstance(mapping, dict):
           raise DataExportError(f'{mapping_file}: mapping must be an object')
  -    timezone = _timestamp_timezone(mapping)
  +    timezone = None
       tables = _prepare_tables(mapping, _model_index())
       output = Path(output_path)
       try:
  ```

- `src/cargotracker/data_migration/exporter.py:120 Mutant #88`

  ```diff
  @@ -117,7 +117,7 @@
       tables = _prepare_tables(mapping, _model_index())
       output = Path(output_path)
       try:
  -        output.mkdir(parents=True, exist_ok=True)
  +        output.mkdir(parents=False, exist_ok=True)
       except OSError as error:
           raise DataExportError(f'{output}: {error}') from error
       for table in tables:
  ```

- `src/cargotracker/data_migration/exporter.py:120 Mutant #89`

  ```diff
  @@ -117,7 +117,7 @@
       tables = _prepare_tables(mapping, _model_index())
       output = Path(output_path)
       try:
  -        output.mkdir(parents=True, exist_ok=True)
  +        output.mkdir(parents=True, exist_ok=False)
       except OSError as error:
           raise DataExportError(f'{output}: {error}') from error
       for table in tables:
  ```

- `src/cargotracker/data_migration/exporter.py:122 Mutant #90`

  ```diff
  @@ -119,7 +119,7 @@
       try:
           output.mkdir(parents=True, exist_ok=True)
       except OSError as error:
  -        raise DataExportError(f'{output}: {error}') from error
  +        raise DataExportError(f'XX{output}: {error}XX') from error
       for table in tables:
           _write_table(output, table, timezone)
       return [(table['target'], table['model']._base_manager.count()) for table in tables]
  ```

- `src/cargotracker/data_migration/management/commands/export_data_snapshot.py:7 Mutant #1`

  ```diff
  @@ -4,7 +4,7 @@
   class Command(BaseCommand):
  -    help = 'Export mapped target tables as a relational snapshot.'
  +    help = 'XXExport mapped target tables as a relational snapshot.XX'
       def add_arguments(self, parser):
           parser.add_argument('--mapping', required=True)
  ```

- `src/cargotracker/data_migration/management/commands/export_data_snapshot.py:7 Mutant #2`

  ```diff
  @@ -4,7 +4,7 @@
   class Command(BaseCommand):
  -    help = 'Export mapped target tables as a relational snapshot.'
  +    help = None
       def add_arguments(self, parser):
           parser.add_argument('--mapping', required=True)
  ```

- `src/cargotracker/data_migration/management/commands/export_data_snapshot.py:10 Mutant #4`

  ```diff
  @@ -7,7 +7,7 @@
       help = 'Export mapped target tables as a relational snapshot.'
       def add_arguments(self, parser):
  -        parser.add_argument('--mapping', required=True)
  +        parser.add_argument('--mapping', required=False)
           parser.add_argument('--out', required=True)
       def handle(self, *args, **options):
  ```

- `src/cargotracker/data_migration/management/commands/export_data_snapshot.py:11 Mutant #6`

  ```diff
  @@ -8,7 +8,7 @@
       def add_arguments(self, parser):
           parser.add_argument('--mapping', required=True)
  -        parser.add_argument('--out', required=True)
  +        parser.add_argument('--out', required=False)
       def handle(self, *args, **options):
           try:
  ```

- `src/cargotracker/data_migration/management/commands/export_data_snapshot.py:18 Mutant #10`

  ```diff
  @@ -15,7 +15,7 @@
               exported = export_snapshot(options['mapping'], options['out'])
           except DataExportError as error:
               raise CommandError(str(error)) from error
  -        total = sum(rows for _, rows in exported)
  +        total = None
           self.stdout.write(
               self.style.SUCCESS(f'Exported {total} rows across {len(exported)} mapped tables.')
           )
  ```

- `src/cargotracker/data_migration/management/commands/export_data_snapshot.py:20 Mutant #11`

  ```diff
  @@ -17,6 +17,6 @@
               raise CommandError(str(error)) from error
           total = sum(rows for _, rows in exported)
           self.stdout.write(
  -            self.style.SUCCESS(f'Exported {total} rows across {len(exported)} mapped tables.')
  +            self.style.SUCCESS(f'XXExported {total} rows across {len(exported)} mapped tables.XX')
           )
  ```

