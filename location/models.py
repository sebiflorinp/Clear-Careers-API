from django.db import models
from authentication.models import Employer


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    street_number = models.IntegerField(default=1)
    is_hq = models.BooleanField(default=False)
