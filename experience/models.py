from django.db import models
from authentication.models import Employee


class Experience(models.Model):
    experience_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

