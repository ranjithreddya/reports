from django.db import models
from django.utils import timezone

class JsonLoad(models.Model):
    json_id = models.BigIntegerField(primary_key=True)  # Use BigIntegerField for large numbers
    status_cd = models.CharField(max_length=16777216, default='INPR')  # Status code
    file_nm = models.CharField(max_length=16777216)  # File name
    json_val = models.JSONField()  # JSON value
    crt_dm = models.DateTimeField(default=timezone.now)  # Creation timestamp

    class Meta:
        db_table = 'json_load'  # Define the table name in the database
        ordering = ['crt_dm']  # Optional: Specify default ordering

    def save(self, *args, **kwargs):
        if self.json_id is None:  # Only set if json_id is not provided
            last_id = JsonLoad.objects.aggregate(models.Max('json_id'))['json_id__max']
            self.json_id = last_id + 1 if last_id is not None else 100000000000
        super().save(*args, **kwargs)
