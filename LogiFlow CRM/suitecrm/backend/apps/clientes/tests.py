import pytest
from django.urls import reverse
from .models import Cliente


@pytest.mark.django_db
class TestClienteModel:
    def test_create_cliente(self, tenant):
        cliente = Cliente.objects.create(
            tenant=tenant,
            razao_social='Empresa Teste LTDA',
            cnpj='12345678000190',
            cidade='São Paulo',
            uf='SP'
        )
        assert cliente.id is not None
        assert cliente.ativo is True
        assert str(cliente) == 'Empresa Teste LTDA'

    def test_cliente_nome_display(self, tenant):
        cliente = Cliente.objects.create(
            tenant=tenant,
            razao_social='Razao Social',
            nome_fantasia='Nome Fantasia',
            cnpj='11111111000111'
        )
        assert cliente.nome_display == 'Nome Fantasia'

        cliente2 = Cliente.objects.create(
            tenant=tenant,
            razao_social='Apenas Razao',
            cnpj='22222222000122'
        )
        assert cliente2.nome_display == 'Apenas Razao'


@pytest.mark.django_db
class TestClienteAPI:
    def test_list_clientes(self, authenticated_client, tenant):
        Cliente.objects.create(tenant=tenant, razao_social='Cliente 1', cnpj='11111111000111')
        Cliente.objects.create(tenant=tenant, razao_social='Cliente 2', cnpj='22222222000122')
        
        url = reverse('cliente-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data['results']) == 2

    def test_create_cliente(self, authenticated_client, tenant):
        url = reverse('cliente-list')
        data = {
            'razao_social': 'Novo Cliente',
            'cnpj': '33333333000133',
            'cidade': 'Rio de Janeiro',
            'uf': 'RJ'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == 201
        assert Cliente.objects.filter(cnpj='33333333000133').exists()

    def test_search_clientes(self, authenticated_client, tenant):
        Cliente.objects.create(tenant=tenant, razao_social='ABC Transportes', cnpj='11111111000111')
        Cliente.objects.create(tenant=tenant, razao_social='XYZ Logistica', cnpj='22222222000122')
        
        url = reverse('cliente-list')
        response = authenticated_client.get(url, {'search': 'ABC'})
        
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['razao_social'] == 'ABC Transportes'

    def test_unauthorized_access(self, api_client):
        url = reverse('cliente-list')
        response = api_client.get(url)
        assert response.status_code == 401
