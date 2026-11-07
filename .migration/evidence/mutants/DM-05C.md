# Surviving mutants: DM-05C

Written by `afs-mutation` on its last run (base `origin/main`): score 0.966, threshold 0.8, killed 288, survived 10. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

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

  Classification: equivalent. After `strip()`, the supported `date.fromisoformat` representations in this loader are at most 10 characters; the extra length of 11 admits no additional valid date input.

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

  Classification: equivalent. The unchanged `_transform` branch accepts both `'identity'` and `None`, so scalar-column mapping yields the same value either way.

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

  Classification: equivalent for the registered target models. The repository defines no proxy models, and `apps.get_models()` excludes auto-created models by default.

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

  Classification: equivalent for the approved mapping. Every mapped reference names `.id` (`.migration/data/mapping.yaml:62-122`), whose field `column`, `name`, and `attname` are identical.

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

  Classification: equivalent for the approved mapping. The mutant adds same-table references to the forward-reference check; no mapped table references itself.

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

  Classification: equivalent for the approved mapping. The mutant only defers same-table references, and the mapping contains no self-references.

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

  Classification: equivalent at the persisted-data boundary for the current schema. Deferred references target nullable integer foreign keys; Django/PostgreSQL persist the empty string as NULL, and the cycle test observes NULL before restoration and the original key afterward.

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

  Classification: equivalent for loaded data. Changing `bulk_create` batch size from 1000 to 1001 changes only the internal batch boundary, not the rows or transaction result.

- `src/cargotracker/data_migration/apps.py:5 Mutant #1`

  ```diff
  @@ -2,6 +2,6 @@
   class DataMigrationConfig(AppConfig):
  -    default_auto_field = 'django.db.models.BigAutoField'
  +    default_auto_field = 'XXdjango.db.models.BigAutoFieldXX'
       name = 'cargotracker.data_migration'
  ```

  Classification: equivalent. The data-migration app defines no models, so its `default_auto_field` value does not affect target schema or loaded data.

- `src/cargotracker/data_migration/apps.py:5 Mutant #2`

  ```diff
  @@ -2,6 +2,6 @@
   class DataMigrationConfig(AppConfig):
  -    default_auto_field = 'django.db.models.BigAutoField'
  +    default_auto_field = None
       name = 'cargotracker.data_migration'
  ```

  Classification: equivalent. The data-migration app defines no models, so setting `default_auto_field` to `None` has no observable effect on this loader.
