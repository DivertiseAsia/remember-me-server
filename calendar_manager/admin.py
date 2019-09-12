from django.contrib import admin
from django.http import HttpResponseRedirect

from calendar_manager.models import Holiday, LeaveRequest


class HolidayAdminView(admin.ModelAdmin):
    model = Holiday
    list_display = ('name', 'date', 'is_vacation')


class LeaveRequestAdminView(admin.ModelAdmin):
    model = LeaveRequest
    fields = ('rid', 'user', 'type', 'from_date', 'to_date', 'reason')
    list_display = ('user', 'type', 'from_date', 'to_date', 'reason', 'status')
    readonly_fields = ('rid', 'user', 'type', 'from_date', 'to_date', 'reason')
    list_display_links = ('status',)

    change_form_template = 'approve_reject_buttons.html'

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return False
        super().has_delete_permission(request, obj)

    def change_view(self, request, object_id, extra_context=None, **kwargs):
        if LeaveRequest.objects.get(pk=object_id).status == LeaveRequest.PENDING:
            extra_context = extra_context or {}
            extra_context['pending'] = True
        return super(LeaveRequestAdminView, self).change_view(request, object_id, extra_context=extra_context)

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            obj.approve()
            self.message_user(request, f'[[{obj.rid}] LeaveRequest is approved.')
            return HttpResponseRedirect('/admin/calendar_manager/leaverequest/')

        if "_reject" in request.POST:
            obj.reject()
            self.message_user(request, f'[[{obj.rid}] LeaveRequest is rejected.')
            return HttpResponseRedirect('/admin/calendar_manager/leaverequest/')

        return super().response_change(request, obj)


admin.site.register(Holiday, HolidayAdminView)
admin.site.register(LeaveRequest, LeaveRequestAdminView)
