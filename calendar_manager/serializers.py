from rest_framework import serializers

from calendar_manager.models import Holiday, LeaveRequest


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('name', 'date', 'is_vacation')


class LeaveRequestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        return obj.user.first_name

    class Meta:
        model = LeaveRequest
        fields = ('rid', 'user', 'type', 'from_date', 'to_date', 'reason', 'status')
        extra_kwargs = {'status': {'read_only': True}}
