import pytest
from rest_framework.test import APIClient
from apps.core.models import Tenant, User


@pytest.fixture
def tenant(db):
    return Tenant.objects.create(
        name='Transportadora Teste',
        slug='teste',
        cnpj='12345678000190',
        plan='professional',
        status='active'
    )


@pytest.fixture
def user(db, tenant):
    return User.objects.create_user(
        username='testuser',
        email='test@logiflow.com',
        password='testpass123',
        tenant=tenant,
        role='operator'
    )


@pytest.fixture
def admin_user(db, tenant):
    return User.objects.create_superuser(
        username='admin',
        email='admin@logiflow.com',
        password='adminpass123',
        tenant=tenant
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client
