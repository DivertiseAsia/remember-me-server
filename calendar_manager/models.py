import datetime
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from general_manager.helpers import EmailHelper


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
    REJECTED = 0
    APPROVED = 1
    PENDING = 2
    REQUEST_STATUS = (
        (REJECTED, "Rejected"),
        (APPROVED, "Approved"),
        (PENDING, "Pending"),
    )
    rid = models.UUIDField('Request ID', default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField('Leave type', choices=LEAVE_TYPE, default=PERSONAL)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField('Request status', choices=REQUEST_STATUS, default=PENDING)

    def approve(self):
        self.status = self.APPROVED
        self.save()

    def reject(self):
        self.status = self.REJECTED
        self.save()


@receiver(pre_save, sender=LeaveRequest)
def auto_approve_on_sick_type(sender, instance, *args, **kwargs):
    if instance.type == LeaveRequest.SICK and instance.from_date < (timezone.now() + datetime.timedelta(days=2)).date():
        instance.status = LeaveRequest.APPROVED


@receiver(post_save, sender=LeaveRequest)
def send_email_on_new_pending(sender, instance, created, *args, **kwargs):
    if created and instance.status == LeaveRequest.PENDING:
        EmailHelper(
            subject='New Leave Request',
            template_file='new_leave_request_email.html',
            ctx={'origin': settings.ORIGIN_URL, 'protocol': settings.ORIGIN_PROTOCOL}
        ).send()


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    all_day = models.BooleanField(default=False)
    start = models.TimeField('Start time', default=datetime.time(10, 00))
    end = models.TimeField('End time', default=datetime.time(18, 00))
    place = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
