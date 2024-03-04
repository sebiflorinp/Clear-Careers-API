from django.db import models
from authentication.models import Employer, Employee
from posting.models import Posting
from django.utils import timezone


class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    posting_id = models.ForeignKey(Posting, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
