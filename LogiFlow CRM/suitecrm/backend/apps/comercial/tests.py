import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Cotacao
from apps.clientes.models import Cliente


@pytest.fixture
def cliente(db, tenant):
    return Cliente.objects.create(
        tenant=tenant,
        razao_social='Cliente Cotacao',
        cnpj='99999999000199'
    )


@pytest.fixture
def cotacao(db, tenant, cliente, user):
    return Cotacao.objects.create(
        tenant=tenant,
        cliente=cliente,
        origem_cidade='São Paulo',
        origem_uf='SP',
        destino_cidade='Rio de Janeiro',
        destino_uf='RJ',
        tipo_carga='geral',
        peso_kg=Decimal('1000'),
        valor_frete=Decimal('1500.00'),
        valor_total=Decimal('1500.00'),
        validade=timezone.now().date() + timedelta(days=15),
        criado_por=user
    )


@pytest.mark.django_db
class TestCotacaoModel:
    def test_create_cotacao(self, cotacao):
        assert cotacao.id is not None
        assert cotacao.numero is not None
        assert cotacao.status == 'aberta'

    def test_aprovar_cotacao(self, cotacao):
        cotacao.aprovar()
        assert cotacao.status == 'aprovada'

    def test_perder_cotacao(self, cotacao):
        cotacao.perder('Preço alto')
        assert cotacao.status == 'perdida'
        assert cotacao.motivo_perda == 'Preço alto'

    def test_cotacao_vencida(self, tenant, cliente, user):
        cotacao = Cotacao.objects.create(
            tenant=tenant,
            cliente=cliente,
            origem_cidade='SP',
            origem_uf='SP',
            destino_cidade='RJ',
            destino_uf='RJ',
            tipo_carga='geral',
            peso_kg=Decimal('500'),
            valor_frete=Decimal('800'),
            valor_total=Decimal('800'),
            validade=timezone.now().date() - timedelta(days=1),
            criado_por=user
        )
        assert cotacao.vencida is True

    def test_rota_property(self, cotacao):
        assert cotacao.rota == 'São Paulo/SP → Rio de Janeiro/RJ'


@pytest.mark.django_db
class TestCotacaoAPI:
    def test_list_cotacoes(self, authenticated_client, cotacao):
        url = reverse('cotacao-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data['results']) >= 1

    def test_aprovar_cotacao_api(self, authenticated_client, cotacao):
        url = reverse('cotacao-aprovar', args=[cotacao.id])
        response = authenticated_client.post(url)
        
        assert response.status_code == 200
        cotacao.refresh_from_db()
        assert cotacao.status == 'aprovada'

    def test_perder_cotacao_api(self, authenticated_client, cotacao):
        url = reverse('cotacao-perder', args=[cotacao.id])
        response = authenticated_client.post(url, {'motivo': 'Cliente desistiu'})
        
        assert response.status_code == 200
        cotacao.refresh_from_db()
        assert cotacao.status == 'perdida'

    def test_filter_by_status(self, authenticated_client, cotacao, tenant, cliente, user):
        # Create approved cotacao
        Cotacao.objects.create(
            tenant=tenant, cliente=cliente, origem_cidade='A', origem_uf='SP',
            destino_cidade='B', destino_uf='RJ', tipo_carga='geral',
            peso_kg=Decimal('100'), valor_frete=Decimal('500'), valor_total=Decimal('500'),
            validade=timezone.now().date() + timedelta(days=10), criado_por=user, status='aprovada'
        )
        
        url = reverse('cotacao-list')
        response = authenticated_client.get(url, {'status': 'aberta'})
        
        assert response.status_code == 200
        for item in response.data['results']:
            assert item['status'] == 'aberta'
