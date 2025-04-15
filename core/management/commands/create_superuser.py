import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser using environment variables'

    def handle(self, *args, **options):
        # Get the custom user model
        User = get_user_model()

        # Get environment variables
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        # Check if all environment variables are set
        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Environment variables are not set properly'))
            return

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists."))
        else:
            # Create the superuser
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))
