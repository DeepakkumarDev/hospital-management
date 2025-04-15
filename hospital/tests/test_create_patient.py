import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

# Fixture for reusable API client
@pytest.fixture
def api_client():
    return APIClient()

# Fixture to authenticate a user
@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate(**kwargs):
        user = User.objects.create_user(
            username=kwargs.get('username', 'testuser'),
            password=kwargs.get('password', 'testpass123'),
            email=kwargs.get('email', 'test@example.com'),
            role=kwargs.get('role', 'doctor')
        )
        api_client.force_authenticate(user=user)
        return user  # Return the user instance in case we need it
    return do_authenticate

# Actual test for creating a patient
@pytest.mark.django_db
def test_create_patient(api_client, authenticate_user):
    # 1. Authenticate and get the user
    user = authenticate_user(username="doctor1", email="doc1@example.com", password="doctor1pass")

    # 2. Prepare patient data (note: created_by is usually set in the view)
    patient_data = {
        "name": "Alice Smith",
        "age": 30,
        "gender": "F",
        "address": "123 Main Street"
    }

    # 3. Send POST request
    response = api_client.post('/api/patients/', patient_data, format="json")

    # 4. Assertions
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert response.data['name'] == "Alice Smith"
    assert response.data['age'] == 30
    assert response.data['gender'] == "F"

