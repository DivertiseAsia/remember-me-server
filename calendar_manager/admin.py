from django.contrib import admin

from calendar_manager.models import Holiday, LeaveRequest


class HolidayAdminView(admin.ModelAdmin):
    model = Holiday
    list_display = ('name', 'date', 'is_vacation')


class LeaveRequestAdminView(admin.ModelAdmin):
    model = LeaveRequest
    list_display = ('user', 'type', 'from_date', 'to_date', 'reason', 'status')
    readonly_fields = ('rid', 'user', 'type', 'from_date', 'to_date', 'reason')

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return False
        super().has_delete_permission(request, obj)


admin.site.register(Holiday, HolidayAdminView)
admin.site.register(LeaveRequest, LeaveRequestAdminView)
