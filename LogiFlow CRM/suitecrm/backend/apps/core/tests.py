import pytest
from django.urls import reverse
from .models import Tenant, User


@pytest.mark.django_db
class TestTenantModel:
    def test_create_tenant(self):
        tenant = Tenant.objects.create(
            name='Test Transport',
            slug='test-transport',
            cnpj='98765432000199',
            plan='starter'
        )
        assert tenant.id is not None
        assert tenant.status == 'active'
        assert str(tenant) == 'Test Transport'

    def test_tenant_slug_unique(self, tenant):
        with pytest.raises(Exception):
            Tenant.objects.create(
                name='Another',
                slug='teste',  # same as fixture
                cnpj='11111111000111'
            )


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self, tenant):
        user = User.objects.create_user(
            username='newuser',
            email='new@test.com',
            password='pass123',
            tenant=tenant
        )
        assert user.id is not None
        assert user.tenant == tenant
        assert user.check_password('pass123')

    def test_user_role_default(self, tenant):
        user = User.objects.create_user(
            username='roleuser',
            email='role@test.com',
            password='pass123',
            tenant=tenant
        )
        assert user.role == 'operador'


@pytest.mark.django_db
class TestAuthAPI:
    def test_obtain_token(self, api_client, user):
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_obtain_token_invalid(self, api_client):
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {
            'username': 'invalid',
            'password': 'wrong'
        })
        assert response.status_code == 401

    def test_refresh_token(self, api_client, user):
        # Get tokens
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        refresh_token = response.data['refresh']
        
        # Refresh
        url = reverse('token_refresh')
        response = api_client.post(url, {'refresh': refresh_token})
        assert response.status_code == 200
        assert 'access' in response.data
