from django.db import models


class CargoRecord(models.Model):
    tracking_id = models.CharField(max_length=255, db_column='tracking_id', unique=True)
    origin = models.ForeignKey(
        'location.LocationRecord',
        db_column='origin_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    spec_origin = models.ForeignKey(
        'location.LocationRecord',
        db_column='spec_origin_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    spec_destination = models.ForeignKey(
        'location.LocationRecord',
        db_column='spec_destination_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    spec_arrival_deadline = models.DateField(db_column='spec_arrival_deadline')
    transport_status = models.CharField(max_length=255, db_column='transport_status')
    last_known_location = models.ForeignKey(
        'location.LocationRecord',
        db_column='last_known_location_id',
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    current_voyage = models.ForeignKey(
        'voyage.VoyageRecord',
        db_column='current_voyage_id',
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    misdirected = models.BooleanField(db_column='misdirected')
    eta = models.DateField(db_column='eta', null=True)
    next_expected_handling_event_type = models.CharField(
        max_length=255,
        db_column='next_expected_handling_event_type',
        null=True,
    )
    next_expected_location = models.ForeignKey(
        'location.LocationRecord',
        db_column='next_expected_location_id',
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    next_expected_voyage = models.ForeignKey(
        'voyage.VoyageRecord',
        db_column='next_expected_voyage_id',
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    unloaded_at_dest = models.BooleanField(db_column='unloaded_at_dest')
    routing_status = models.CharField(max_length=255, db_column='routing_status')
    calculated_at = models.DateTimeField(db_column='calculated_at')
    last_event = models.ForeignKey(
        'handling.HandlingEventRecord',
        db_column='last_event_id',
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
    )

    class Meta:
        db_table = 'cargo'


class LegRecord(models.Model):
    cargo = models.ForeignKey(
        CargoRecord,
        db_column='cargo_id',
        on_delete=models.CASCADE,
        related_name='legs',
    )
    voyage = models.ForeignKey(
        'voyage.VoyageRecord',
        db_column='voyage_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    load_location = models.ForeignKey(
        'location.LocationRecord',
        db_column='load_location_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    unload_location = models.ForeignKey(
        'location.LocationRecord',
        db_column='unload_location_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    load_time = models.DateTimeField(db_column='load_time')
    unload_time = models.DateTimeField(db_column='unload_time')

    class Meta:
        db_table = 'leg'
        ordering = ('load_time',)
