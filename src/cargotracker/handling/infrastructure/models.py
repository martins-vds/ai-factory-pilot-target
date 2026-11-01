from django.db import models


class HandlingEventRecord(models.Model):
    event_type = models.CharField(max_length=255, db_column='type')
    voyage = models.ForeignKey(
        'voyage.VoyageRecord',
        db_column='voyage_id',
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    location = models.ForeignKey(
        'location.LocationRecord',
        db_column='location_id',
        on_delete=models.PROTECT,
        related_name='+',
    )
    completion_time = models.DateField(db_column='completionTime')
    registration_time = models.DateField(db_column='registration')
    cargo = models.ForeignKey(
        'cargo.CargoRecord',
        db_column='cargo_id',
        on_delete=models.PROTECT,
        related_name='+',
    )

    class Meta:
        db_table = 'HandlingEvent'
