from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = 'dev@divertise.asia'
        password = settings.SUPER_PASSWORD
        username = 'dev'

        if User.objects.filter(email__iexact=email).exists():
            u = User.objects.get(email=email)
            u.username = username
            u.set_password(password)
            u.is_superuser = True
            u.is_staff = True
            u.is_active = True
            u.save()
            self.stdout.write("The admin account has already existed. Password will be reset.")
        else:
            u = User.objects.create_superuser(username, email, password)
            u.is_active = True
            u.save()
            self.stdout.write("The admin account has been created.")
