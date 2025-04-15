import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from hospital.models import Patient, Doctor
from rest_framework import status

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate(**kwargs):
        # Dynamically generate a unique password for each user
        password = kwargs.get('password', 'testpass123')  # Default password if not provided
        user, _ = User.objects.get_or_create(
            username=kwargs.get('username', 'testuser'),
            email=kwargs.get('email', 'test@example.com'),
            role=kwargs.get('role', 'doctor')
        )
        # Set the password for the user (ensures it's not the default password)
        user.set_password(password)
        user.save()

        # Authenticate with the provided password
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate


@pytest.mark.django_db
def test_doctor_can_only_access_own_patient_records(api_client, authenticate_user):
    doctor1_user = authenticate_user(username="doctor1", email="doc1@example.com", password="doctor1pass")
    response = api_client.post('/api/patients/', {
        "name": "Alice Smith",
        "age": 30,
        "gender": "F",
        "address": "123 Main Street"
    }, format="json")
    
    assert response.status_code == 201
    patient_id = response.data["id"]

    doctor2_user = authenticate_user(username="doctor2", email="doc2@example.com", password="doctor2pass")

    response = api_client.get(f"/api/patients/{patient_id}/")
    
    assert True
    assert response.status_code == 404
    
    
@pytest.mark.django_db
def test_restrict_access_to_other_doctor_records(api_client, authenticate_user):
    
    
    doctor1 = authenticate_user(username="doctor1", email="doc1@example.com", password="doctor1pass")
    response = api_client.post('/api/patients/', {
        "name": "John Doe",
        "age": 40,
        "gender": "M",
        "address": "123 Main St"
    }, format='json')
    
    assert response.status_code == 201
    patient_id = response.data['id']

 
    doctor2 = authenticate_user(username="doctor2", email="doc2@example.com")
    response = api_client.get(f'/api/patients/{patient_id}/')

    # Should be forbidden
    assert response.status_code == 404