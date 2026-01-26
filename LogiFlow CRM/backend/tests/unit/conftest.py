"""
Fixtures compartilhadas para testes unitários
"""
import pytest
from decimal import Decimal
from uuid import uuid4

from domain.value_objects.endereco import Endereco
from domain.value_objects.documento import CNPJ, CPF


@pytest.fixture
def endereco_sp():
    """Fixture: Endereço em São Paulo"""
    return Endereco(
        logradouro="Av. Paulista",
        numero="1000",
        bairro="Bela Vista",
        cidade="São Paulo",
        uf="SP",
        cep="01310100"
    )


@pytest.fixture
def endereco_rj():
    """Fixture: Endereço no Rio de Janeiro"""
    return Endereco(
        logradouro="Av. Rio Branco",
        numero="500",
        bairro="Centro",
        cidade="Rio de Janeiro",
        uf="RJ",
        cep="20040002"
    )


@pytest.fixture
def cnpj_valido():
    """Fixture: CNPJ válido"""
    return CNPJ("11222333000181")


@pytest.fixture
def cpf_valido():
    """Fixture: CPF válido"""
    return CPF("52998224725")


@pytest.fixture
def cliente_id():
    """Fixture: UUID de cliente"""
    return uuid4()
