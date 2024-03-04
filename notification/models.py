from django.db import models

from authentication.models import User
from django.utils import timezone


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)



