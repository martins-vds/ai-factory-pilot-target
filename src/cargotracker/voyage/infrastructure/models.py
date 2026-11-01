from django.db import models


class VoyageRecord(models.Model):
    voyage_number = models.CharField(max_length=255, db_column='voyage_number')

    class Meta:
        db_table = 'voyage'
