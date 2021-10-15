from django.contrib import admin
from django.contrib.auth.models import Group

from user_manager.models import Profile


class ProfileAdminView(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'birth_date')


admin.site.register(Profile, ProfileAdminView)

admin.site.unregister(Group)

admin.site.site_header = 'RememberME Administration'
