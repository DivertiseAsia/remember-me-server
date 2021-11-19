from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from calendar_manager.models import Holiday, LeaveRequest, Event
from calendar_manager.serializers import HolidaySerializer, LeaveRequestSerializer, EventSerializer
from general_manager.generators.tokens import *

account_activation_token = PasswordResetTokenGenerator()


class HolidayViewSet(viewsets.mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = HolidaySerializer
    queryset = Holiday.objects.all()


class LeaveRequestViewSet(viewsets.mixins.CreateModelMixin,
                          viewsets.mixins.ListModelMixin,
                          viewsets.mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LeaveRequestSerializer
    queryset = LeaveRequest.objects.all()
    lookup_field = 'rid'

    def create(self, request, *args, **kwargs):
        """
        Create new leave request.
        ---
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Get own leave requests.
        ---
        """
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Cancel leave request.
        ---
        """
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def all(self, request):
        """
        Get all approved leave requests.
        ---
        """
        queryset = self.get_queryset().filter(status=LeaveRequest.APPROVED)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False,
            url_path=r'^approve/(?P<rid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$')
    def approve(self, request, rid64, token):
        """
        Approve a leave request.
        ---
        """
        rid = force_text(urlsafe_base64_decode(rid64))
        instance = get_object_or_404(self.get_queryset(), rid=rid)
        if LeaveRequestToken.check_token(instance, token):
            instance.status = LeaveRequest.APPROVED
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['POST'], detail=False,
            url_path=r'^reject/(?P<rid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$')
    def reject(self, request, rid64, token):
        """
        Reject a leave request.
        ---
        """
        rid = force_text(urlsafe_base64_decode(rid64))
        instance = get_object_or_404(self.get_queryset(), rid=rid)
        if LeaveRequestToken.check_token(instance, token):
            instance.status = LeaveRequest.REJECTED
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EventViewSet(viewsets.mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    queryset = Event.objects.filter(date__gte=timezone.now().date())
