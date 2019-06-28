import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Holiday(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    is_vacation = models.BooleanField(default=True)


class LeaveRequest(models.Model):
    PERSONAL = 0
    SICK = 1
    LEAVE_TYPE = (
        (PERSONAL, "Personal"),
        (SICK, "Sick"),
    )
    rid = models.UUIDField('Request ID', default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField('Leave Type', choices=LEAVE_TYPE, default=PERSONAL)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)


@receiver(pre_save, sender=LeaveRequest)
def auto_approve_on_sick_type(sender, instance, true=True, **kwargs):
    if instance.type == LeaveRequest.SICK:
        instance.is_approved = true
