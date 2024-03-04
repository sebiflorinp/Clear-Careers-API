from django.db import models
from authentication.models import Employee


class Education(models.Model):
    education_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100, null=False, blank=False)
    field = models.CharField(max_length=100, null=False, blank=True)
    degree = models.CharField(max_length=100, null=False, blank=False)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
