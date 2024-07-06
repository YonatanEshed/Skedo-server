from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..models import Schedule, Group, GroupActivity

from datetime import time



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

        # raise IndexError(response.data)
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
