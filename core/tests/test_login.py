import pytest
from rest_framework import status

@pytest.mark.django_db
class TestUserLogin:
    def test_login_with_valid_credentials(self, api_client, create_test_user):
        # Arrange
        user = create_test_user(username='testuser', password='testpass123')

        # Act
        response = api_client.post('/api/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data
        assert response.data['user']['username'] == 'testuser'
        assert response.data['msg'] == 'Login successful'

    def test_login_with_invalid_credentials(self, api_client, create_test_user):
        # Arrange
        create_test_user(username='testuser', password='correctpass')

        # Act
        response = api_client.post('/api/login/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data or 'username' in response.data or 'password' in response.data
