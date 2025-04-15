import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings.dev')

django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_test_user():
    def make_user(**kwargs):
        return User.objects.create_user(
            username=kwargs.get('username', 'testuser'),
            password=kwargs.get('password', 'testpass123'),
            email=kwargs.get('email', 'test@example.com'),
            role=kwargs.get('role', 'doctor')
        )
    return make_user
