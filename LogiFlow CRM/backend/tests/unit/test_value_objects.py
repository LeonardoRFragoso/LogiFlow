"""
Testes unitários para Value Objects
====================================
Testa validação e comportamento dos Value Objects.
"""
import pytest

from domain.value_objects.endereco import Endereco
from domain.value_objects.documento import CNPJ, CPF


class TestEndereco:
    """Testes para Value Object Endereco"""
    
    def test_criar_endereco_valido(self):
        """Deve criar endereço com dados válidos"""
        endereco = Endereco(
            logradouro="Rua das Flores",
            numero="123",
            bairro="Centro",
            cidade="São Paulo",
            uf="SP",
            cep="01234567"
        )
        
        assert endereco.logradouro == "Rua das Flores"
        assert endereco.uf == "SP"
    
    def test_endereco_com_complemento(self):
        """Deve criar endereço com complemento"""
        endereco = Endereco(
            logradouro="Av. Principal",
            numero="456",
            bairro="Industrial",
            cidade="Campinas",
            uf="SP",
            cep="13000000",
            complemento="Sala 10"
        )
        
        assert endereco.complemento == "Sala 10"
    
    def test_cep_formatado(self):
        """Deve formatar CEP corretamente"""
        endereco = Endereco(
            logradouro="Rua Teste",
            numero="1",
            bairro="Centro",
            cidade="SP",
            uf="SP",
            cep="01234567"
        )
        
        assert endereco.cep_formatado == "01234-567"
    
    def test_endereco_completo(self):
        """Deve retornar endereço formatado"""
        endereco = Endereco(
            logradouro="Rua Teste",
            numero="100",
            bairro="Centro",
            cidade="São Paulo",
            uf="SP",
            cep="01234567"
        )
        
        completo = endereco.endereco_completo
        assert "Rua Teste" in completo
        assert "São Paulo" in completo
    
    def test_endereco_sem_logradouro_deve_falhar(self):
        """Deve falhar sem logradouro"""
        with pytest.raises(ValueError, match="Logradouro é obrigatório"):
            Endereco(
                logradouro="",
                numero="1",
                bairro="Centro",
                cidade="SP",
                uf="SP",
                cep="01234567"
            )
    
    def test_endereco_uf_invalida_deve_falhar(self):
        """Deve falhar com UF inválida"""
        with pytest.raises(ValueError, match="UF deve ter 2 caracteres"):
            Endereco(
                logradouro="Rua Teste",
                numero="1",
                bairro="Centro",
                cidade="SP",
                uf="São Paulo",  # UF inválida
                cep="01234567"
            )
    
    def test_endereco_imutavel(self):
        """Endereço deve ser imutável (frozen dataclass)"""
        endereco = Endereco(
            logradouro="Rua Teste",
            numero="1",
            bairro="Centro",
            cidade="SP",
            uf="SP",
            cep="01234567"
        )
        
        with pytest.raises(AttributeError):
            endereco.logradouro = "Nova Rua"


class TestCNPJ:
    """Testes para Value Object CNPJ"""
    
    def test_cnpj_valido(self):
        """Deve criar CNPJ válido"""
        cnpj = CNPJ("11222333000181")
        assert cnpj.valor == "11222333000181"
    
    def test_cnpj_formatado(self):
        """Deve formatar CNPJ corretamente"""
        cnpj = CNPJ("11222333000181")
        assert cnpj.formatado == "11.222.333/0001-81"
    
    def test_cnpj_com_mascara(self):
        """Deve aceitar CNPJ com máscara"""
        cnpj = CNPJ("11.222.333/0001-81")
        assert cnpj.valor == "11222333000181"
    
    def test_cnpj_tamanho_invalido(self):
        """Deve rejeitar CNPJ com tamanho inválido"""
        with pytest.raises(ValueError, match="deve ter 14 dígitos"):
            CNPJ("123456")
    
    def test_cnpj_digitos_invalidos(self):
        """Deve rejeitar CNPJ com dígitos verificadores inválidos"""
        with pytest.raises(ValueError, match="dígitos verificadores incorretos"):
            CNPJ("11222333000199")  # DV incorreto
    
    def test_cnpj_todos_digitos_iguais(self):
        """Deve rejeitar CNPJ com todos dígitos iguais"""
        with pytest.raises(ValueError):
            CNPJ("11111111111111")


class TestCPF:
    """Testes para Value Object CPF"""
    
    def test_cpf_valido(self):
        """Deve criar CPF válido"""
        cpf = CPF("52998224725")
        assert cpf.valor == "52998224725"
    
    def test_cpf_formatado(self):
        """Deve formatar CPF corretamente"""
        cpf = CPF("52998224725")
        assert cpf.formatado == "529.982.247-25"
    
    def test_cpf_com_mascara(self):
        """Deve aceitar CPF com máscara"""
        cpf = CPF("529.982.247-25")
        assert cpf.valor == "52998224725"
    
    def test_cpf_tamanho_invalido(self):
        """Deve rejeitar CPF com tamanho inválido"""
        with pytest.raises(ValueError, match="deve ter 11 dígitos"):
            CPF("123456")
    
    def test_cpf_digitos_invalidos(self):
        """Deve rejeitar CPF com dígitos verificadores inválidos"""
        with pytest.raises(ValueError, match="dígitos verificadores incorretos"):
            CPF("52998224799")  # DV incorreto
    
    def test_cpf_todos_digitos_iguais(self):
        """Deve rejeitar CPF com todos dígitos iguais"""
        with pytest.raises(ValueError):
            CPF("11111111111")
