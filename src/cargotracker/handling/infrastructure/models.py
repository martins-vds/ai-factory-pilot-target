from typing import ClassVar

from django.db import models

from cargotracker.handling.domain.registration_attempt import RegistrationAttemptStatus


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
    completion_time = models.DateTimeField(db_column='completionTime')
    registration_time = models.DateTimeField(db_column='registration')
    cargo = models.ForeignKey(
        'cargo.CargoRecord',
        db_column='cargo_id',
        on_delete=models.PROTECT,
        related_name='+',
    )

    class Meta:
        db_table = 'HandlingEvent'


class RegistrationAttemptRecord(models.Model):
    tracking_id = models.CharField(max_length=255)
    completion_time = models.DateTimeField()
    registration_time = models.DateTimeField()
    event_type = models.CharField(max_length=255)
    un_locode = models.CharField(max_length=5)
    voyage_number = models.CharField(max_length=255, null=True)
    status = models.CharField(
        max_length=10,
        choices=[(status.value, status.value) for status in RegistrationAttemptStatus],
        db_index=True,
    )
    rejection_reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'handling_registration_attempt'
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.CheckConstraint(
                condition=(
                    models.Q(status__in=('accepted', 'registered'), rejection_reason__isnull=True)
                    | (
                        models.Q(status='rejected', rejection_reason__isnull=False)
                        & ~models.Q(rejection_reason='')
                    )
                ),
                name='handling_attempt_rejection_reason_consistent',
            )
        ]
