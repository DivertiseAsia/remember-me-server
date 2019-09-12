from rest_framework import serializers

from calendar_manager.models import Holiday, LeaveRequest
from user_manager.serializers import UserSerializer


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('name', 'date', 'is_vacation')


class LeaveRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = ('rid', 'user', 'type', 'from_date', 'to_date', 'reason', 'status')
