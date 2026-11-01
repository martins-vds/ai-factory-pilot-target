from django.db import models


class LocationRecord(models.Model):
    unlocode = models.CharField(max_length=255, db_column='unlocode')
    name = models.CharField(max_length=255, db_column='name')

    class Meta:
        db_table = 'location'
