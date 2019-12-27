from rest_framework import serializers

from calendar_manager.models import Holiday, LeaveRequest, Event


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


class EventSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    @staticmethod
    def get_details(obj):
        time = 'All day' if obj.all_day else f'{obj.start.strftime("%H:%M")}–{obj.end.strftime("%H:%M")}'
        place = f'\n@{obj.place}' if obj.place else ''
        note = f'\nNotes: {obj.note}' if obj.note else ''
        return f'{time}{place}{note}'

    class Meta:
        model = Event
        fields = ('name', 'date', 'details')
