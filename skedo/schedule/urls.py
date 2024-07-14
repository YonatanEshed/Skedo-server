from django.urls import path

from .views import ScheduleView, GroupView, GroupDetailView

urlpatterns = [
    path("schedule/", ScheduleView.as_view(), name="get-put-schedule"),
    path("group/", GroupView.as_view(), name="get-post-group"),
    path("group/<int:pk>", GroupDetailView.as_view(), name="get-put-delete-group"),
]