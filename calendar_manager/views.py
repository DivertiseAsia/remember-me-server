from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from calendar_manager.models import Holiday, LeaveRequest
from calendar_manager.serializers import HolidaySerializer, LeaveRequestSerializer

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

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny(), ]
        return super(LeaveRequestViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create new leave request.
        ---
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            req = LeaveRequest(user=request.user, **serializer.data)
            req.save()
            return Response(self.get_serializer(req).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Cancel leave request.
        ---
        """
        instance = self.get_object()
        if instance.user is not request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
