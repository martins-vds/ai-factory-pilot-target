import csv
import datetime
import decimal
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml
from django.apps import apps
from django.core.management.color import no_style
from django.db import connection, transaction


TRUE = {'1', 'true', 't', 'yes', 'y'}
FALSE = {'0', 'false', 'f', 'no', 'n'}


class DataLoadError(Exception):
    pass


def _transform(value, transform, timezone):
    if value is None:
        return None
    if isinstance(transform, dict):
        if 'map' not in transform:
            raise DataLoadError(f'unknown transform {transform!r}')
        mapping = transform['map']
        if value in mapping:
            result = mapping[value]
        elif str(value) in mapping:
            result = mapping[str(value)]
        else:
            raise DataLoadError(f'no mapping for value {value!r}')
        return None if result is None else str(result)
    if transform in ('identity', None):
        return value
    if transform == 'trim':
        return value.strip()
    if transform == 'null_if_empty':
        return None if value.strip() == '' else value
    if transform == 'int':
        return int(decimal.Decimal(value.strip()))
    if transform == 'decimal':
        return decimal.Decimal(value.strip())
    if transform == 'bool':
        normalized = value.strip().lower()
        if normalized in TRUE:
            return True
        if normalized in FALSE:
            return False
        raise DataLoadError(f'not a boolean: {value!r}')
    if transform in ('timestamp', 'date'):
        if transform == 'date' and len(value.strip()) <= 10:
            parsed = datetime.date.fromisoformat(value.strip())
            return parsed
        try:
            parsed = datetime.datetime.fromisoformat(value.strip().replace('Z', '+00:00'))
        except ValueError:
            for pattern in (
                '%Y-%m-%d %H:%M:%S.%f%z',
                '%Y-%m-%d %H:%M:%S%z',
                '%Y-%m-%d %H:%M',
            ):
                try:
                    parsed = datetime.datetime.strptime(value.strip(), pattern)
                    break
                except ValueError:
                    continue
            else:
                raise DataLoadError(f'not a timestamp: {value!r}')
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone)
        parsed = parsed.astimezone(datetime.timezone.utc)
        if transform == 'date':
            return parsed.date()
        return parsed
    raise DataLoadError(f'unknown transform {transform!r}')


def _column_specs(spec):
    columns = spec.get('columns')
    if not isinstance(columns, dict) or not columns:
        raise DataLoadError(f'{spec.get("target")}: mapping has no columns')
    result = []
    for target_column, definition in columns.items():
        if isinstance(definition, dict):
            source_column = definition.get('from')
            transform = definition.get('as', 'identity')
        else:
            source_column = definition
            transform = 'identity'
        if not isinstance(source_column, str):
            raise DataLoadError(f'{target_column}: mapping must name a source column')
        result.append((target_column, source_column, transform))
    return result


def _model_index():
    return {
        model._meta.db_table: model
        for model in apps.get_models()
        if not model._meta.proxy and not model._meta.auto_created
    }


def _field_for_column(model, column):
    for field in model._meta.concrete_fields:
        if column in (field.column, field.name, field.attname):
            return field
    raise DataLoadError(f'{model._meta.db_table}: no target column {column!r}')


def _read_manifest(snapshot):
    path = snapshot / 'manifest.json'
    if not path.is_file():
        raise DataLoadError(f'{path}: no manifest.json')
    try:
        manifest = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise DataLoadError(f'{path}: invalid manifest: {error}') from error
    if not isinstance(manifest.get('tables'), dict):
        raise DataLoadError(f'{path}: tables must be an object')
    return manifest


def _read_source_rows(snapshot, source, manifest):
    metadata = manifest['tables'].get(source)
    if metadata is None:
        raise DataLoadError(f'{source}: table is not listed in the snapshot manifest')
    path = snapshot / f'{source}.csv'
    if not path.is_file():
        raise DataLoadError(f'{path}: missing')
    if metadata.get('sha256') and hashlib.sha256(path.read_bytes()).hexdigest() != metadata['sha256']:
        raise DataLoadError(f'{source}: sha256 differs from the snapshot manifest')

    marker = manifest.get('null', '\\N')
    try:
        with path.open(newline='', encoding='utf-8') as stream:
            reader = csv.reader(stream)
            header = next(reader, None)
            if not header:
                raise DataLoadError(f'{path}: empty file (a header row is required)')
            if len(header) != len(set(header)):
                raise DataLoadError(f'{path}: duplicate columns in header')
            rows = []
            for line, row in enumerate(reader, start=2):
                if len(row) != len(header):
                    raise DataLoadError(
                        f'{path}:{line}: {len(row)} fields, header has {len(header)}'
                    )
                rows.append(dict(zip(header, (None if value == marker else value for value in row))))
    except OSError as error:
        raise DataLoadError(f'{path}: {error}') from error

    if 'rows' in metadata and len(rows) != metadata['rows']:
        raise DataLoadError(
            f'{source}: {len(rows)} rows, manifest says {metadata["rows"]}'
        )
    return rows


def _mapping_timezone(mapping):
    zone = (mapping.get('defaults') or {}).get('timestamp_tz', 'UTC')
    try:
        return ZoneInfo(zone)
    except (TypeError, ZoneInfoNotFoundError) as error:
        raise DataLoadError(f'unknown timestamp timezone {zone!r}') from error


def _prepare_tables(mapping, models):
    specs = mapping.get('tables')
    if not isinstance(specs, list) or not specs:
        raise DataLoadError('mapping has no tables')
    targets = [spec.get('target') for spec in specs]
    if any(not isinstance(target, str) for target in targets) or len(targets) != len(set(targets)):
        raise DataLoadError('mapping targets must be unique table names')
    prepared = []
    for spec in specs:
        target = spec['target']
        model = models.get(target)
        if model is None:
            raise DataLoadError(f'{target}: no registered Django model for target table')
        columns = _column_specs(spec)
        fields = {name: _field_for_column(model, name) for name, _, _ in columns}
        if model._meta.pk not in fields.values():
            raise DataLoadError(f'{target}: mapping must include its primary key')
        prepared.append({'spec': spec, 'model': model, 'columns': columns, 'fields': fields})

    target_indexes = {entry['spec']['target']: index for index, entry in enumerate(prepared)}
    for index, entry in enumerate(prepared):
        refs = entry['spec'].get('refs') or {}
        entry['refs'] = {}
        for column, reference in refs.items():
            if column not in entry['fields']:
                raise DataLoadError(f'{entry["spec"]["target"]}: reference {column!r} is not mapped')
            try:
                table, referenced_column = reference.rsplit('.', 1)
            except (AttributeError, ValueError) as error:
                raise DataLoadError(f'{column}: invalid reference {reference!r}') from error
            referenced_entry = next(
                (candidate for candidate in prepared if candidate['spec']['target'] == table),
                None,
            )
            if referenced_entry is None:
                raise DataLoadError(f'{column}: reference target {table!r} is not mapped')
            field = entry['fields'][column]
            if not field.is_relation or field.remote_field.model is not referenced_entry['model']:
                raise DataLoadError(
                    f'{entry["spec"]["target"]}.{column}: reference does not match the model'
                )
            if not any(
                candidate.column == referenced_column
                or candidate.name == referenced_column
                or candidate.attname == referenced_column
                for candidate in referenced_entry['model']._meta.concrete_fields
            ):
                raise DataLoadError(f'{reference}: no referenced target column')
            entry['refs'][column] = {
                'target_index': target_indexes[table],
                'field': field,
                'target_model': referenced_entry['model'],
            }
    return prepared


@transaction.atomic
def load_snapshot(snapshot_path, mapping_path):
    if connection.vendor != 'postgresql':
        raise DataLoadError('load_data_snapshot requires PostgreSQL')
    snapshot = Path(snapshot_path)
    mapping_file = Path(mapping_path)
    try:
        mapping = yaml.safe_load(mapping_file.read_text(encoding='utf-8')) or {}
    except (OSError, yaml.YAMLError) as error:
        raise DataLoadError(f'{mapping_file}: unable to read mapping: {error}') from error
    if not isinstance(mapping, dict):
        raise DataLoadError(f'{mapping_file}: mapping must be an object')

    manifest = _read_manifest(snapshot)
    timezone = _mapping_timezone(mapping)
    prepared = _prepare_tables(mapping, _model_index())
    pending = []
    row_counts = []

    for index, entry in enumerate(prepared):
        model = entry['model']
        for column, reference in entry['refs'].items():
            if reference['target_index'] > index:
                if not reference['field'].null:
                    raise DataLoadError(
                        f'{entry["spec"]["target"]}.{column}: a forward reference must be nullable'
                    )
                model._base_manager.all().update(**{reference['field'].attname: None})
    for entry in reversed(prepared):
        entry['model']._base_manager.all().delete()

    for index, entry in enumerate(prepared):
        spec = entry['spec']
        model = entry['model']
        source_rows = _read_source_rows(snapshot, spec['source'], manifest)
        required_sources = {source for _, source, _ in entry['columns']}
        missing = required_sources.difference(source_rows[0].keys()) if source_rows else set()
        if missing:
            raise DataLoadError(
                f'{spec["source"]}: no column(s) {", ".join(sorted(missing))} in its CSV header'
            )
        objects = []
        for row in source_rows:
            values = {}
            for target_column, source_column, transform in entry['columns']:
                field = entry['fields'][target_column]
                value = _transform(row[source_column], transform, timezone)
                reference = entry['refs'].get(target_column)
                if reference and reference['target_index'] > index and value is not None:
                    pending.append((model, values, field, value))
                    value = None
                values[field.attname] = value
            if values[model._meta.pk.attname] is None:
                raise DataLoadError(f'{spec["source"]}: primary key cannot be NULL')
            objects.append(model(**values))
        model._base_manager.bulk_create(objects, batch_size=1000)
        row_counts.append((spec['target'], len(source_rows)))

    for model, values, field, value in pending:
        model._base_manager.filter(pk=values[model._meta.pk.attname]).update(
            **{field.attname: value}
        )

    reset_sql = connection.ops.sequence_reset_sql(
        no_style(),
        [entry['model'] for entry in prepared],
    )
    with connection.cursor() as cursor:
        for statement in reset_sql:
            cursor.execute(statement)

    return row_counts
