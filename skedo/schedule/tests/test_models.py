from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ..models import Schedule, Group, GroupActivity

from datetime import time, timedelta


class ScheduleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser"
        )
    
    def test_schedule_creation(self):
        schedule = Schedule.objects.create(
            user=self.user, start_time=time(2,30), end_time=time(3,0)
        )
        self.assertTrue(
                isinstance(schedule, Schedule)
            )
        self.assertEqual(
                str(schedule), 
                f"{self.user.username}'s schedule: 02:30:00 - 03:00:00"
            )
    
    def test_end_time_before_start_time(self):
        schedule = Schedule(
            user=self.user, start_time=time(3,30), end_time=time(3,0)
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_start_time_equal_end_time(self):
        schedule = Schedule(
            user=self.user, start_time=time(3,0), end_time=time(3,0)
        )
        with self.assertRaises(ValidationError):
            schedule.full_clean()


class GroupTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser"
        )
        self.group = Group.objects.create(
            user=self.user, 
            name="group1", 
            times_per_week=3, 
            duration=timedelta(hours=0, minutes=30)
        )
    
    def test_group_creation(self):
        self.assertTrue(
                isinstance(self.group, Group)
            )
        self.assertEqual(str(self.group), "group1")


class GroupActivityTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser"
        )

        self.group = Group.objects.create(
            user=self.user, 
            name="group1", 
            times_per_week=3, 
            duration=timedelta(hours=0, minutes=30)
        )

        self.schedule = Schedule.objects.create(
            user=self.user, start_time=time(2,30), end_time=time(3,0)
        )

        self.group_activity = GroupActivity.objects.create(
            group=self.group, schedule=self.schedule, start_time=time(2,30)
        )
    
    def test_group_creation(self):
        self.assertTrue(
                isinstance(self.group_activity, GroupActivity)
            )
        self.assertEqual(str(self.group_activity), f"group1 starts at 02:30:00")
