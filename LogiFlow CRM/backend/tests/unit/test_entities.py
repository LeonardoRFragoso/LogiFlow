"""
Testes unitários para Entidades de Domínio
==========================================
Testa regras de negócio encapsuladas nas entidades.
"""
import pytest
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from domain.entities.cliente import Cliente
from domain.entities.cotacao import Cotacao, ItemCotacao, StatusCotacao, TipoFrete, TipoCarga
from domain.entities.pedido import Pedido, StatusPedido
from domain.value_objects.endereco import Endereco
from domain.value_objects.documento import CNPJ, CPF


class TestCliente:
    """Testes para entidade Cliente"""
    
    def test_criar_cliente_valido(self):
        """Deve criar cliente com dados válidos"""
        cliente = Cliente(
            razao_social="Empresa Teste Ltda",
            nome_fantasia="Teste",
            documento=CNPJ("11222333000181"),
            email="teste@empresa.com",
        )
        
        assert cliente.razao_social == "Empresa Teste Ltda"
        assert cliente.ativo is True
        assert cliente.id is not None
    
    def test_cliente_sem_razao_social_deve_falhar(self):
        """Deve falhar ao criar cliente sem razão social"""
        with pytest.raises(ValueError, match="Razão social é obrigatória"):
            Cliente(razao_social="", documento=CNPJ("11222333000181"))
    
    def test_ativar_cliente(self):
        """Deve ativar cliente desativado"""
        cliente = Cliente(razao_social="Teste", ativo=False)
        cliente.ativar()
        assert cliente.ativo is True
    
    def test_desativar_cliente(self):
        """Deve desativar cliente ativo"""
        cliente = Cliente(razao_social="Teste", ativo=True)
        cliente.desativar()
        assert cliente.ativo is False


class TestCotacao:
    """Testes para entidade Cotação"""
    
    @pytest.fixture
    def endereco_origem(self):
        return Endereco(
            logradouro="Rua Teste",
            numero="100",
            bairro="Centro",
            cidade="São Paulo",
            uf="SP",
            cep="01000000"
        )
    
    @pytest.fixture
    def endereco_destino(self):
        return Endereco(
            logradouro="Av. Principal",
            numero="500",
            bairro="Industrial",
            cidade="Campinas",
            uf="SP",
            cep="13000000"
        )
    
    @pytest.fixture
    def item_cotacao(self):
        return ItemCotacao(
            descricao="Carga Geral",
            quantidade=10,
            peso_kg=Decimal("100.5"),
            volume_m3=Decimal("2.0")
        )
    
    def test_criar_cotacao_valida(self, endereco_origem, endereco_destino, item_cotacao):
        """Deve criar cotação com dados válidos"""
        cotacao = Cotacao(
            cliente_id=uuid4(),
            origem=endereco_origem,
            destino=endereco_destino,
            itens=[item_cotacao],
            valor_frete=Decimal("500.00")
        )
        
        assert cotacao.status == StatusCotacao.RASCUNHO
        assert cotacao.valor_total == Decimal("500.00")
        assert cotacao.peso_total == Decimal("1005.0")  # 10 * 100.5
    
    def test_cotacao_sem_itens_deve_falhar(self, endereco_origem, endereco_destino):
        """Deve falhar ao criar cotação sem itens"""
        with pytest.raises(ValueError, match="deve ter pelo menos um item"):
            Cotacao(
                cliente_id=uuid4(),
                origem=endereco_origem,
                destino=endereco_destino,
                itens=[]
            )
    
    def test_enviar_cotacao(self, endereco_origem, endereco_destino, item_cotacao):
        """Deve enviar cotação em rascunho"""
        cotacao = Cotacao(
            cliente_id=uuid4(),
            origem=endereco_origem,
            destino=endereco_destino,
            itens=[item_cotacao]
        )
        
        cotacao.enviar()
        assert cotacao.status == StatusCotacao.ENVIADA
    
    def test_aprovar_cotacao_enviada(self, endereco_origem, endereco_destino, item_cotacao):
        """Deve aprovar cotação enviada"""
        cotacao = Cotacao(
            cliente_id=uuid4(),
            origem=endereco_origem,
            destino=endereco_destino,
            itens=[item_cotacao]
        )
        
        cotacao.enviar()
        cotacao.aprovar()
        assert cotacao.status == StatusCotacao.APROVADA
    
    def test_nao_pode_aprovar_cotacao_em_rascunho(self, endereco_origem, endereco_destino, item_cotacao):
        """Não deve aprovar cotação em rascunho"""
        cotacao = Cotacao(
            cliente_id=uuid4(),
            origem=endereco_origem,
            destino=endereco_destino,
            itens=[item_cotacao]
        )
        
        with pytest.raises(ValueError):
            cotacao.aprovar()
    
    def test_cotacao_expirada(self, endereco_origem, endereco_destino, item_cotacao):
        """Deve identificar cotação expirada"""
        cotacao = Cotacao(
            cliente_id=uuid4(),
            origem=endereco_origem,
            destino=endereco_destino,
            itens=[item_cotacao],
            validade=date(2020, 1, 1)  # Data passada
        )
        
        assert cotacao.esta_expirada() is True


class TestPedido:
    """Testes para entidade Pedido"""
    
    @pytest.fixture
    def endereco(self):
        return Endereco(
            logradouro="Rua Teste",
            numero="100",
            bairro="Centro",
            cidade="São Paulo",
            uf="SP",
            cep="01000000"
        )
    
    def test_criar_pedido_valido(self, endereco):
        """Deve criar pedido com dados válidos"""
        pedido = Pedido(
            cliente_id=uuid4(),
            cotacao_id=uuid4(),
            origem=endereco,
            destino=endereco,
            valor_frete=Decimal("500.00")
        )
        
        assert pedido.status == StatusPedido.AGUARDANDO_COLETA
    
    def test_coletar_pedido(self, endereco):
        """Deve registrar coleta do pedido"""
        pedido = Pedido(
            cliente_id=uuid4(),
            cotacao_id=None,
            origem=endereco,
            destino=endereco
        )
        
        pedido.coletar()
        
        assert pedido.status == StatusPedido.COLETADO
        assert pedido.data_coleta_realizada is not None
    
    def test_fluxo_completo_entrega(self, endereco):
        """Deve completar fluxo de entrega"""
        pedido = Pedido(
            cliente_id=uuid4(),
            cotacao_id=None,
            origem=endereco,
            destino=endereco
        )
        
        # Fluxo: Aguardando -> Coletado -> Em Trânsito -> Saiu Entrega -> Entregue
        pedido.coletar()
        assert pedido.status == StatusPedido.COLETADO
        
        pedido.iniciar_transporte()
        assert pedido.status == StatusPedido.EM_TRANSITO
        
        pedido.sair_para_entrega()
        assert pedido.status == StatusPedido.SAIU_PARA_ENTREGA
        
        pedido.entregar()
        assert pedido.status == StatusPedido.ENTREGUE
        assert pedido.data_entrega_realizada is not None
    
    def test_cancelar_pedido(self, endereco):
        """Deve cancelar pedido com motivo"""
        pedido = Pedido(
            cliente_id=uuid4(),
            cotacao_id=None,
            origem=endereco,
            destino=endereco
        )
        
        pedido.cancelar("Cliente solicitou cancelamento")
        
        assert pedido.status == StatusPedido.CANCELADO
        assert "Cliente solicitou cancelamento" in pedido.observacoes
    
    def test_nao_pode_cancelar_pedido_entregue(self, endereco):
        """Não deve cancelar pedido já entregue"""
        pedido = Pedido(
            cliente_id=uuid4(),
            cotacao_id=None,
            origem=endereco,
            destino=endereco
        )
        
        pedido.coletar()
        pedido.iniciar_transporte()
        pedido.sair_para_entrega()
        pedido.entregar()
        
        with pytest.raises(ValueError):
            pedido.cancelar()
