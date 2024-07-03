from rest_framework.serializers import Serializer

from models import Schedule, Group, GroupActivity


class ScheduleSerializer(Serializer):
    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields = (
            "user"
        )


class GroupSerializer(Serializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = (
            "user"
        )


class GroupActivitySerializer(Serializer):
    group = GroupSerializer()

    class Meta:
        model = GroupActivity
        fields = "__all__"
        read_only_fields = (
            "group",
            "schedule",
        )
