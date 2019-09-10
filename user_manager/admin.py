from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from user_manager.models import Profile


class ProfileAdminView(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'birth_date')


admin.site.register(Profile, ProfileAdminView)

admin.site.unregister(Token)
admin.site.unregister(Group)

admin.site.site_header = 'RememberME Administration'
