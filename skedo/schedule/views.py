from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import ScheduleSerializer, GroupSerializer
from .models import Schedule, Group


class ScheduleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            schedule = Schedule.objects.get(user=request.user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        try:
            schedule = Schedule.objects.get(user=request.user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ScheduleSerializer(schedule, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Group.objects.all()
        queryset = queryset.filter(user=request.user)
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


class GroupDetailView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_group(self, user, pk):
        try:
            group = Group.objects.get(pk=pk, user=user)
        except:
            return None
        
        return group

    def get(self, request, pk):
        group = self.get_group(request.user, pk)
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        group = self.get_group(request.user, pk)
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_group(request.user, pk)
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        group.delete()
        return Response(status=status.HTTP_200_OK)
