# Surviving mutants: DM-05C

Written by `afs-mutation` on its last run (base `origin/main`): score 0.752, threshold 0.8, killed 227, survived 75. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

- `src/cargotracker/data_migration/loader.py:27 Mutant #16`

  ```diff
  @@ -24,7 +24,7 @@
           return None
       if isinstance(transform, dict):
           if 'map' not in transform:
  -            raise DataLoadError(f'unknown transform {transform!r}')
  +            raise DataLoadError(f'XXunknown transform {transform!r}XX')
           mapping = transform['map']
           if value in mapping:
               result = mapping[value]
  ```

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

- `src/cargotracker/data_migration/loader.py:34 Mutant #23`

  ```diff
  @@ -31,7 +31,7 @@
           elif str(value) in mapping:
               result = mapping[str(value)]
           else:
  -            raise DataLoadError(f'no mapping for value {value!r}')
  +            raise DataLoadError(f'XXno mapping for value {value!r}XX')
           return None if result is None else str(result)
       if transform in ('identity', None):
           return value
  ```

- `src/cargotracker/data_migration/loader.py:52 Mutant #44`

  ```diff
  @@ -49,7 +49,7 @@
               return True
           if normalized in FALSE:
               return False
  -        raise DataLoadError(f'not a boolean: {value!r}')
  +        raise DataLoadError(f'XXnot a boolean: {value!r}XX')
       if transform in ('timestamp', 'date'):
           if transform == 'date' and len(value.strip()) <= 10:
               parsed = datetime.date.fromisoformat(value.strip())
  ```

- `src/cargotracker/data_migration/loader.py:54 Mutant #48`

  ```diff
  @@ -51,7 +51,7 @@
               return False
           raise DataLoadError(f'not a boolean: {value!r}')
       if transform in ('timestamp', 'date'):
  -        if transform == 'date' and len(value.strip()) <= 10:
  +        if transform != 'date' and len(value.strip()) <= 10:
               parsed = datetime.date.fromisoformat(value.strip())
               return parsed
           try:
  ```

- `src/cargotracker/data_migration/loader.py:54 Mutant #49`

  ```diff
  @@ -51,7 +51,7 @@
               return False
           raise DataLoadError(f'not a boolean: {value!r}')
       if transform in ('timestamp', 'date'):
  -        if transform == 'date' and len(value.strip()) <= 10:
  +        if transform == 'XXdateXX' and len(value.strip()) <= 10:
               parsed = datetime.date.fromisoformat(value.strip())
               return parsed
           try:
  ```

- `src/cargotracker/data_migration/loader.py:54 Mutant #50`

  ```diff
  @@ -51,7 +51,7 @@
               return False
           raise DataLoadError(f'not a boolean: {value!r}')
       if transform in ('timestamp', 'date'):
  -        if transform == 'date' and len(value.strip()) <= 10:
  +        if transform == 'date' and len(value.strip()) < 10:
               parsed = datetime.date.fromisoformat(value.strip())
               return parsed
           try:
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

- `src/cargotracker/data_migration/loader.py:54 Mutant #52`

  ```diff
  @@ -51,7 +51,7 @@
               return False
           raise DataLoadError(f'not a boolean: {value!r}')
       if transform in ('timestamp', 'date'):
  -        if transform == 'date' and len(value.strip()) <= 10:
  +        if transform == 'date' or len(value.strip()) <= 10:
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

- `src/cargotracker/data_migration/loader.py:63 Mutant #57`

  ```diff
  @@ -60,7 +60,7 @@
               for pattern in (
                   '%Y-%m-%d %H:%M:%S.%f%z',
                   '%Y-%m-%d %H:%M:%S%z',
  -                '%Y-%m-%d %H:%M',
  +                'XX%Y-%m-%d %H:%MXX',
               ):
                   try:
                       parsed = datetime.datetime.strptime(value.strip(), pattern)
  ```

- `src/cargotracker/data_migration/loader.py:66 Mutant #58`

  ```diff
  @@ -63,7 +63,7 @@
                   '%Y-%m-%d %H:%M',
               ):
                   try:
  -                    parsed = datetime.datetime.strptime(value.strip(), pattern)
  +                    parsed = None
                       break
                   except ValueError:
                       continue
  ```

- `src/cargotracker/data_migration/loader.py:67 Mutant #59`

  ```diff
  @@ -64,7 +64,7 @@
               ):
                   try:
                       parsed = datetime.datetime.strptime(value.strip(), pattern)
  -                    break
  +                    continue
                   except ValueError:
                       continue
               else:
  ```

- `src/cargotracker/data_migration/loader.py:69 Mutant #60`

  ```diff
  @@ -66,7 +66,7 @@
                       parsed = datetime.datetime.strptime(value.strip(), pattern)
                       break
                   except ValueError:
  -                    continue
  +                    break
               else:
                   raise DataLoadError(f'not a timestamp: {value!r}')
           if parsed.tzinfo is None:
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

- `src/cargotracker/data_migration/loader.py:78 Mutant #67`

  ```diff
  @@ -75,7 +75,7 @@
           if transform == 'date':
               return parsed.date()
           return parsed
  -    raise DataLoadError(f'unknown transform {transform!r}')
  +    raise DataLoadError(f'XXunknown transform {transform!r}XX')
   def _column_specs(spec):
  ```

- `src/cargotracker/data_migration/loader.py:83 Mutant #72`

  ```diff
  @@ -80,7 +80,7 @@
   def _column_specs(spec):
       columns = spec.get('columns')
  -    if not isinstance(columns, dict) or not columns:
  +    if not isinstance(columns, dict) and not columns:
           raise DataLoadError(f'{spec.get("target")}: mapping has no columns')
       result = []
       for target_column, definition in columns.items():
  ```

- `src/cargotracker/data_migration/loader.py:84 Mutant #73`

  ```diff
  @@ -81,7 +81,7 @@
   def _column_specs(spec):
       columns = spec.get('columns')
       if not isinstance(columns, dict) or not columns:
  -        raise DataLoadError(f'{spec.get("target")}: mapping has no columns')
  +        raise DataLoadError(f'{spec.get("XXtargetXX")}: mapping has no columns')
       result = []
       for target_column, definition in columns.items():
           if isinstance(definition, dict):
  ```

- `src/cargotracker/data_migration/loader.py:84 Mutant #74`

  ```diff
  @@ -81,7 +81,7 @@
   def _column_specs(spec):
       columns = spec.get('columns')
       if not isinstance(columns, dict) or not columns:
  -        raise DataLoadError(f'{spec.get("target")}: mapping has no columns')
  +        raise DataLoadError(f'XX{spec.get("target")}: mapping has no columnsXX')
       result = []
       for target_column, definition in columns.items():
           if isinstance(definition, dict):
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

- `src/cargotracker/data_migration/loader.py:94 Mutant #85`

  ```diff
  @@ -91,7 +91,7 @@
               source_column = definition
               transform = 'identity'
           if not isinstance(source_column, str):
  -            raise DataLoadError(f'{target_column}: mapping must name a source column')
  +            raise DataLoadError(f'XX{target_column}: mapping must name a source columnXX')
           result.append((target_column, source_column, transform))
       return result
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

- `src/cargotracker/data_migration/loader.py:117 Mutant #95`

  ```diff
  @@ -114,7 +114,7 @@
   def _read_manifest(snapshot):
       path = snapshot / 'manifest.json'
       if not path.is_file():
  -        raise DataLoadError(f'{path}: no manifest.json')
  +        raise DataLoadError(f'XX{path}: no manifest.jsonXX')
       try:
           manifest = json.loads(path.read_text(encoding='utf-8'))
       except (OSError, json.JSONDecodeError) as error:
  ```

- `src/cargotracker/data_migration/loader.py:121 Mutant #98`

  ```diff
  @@ -118,7 +118,7 @@
       try:
           manifest = json.loads(path.read_text(encoding='utf-8'))
       except (OSError, json.JSONDecodeError) as error:
  -        raise DataLoadError(f'{path}: invalid manifest: {error}') from error
  +        raise DataLoadError(f'XX{path}: invalid manifest: {error}XX') from error
       if not isinstance(manifest.get('tables'), dict):
           raise DataLoadError(f'{path}: tables must be an object')
       return manifest
  ```

- `src/cargotracker/data_migration/loader.py:123 Mutant #101`

  ```diff
  @@ -120,7 +120,7 @@
       except (OSError, json.JSONDecodeError) as error:
           raise DataLoadError(f'{path}: invalid manifest: {error}') from error
       if not isinstance(manifest.get('tables'), dict):
  -        raise DataLoadError(f'{path}: tables must be an object')
  +        raise DataLoadError(f'XX{path}: tables must be an objectXX')
       return manifest
  ```

- `src/cargotracker/data_migration/loader.py:130 Mutant #105`

  ```diff
  @@ -127,7 +127,7 @@
   def _read_source_rows(snapshot, source, manifest):
       metadata = manifest['tables'].get(source)
       if metadata is None:
  -        raise DataLoadError(f'{source}: table is not listed in the snapshot manifest')
  +        raise DataLoadError(f'XX{source}: table is not listed in the snapshot manifestXX')
       path = snapshot / f'{source}.csv'
       if not path.is_file():
           raise DataLoadError(f'{path}: missing')
  ```

- `src/cargotracker/data_migration/loader.py:133 Mutant #110`

  ```diff
  @@ -130,7 +130,7 @@
           raise DataLoadError(f'{source}: table is not listed in the snapshot manifest')
       path = snapshot / f'{source}.csv'
       if not path.is_file():
  -        raise DataLoadError(f'{path}: missing')
  +        raise DataLoadError(f'XX{path}: missingXX')
       if (
           metadata.get('sha256')
           and hashlib.sha256(path.read_bytes()).hexdigest() != metadata['sha256']
  ```

- `src/cargotracker/data_migration/loader.py:138 Mutant #115`

  ```diff
  @@ -135,7 +135,7 @@
           metadata.get('sha256')
           and hashlib.sha256(path.read_bytes()).hexdigest() != metadata['sha256']
       ):
  -        raise DataLoadError(f'{source}: sha256 differs from the snapshot manifest')
  +        raise DataLoadError(f'XX{source}: sha256 differs from the snapshot manifestXX')
       marker = manifest.get('null', '\\N')
       try:
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

- `src/cargotracker/data_migration/loader.py:146 Mutant #124`

  ```diff
  @@ -143,7 +143,7 @@
               reader = csv.reader(stream)
               header = next(reader, None)
               if not header:
  -                raise DataLoadError(f'{path}: empty file (a header row is required)')
  +                raise DataLoadError(f'XX{path}: empty file (a header row is required)XX')
               if len(header) != len(set(header)):
                   raise DataLoadError(f'{path}: duplicate columns in header')
               rows = []
  ```

- `src/cargotracker/data_migration/loader.py:148 Mutant #126`

  ```diff
  @@ -145,7 +145,7 @@
               if not header:
                   raise DataLoadError(f'{path}: empty file (a header row is required)')
               if len(header) != len(set(header)):
  -                raise DataLoadError(f'{path}: duplicate columns in header')
  +                raise DataLoadError(f'XX{path}: duplicate columns in headerXX')
               rows = []
               for line, row in enumerate(reader, start=2):
                   if len(row) != len(header):
  ```

- `src/cargotracker/data_migration/loader.py:150 Mutant #128`

  ```diff
  @@ -147,7 +147,7 @@
               if len(header) != len(set(header)):
                   raise DataLoadError(f'{path}: duplicate columns in header')
               rows = []
  -            for line, row in enumerate(reader, start=2):
  +            for line, row in enumerate(reader, start=3):
                   if len(row) != len(header):
                       raise DataLoadError(
                           f'{path}:{line}: {len(row)} fields, header has {len(header)}'
  ```

- `src/cargotracker/data_migration/loader.py:153 Mutant #130`

  ```diff
  @@ -150,7 +150,7 @@
               for line, row in enumerate(reader, start=2):
                   if len(row) != len(header):
                       raise DataLoadError(
  -                        f'{path}:{line}: {len(row)} fields, header has {len(header)}'
  +                        f'XX{path}:{line}: {len(row)} fields, header has {len(header)}XX'
                       )
                   rows.append(
                       dict(zip(header, (None if value == marker else value for value in row)))
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

- `src/cargotracker/data_migration/loader.py:162 Mutant #139`

  ```diff
  @@ -159,7 +159,7 @@
           raise DataLoadError(f'{path}: {error}') from error
       if 'rows' in metadata and len(rows) != metadata['rows']:
  -        raise DataLoadError(f'{source}: {len(rows)} rows, manifest says {metadata["rows"]}')
  +        raise DataLoadError(f'XX{source}: {len(rows)} rows, manifest says {metadata["rows"]}XX')
       return rows
  ```

- `src/cargotracker/data_migration/loader.py:171 Mutant #145`

  ```diff
  @@ -168,7 +168,7 @@
       try:
           return ZoneInfo(zone)
       except (TypeError, ZoneInfoNotFoundError) as error:
  -        raise DataLoadError(f'unknown timestamp timezone {zone!r}') from error
  +        raise DataLoadError(f'XXunknown timestamp timezone {zone!r}XX') from error
   def _prepare_tables(mapping, models):
  ```

- `src/cargotracker/data_migration/loader.py:177 Mutant #151`

  ```diff
  @@ -174,7 +174,7 @@
   def _prepare_tables(mapping, models):
       specs = mapping.get('tables')
       if not isinstance(specs, list) or not specs:
  -        raise DataLoadError('mapping has no tables')
  +        raise DataLoadError('XXmapping has no tablesXX')
       targets = [spec.get('target') for spec in specs]
       if any(not isinstance(target, str) for target in targets) or len(targets) != len(set(targets)):
           raise DataLoadError('mapping targets must be unique table names')
  ```

- `src/cargotracker/data_migration/loader.py:180 Mutant #157`

  ```diff
  @@ -177,7 +177,7 @@
           raise DataLoadError('mapping has no tables')
       targets = [spec.get('target') for spec in specs]
       if any(not isinstance(target, str) for target in targets) or len(targets) != len(set(targets)):
  -        raise DataLoadError('mapping targets must be unique table names')
  +        raise DataLoadError('XXmapping targets must be unique table namesXX')
       prepared = []
       for spec in specs:
           target = spec['target']
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

- `src/cargotracker/data_migration/loader.py:190 Mutant #167`

  ```diff
  @@ -187,7 +187,7 @@
           columns = _column_specs(spec)
           fields = {name: _field_for_column(model, name) for name, _, _ in columns}
           if model._meta.pk not in fields.values():
  -            raise DataLoadError(f'{target}: mapping must include its primary key')
  +            raise DataLoadError(f'XX{target}: mapping must include its primary keyXX')
           prepared.append({'spec': spec, 'model': model, 'columns': columns, 'fields': fields})
       target_indexes = {entry['spec']['target']: index for index, entry in enumerate(prepared)}
  ```

- `src/cargotracker/data_migration/loader.py:200 Mutant #185`

  ```diff
  @@ -197,7 +197,7 @@
           for column, reference in refs.items():
               if column not in entry['fields']:
                   raise DataLoadError(
  -                    f'{entry["spec"]["target"]}: reference {column!r} is not mapped'
  +                    f'XX{entry["spec"]["target"]}: reference {column!r} is not mappedXX'
                   )
               try:
                   table, referenced_column = reference.rsplit('.', 1)
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

- `src/cargotracker/data_migration/loader.py:205 Mutant #189`

  ```diff
  @@ -202,7 +202,7 @@
               try:
                   table, referenced_column = reference.rsplit('.', 1)
               except (AttributeError, ValueError) as error:
  -                raise DataLoadError(f'{column}: invalid reference {reference!r}') from error
  +                raise DataLoadError(f'XX{column}: invalid reference {reference!r}XX') from error
               referenced_entry = next(
                   (candidate for candidate in prepared if candidate['spec']['target'] == table),
                   None,
  ```

- `src/cargotracker/data_migration/loader.py:211 Mutant #195`

  ```diff
  @@ -208,7 +208,7 @@
                   None,
               )
               if referenced_entry is None:
  -                raise DataLoadError(f'{column}: reference target {table!r} is not mapped')
  +                raise DataLoadError(f'XX{column}: reference target {table!r} is not mappedXX')
               field = entry['fields'][column]
               if not field.is_relation or field.remote_field.model is not referenced_entry['model']:
                   raise DataLoadError(
  ```

- `src/cargotracker/data_migration/loader.py:215 Mutant #204`

  ```diff
  @@ -212,7 +212,7 @@
               field = entry['fields'][column]
               if not field.is_relation or field.remote_field.model is not referenced_entry['model']:
                   raise DataLoadError(
  -                    f'{entry["spec"]["target"]}.{column}: reference does not match the model'
  +                    f'XX{entry["spec"]["target"]}.{column}: reference does not match the modelXX'
                   )
               if not any(
                   candidate.column == referenced_column
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

- `src/cargotracker/data_migration/loader.py:223 Mutant #211`

  ```diff
  @@ -220,7 +220,7 @@
                   or candidate.attname == referenced_column
                   for candidate in referenced_entry['model']._meta.concrete_fields
               ):
  -                raise DataLoadError(f'{reference}: no referenced target column')
  +                raise DataLoadError(f'XX{reference}: no referenced target columnXX')
               entry['refs'][column] = {
                   'target_index': target_indexes[table],
                   'field': field,
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

- `src/cargotracker/data_migration/loader.py:253 Mutant #240`

  ```diff
  @@ -250,7 +250,7 @@
       missing = required_sources.difference(source_rows[0].keys()) if source_rows else set()
       if missing:
           raise DataLoadError(
  -            f'{spec["source"]}: no column(s) {", ".join(sorted(missing))} in its CSV header'
  +            f'XX{spec["source"]}: no column(s) {", ".join(sorted(missing))} in its CSV headerXX'
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

