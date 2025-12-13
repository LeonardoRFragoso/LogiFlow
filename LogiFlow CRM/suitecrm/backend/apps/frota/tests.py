import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Motorista, Veiculo


@pytest.mark.django_db
class TestMotoristaModel:
    def test_create_motorista(self, tenant):
        motorista = Motorista.objects.create(
            tenant=tenant,
            nome='João Silva',
            cpf='12345678901',
            cnh_numero='12345678900',
            cnh_categoria='E',
            cnh_validade=timezone.now().date() + timedelta(days=365)
        )
        assert motorista.id is not None
        assert str(motorista) == 'João Silva'

    def test_cnh_vencida(self, tenant):
        motorista = Motorista.objects.create(
            tenant=tenant,
            nome='CNH Vencida',
            cpf='11111111111',
            cnh_numero='11111111100',
            cnh_categoria='D',
            cnh_validade=timezone.now().date() - timedelta(days=10)
        )
        assert motorista.cnh_vencida is True
        assert motorista.cnh_vencendo is False

    def test_cnh_vencendo(self, tenant):
        motorista = Motorista.objects.create(
            tenant=tenant,
            nome='CNH Vencendo',
            cpf='22222222222',
            cnh_numero='22222222200',
            cnh_categoria='C',
            cnh_validade=timezone.now().date() + timedelta(days=20)
        )
        assert motorista.cnh_vencida is False
        assert motorista.cnh_vencendo is True
        assert motorista.dias_para_vencer_cnh == 20


@pytest.mark.django_db
class TestVeiculoModel:
    def test_create_veiculo(self, tenant):
        veiculo = Veiculo.objects.create(
            tenant=tenant,
            placa='ABC1D23',
            tipo='truck',
            marca='Volvo',
            modelo='FH 540'
        )
        assert veiculo.id is not None
        assert str(veiculo) == 'ABC1D23 - Volvo FH 540'

    def test_veiculo_status_default(self, tenant):
        veiculo = Veiculo.objects.create(
            tenant=tenant,
            placa='XYZ9K87',
            tipo='carreta'
        )
        assert veiculo.status == 'disponivel'


@pytest.mark.django_db
class TestMotoristaAPI:
    def test_list_motoristas(self, authenticated_client, tenant):
        Motorista.objects.create(
            tenant=tenant, nome='Motorista 1', cpf='11111111111',
            cnh_numero='11111111100', cnh_categoria='E',
            cnh_validade=timezone.now().date() + timedelta(days=365)
        )
        
        url = reverse('motorista-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data['results']) >= 1

    def test_filter_cnh_vencendo(self, authenticated_client, tenant):
        # CNH válida
        Motorista.objects.create(
            tenant=tenant, nome='CNH OK', cpf='11111111111',
            cnh_numero='11111111100', cnh_categoria='E',
            cnh_validade=timezone.now().date() + timedelta(days=365)
        )
        # CNH vencendo
        Motorista.objects.create(
            tenant=tenant, nome='CNH Vencendo', cpf='22222222222',
            cnh_numero='22222222200', cnh_categoria='D',
            cnh_validade=timezone.now().date() + timedelta(days=15)
        )
        
        url = reverse('motorista-list')
        response = authenticated_client.get(url, {'cnh_vencendo': 'true'})
        
        assert response.status_code == 200


@pytest.mark.django_db
class TestVeiculoAPI:
    def test_list_veiculos(self, authenticated_client, tenant):
        Veiculo.objects.create(tenant=tenant, placa='AAA1111', tipo='toco')
        
        url = reverse('veiculo-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data['results']) >= 1

    def test_filter_by_status(self, authenticated_client, tenant):
        Veiculo.objects.create(tenant=tenant, placa='BBB2222', tipo='truck', status='disponivel')
        Veiculo.objects.create(tenant=tenant, placa='CCC3333', tipo='van', status='em_viagem')
        
        url = reverse('veiculo-list')
        response = authenticated_client.get(url, {'status': 'disponivel'})
        
        assert response.status_code == 200
        for item in response.data['results']:
            assert item['status'] == 'disponivel'
