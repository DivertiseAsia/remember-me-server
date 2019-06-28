from django.contrib import admin

from user_manager.models import Profile


class ProfileAdminView(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'birth_date')


admin.site.register(Profile, ProfileAdminView)

admin.site.site_header = 'RememberME Administration'
