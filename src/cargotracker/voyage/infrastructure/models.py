from django.db import models


class VoyageRecord(models.Model):
    voyage_number = models.CharField(max_length=255, db_column='voyage_number')

    class Meta:
        db_table = 'voyage'


class CarrierMovementRecord(models.Model):
    arrival_time = models.DateTimeField(db_column='arrival_time')
    departure_time = models.DateTimeField(db_column='departure_time')
    arrival_location = models.ForeignKey(
        'location.LocationRecord',
        db_column='arrival_location_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    departure_location = models.ForeignKey(
        'location.LocationRecord',
        db_column='departure_location_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    voyage = models.ForeignKey(
        'voyage.VoyageRecord',
        db_column='voyage_id',
        on_delete=models.PROTECT,
        related_name='+',
    )

    class Meta:
        db_table = 'carrier_movement'
