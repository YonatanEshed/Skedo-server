from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Schedule, Group, GroupActivity

from datetime import time, timedelta


class ScheduleViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.schedule1 = Schedule.objects.create(user=self.user1, start_time=time(6, 0), end_time=time(22, 0))
        self.schedule2 = Schedule.objects.create(user=self.user2, start_time=time(7, 0), end_time=time(23, 0))

        self.client1 = APIClient()
        self.client2 = APIClient()

        self.client1.login(username='user1', password='password123')
        self.client2.login(username='user2', password='password123')

    def test_get_own_schedule(self):
        response = self.client1.get(reverse("get-put-schedule"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.schedule1.pk)
    
    def test_update_own_schedule(self):
        data = {
            "start_time": "07:00:00",
            "end_time": "23:30:00",
        }
        response = self.client1.put(reverse("get-put-schedule"), data, format='json')
        self.schedule1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.schedule1.pk)
        self.assertEqual(data.get("start_time"), str(self.schedule1.start_time))
        self.assertEqual(data.get("end_time"), str(self.schedule1.end_time))


class GroupViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.group1_1 = Group.objects.create(
            user=self.user1, name="group 1", times_per_week=2, duration=timedelta(hours=1, minutes=0)
            )
        self.group1_2 = Group.objects.create(
            user=self.user1, name="group 2", times_per_week=2, duration=timedelta(hours=0, minutes=45)
            )
        self.group2_1 = Group.objects.create(
            user=self.user2, name="group 1", times_per_week=2, duration=timedelta(hours=1, minutes=15)
            )
        self.group2_2 = Group.objects.create(
            user=self.user2, name="group 2", times_per_week=2, duration=timedelta(hours=0, minutes=30)
            )

        self.client1 = APIClient()
        self.client2 = APIClient()

        self.client1.login(username='user1', password='password123')
        self.client2.login(username='user2', password='password123')

    def test_get_own_groups(self):
        response = self.client1.get(reverse("get-post-group"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get("id"), self.group1_1.pk)
        self.assertEqual(response.data[1].get("id"), self.group1_2.pk)
    
    def test_create_group(self):
        data = {
            "name": "group 3",
            "times_per_week": 4,
            "duration": "01:15:00"
        }
        response = self.client1.post(reverse("get-post-group"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("name"), data.get("name"))
        self.assertEqual(data.get("times_per_week"), data.get("times_per_week"))
        self.assertEqual(data.get("duration"), data.get("duration"))


class GroupDetailViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.group1_1 = Group.objects.create(
            user=self.user1, name="group 1", times_per_week=2, duration=timedelta(hours=1, minutes=0)
            )
        self.group1_2 = Group.objects.create(
            user=self.user1, name="group 2", times_per_week=2, duration=timedelta(hours=0, minutes=45)
            )
        self.group2_1 = Group.objects.create(
            user=self.user2, name="group 1", times_per_week=2, duration=timedelta(hours=1, minutes=15)
            )
        self.group2_2 = Group.objects.create(
            user=self.user2, name="group 2", times_per_week=2, duration=timedelta(hours=0, minutes=30)
            )

        self.client1 = APIClient()
        self.client2 = APIClient()

        self.client1.login(username='user1', password='password123')
        self.client2.login(username='user2', password='password123')

    def test_get_own_group(self):
        response = self.client1.get(reverse("get-put-delete-group", args=[self.group1_1.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.group1_1.pk)
        self.assertEqual(response.data.get("name"), self.group1_1.name)
    
    def test_update_own_group(self):
        data = {
            "name": "group 1",
            "times_per_week": 3,
            "duration": "1:15:00"
        }
        response = self.client1.put(reverse("get-put-delete-group", args=[self.group1_1.pk]), data, format='json')
        self.group1_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.group1_1.pk)
        self.assertEqual(self.group1_1.name, data.get("name"))
        self.assertEqual(self.group1_1.times_per_week, data.get("times_per_week"))
        self.assertEqual(str(self.group1_1.duration), data.get("duration"))

    def test_delete_own_group(self):
        new_group = Group.objects.create(
            user=self.user1, name="group 3", times_per_week=1, duration=timedelta(hours=0, minutes=45)
            )

        response = self.client1.delete(reverse("get-put-delete-group", args=[new_group.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Group.objects.filter(pk=new_group.pk).exists())

    def test_get_other_user_group(self):
        response = self.client2.get(reverse("get-put-delete-group", args=[self.group1_1.pk]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_other_user_group(self):
        data = {
            "name": "group 1",
            "times_per_week": 3,
            "duration": "01:15:00"
        }
        response = self.client2.put(reverse("get-put-delete-group", args=[self.group1_1.pk]), data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_other_user_group(self):
        new_group = Group.objects.create(
            user=self.user2, name="group 3", times_per_week=1, duration=timedelta(hours=0, minutes=45)
            )

        response = self.client1.delete(reverse("get-put-delete-group", args=[new_group.pk]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Group.objects.filter(pk=new_group.pk).exists())
