# Surviving mutants: DM-05D

Written by `afs-mutation` on its last run (base `origin/main`): score 0.932, threshold 0.8, killed 96, survived 7. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent. The diff under each line is the change mutmut made.

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

- `src/cargotracker/data_migration/exporter.py:59 Mutant #45`

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

- `src/cargotracker/data_migration/exporter.py:95 Mutant #72`

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

- `src/cargotracker/data_migration/management/commands/export_data_snapshot.py:7 Mutant #1`

  ```diff
  @@ -4,7 +4,7 @@
   class Command(BaseCommand):
  -    help = 'Export mapped target tables as a relational snapshot.'
  +    help = 'XXExport mapped target tables as a relational snapshot.XX'
       def add_arguments(self, parser):
           parser.add_argument('--mapping', required=True)
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

