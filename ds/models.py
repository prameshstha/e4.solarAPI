from datetime import datetime
from django.db import models


# Create your models here.

class DCHubDetails(models.Model):
    dc_48_current1 = models.FloatField()
    dc_48_current2 = models.FloatField()
    dc_48_current3 = models.FloatField()
    dc_48_current4 = models.FloatField()
    dc_48_current5 = models.FloatField()
    dc_48_voltage1 = models.FloatField()
    dc_48_voltage2 = models.FloatField()
    pv1_voltage = models.FloatField()
    pv1_current = models.FloatField()
    bms_voltage = models.FloatField()
    bms_current = models.FloatField()
    battery_capacity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'System data at ' + str(self.created_at)
