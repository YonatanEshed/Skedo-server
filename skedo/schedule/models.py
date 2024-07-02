from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Schedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError(_('end_time must be after start_time'))

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s schedule: {self.start_time} - {self.end_time}"


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    times_per_week = models.IntegerField()
    duration = models.DurationField()

    def __str__(self):
        return self.name


class GroupActivity(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    start_time = models.TimeField()

    def __str__(self):
        return f"{self.group} starts at {self.start_time}"
