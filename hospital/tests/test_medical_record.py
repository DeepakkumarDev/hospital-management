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
def test_doctor_can_only_add_medical_record_to_own_patient(api_client, authenticate_user):
    # Authenticate doctor1 with a unique password
    doctor1_user = authenticate_user(username="doctor1", email="doc1@example.com", password="doctor1pass")
    response = api_client.post('/api/patients/', {
        "name": "Alice Smith",
        "age": 30,
        "gender": "F",
        "address": "123 Main Street"
    }, format="json")
    
    assert response.status_code == 201
    patient_id = response.data['id']

    # Now authenticate doctor2 with a unique password
    doctor2_user = authenticate_user(username="doctor2", email="doc2@example.com", password="doctor2pass")

    # doctor2 attempts to add a medical record to doctor1's patient
    medical_record_data = {
        "patient_id": patient_id,
        "diagnosis": "Cold",
        "treatment": "Rest and fluids",
        "notes": "Should recover in 3 days"
    }

    response = api_client.post('/api/patients/records/add/', medical_record_data, format="json")

    # Assert that doctor2 can't add medical record to doctor1's patient
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "patient not found" in str(response.data['patient_id'][0]).lower()



# import pytest
# from rest_framework.test import APIClient
# from django.contrib.auth import get_user_model
# from hospital.models import Patient, Doctor
# from rest_framework import status

# User = get_user_model()

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def authenticate_user(api_client):
#     def do_authenticate(**kwargs):
#         user,_ = User.objects.get_or_create(
#             username=kwargs.get('username', 'testuser'),
#             password=kwargs.get('password', 'testpass123'),
#             email=kwargs.get('email', 'test@example.com'),
#             role=kwargs.get('role', 'doctor')
#         )
#         api_client.force_authenticate(user=user)
#         return user
#     return do_authenticate

# @pytest.mark.django_db
# def test_doctor_can_only_add_medical_record_to_own_patient(api_client, authenticate_user):
#     # Authenticate doctor1 and create a patient
#     doctor1_user = authenticate_user(username="doctor1", email="doc1@example.com")
#     response = api_client.post('/api/patients/', {
#         "name": "Alice Smith",
#         "age": 30,
#         "gender": "F",
#         "address": "123 Main Street"
#     }, format="json")
    
#     assert response.status_code == 201
#     patient_id = response.data['id']
#     # api_client.logout()

#     # Now authenticate doctor2 (new session)
#     doctor2_user = authenticate_user(username="doctor2", email="doc2@example.com")

#     # doctor2 attempts to add a medical record to doctor1's patient
#     medical_record_data = {
#         "patient_id": patient_id,
#         "diagnosis": "Cold",
#         "treatment": "Rest and fluids",
#         "notes": "Should recover in 3 days"
#     }

#     response = api_client.post('/api/patients/records/add/', medical_record_data, format="json")

#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#     assert "patient not found" in str(response.data['patient_id'][0]).lower()
