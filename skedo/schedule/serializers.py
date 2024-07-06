from rest_framework.serializers import ModelSerializer, IntegerField

from .models import Schedule, Group, GroupActivity


class ScheduleSerializer(ModelSerializer):
    id = IntegerField(source='pk', read_only=True)

    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields = [
            "user"
        ]


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = [
            "user"
        ]


class GroupActivitySerializer(ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = GroupActivity
        fields = "__all__"
        read_only_fields = [
            "group",
            "schedule",
        ]
