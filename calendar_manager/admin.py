from django.contrib import admin

from calendar_manager.models import Holiday, LeaveRequest


class HolidayAdminView(admin.ModelAdmin):
    model = Holiday
    list_display = ('name', 'date', 'is_vacation')


class LeaveRequestAdminView(admin.ModelAdmin):
    model = LeaveRequest
    list_display = ('user', 'type', 'from_date', 'to_date', 'reason', 'is_approved')
    readonly_fields = ('rid', 'user', 'type', 'from_date', 'to_date', 'reason')


admin.site.register(Holiday, HolidayAdminView)
admin.site.register(LeaveRequest, LeaveRequestAdminView)
