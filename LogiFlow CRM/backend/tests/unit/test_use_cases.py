"""
Testes unitários para Use Cases
================================
Testa casos de uso com mocks dos repositories.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from decimal import Decimal

from domain.entities.cliente import Cliente
from domain.entities.cotacao import Cotacao, ItemCotacao, StatusCotacao
from domain.value_objects.endereco import Endereco
from domain.value_objects.documento import CNPJ
from domain.exceptions import EntityNotFoundException, ValidationException

from application.dtos.cliente_dto import ClienteCreateDTO, ClienteUpdateDTO, EnderecoDTO
from application.use_cases.cliente_use_cases import (
    CriarClienteUseCase,
    AtualizarClienteUseCase,
    BuscarClienteUseCase,
    ListarClientesUseCase,
)


class TestCriarClienteUseCase:
    """Testes para caso de uso Criar Cliente"""
    
    @pytest.fixture
    def mock_repository(self):
        repo = AsyncMock()
        repo.get_by_documento = AsyncMock(return_value=None)
        repo.add = AsyncMock()
        return repo
    
    @pytest.fixture
    def dto_cliente(self):
        return ClienteCreateDTO(
            razao_social="Empresa Teste Ltda",
            nome_fantasia="Teste",
            documento="11222333000181",
            email="teste@empresa.com",
            telefone="11999999999"
        )
    
    @pytest.mark.asyncio
    async def test_criar_cliente_sucesso(self, mock_repository, dto_cliente):
        """Deve criar cliente com sucesso"""
        # Configurar mock para retornar cliente criado
        def mock_add(cliente):
            return cliente
        mock_repository.add = AsyncMock(side_effect=mock_add)
        
        use_case = CriarClienteUseCase(mock_repository)
        result = await use_case.execute(dto_cliente)
        
        assert result.razao_social == "Empresa Teste Ltda"
        assert result.documento == "11222333000181"
        mock_repository.add.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_criar_cliente_documento_duplicado(self, mock_repository, dto_cliente):
        """Deve rejeitar cliente com documento duplicado"""
        # Configurar mock para simular documento existente
        cliente_existente = Cliente(
            razao_social="Outra Empresa",
            documento=CNPJ("11222333000181")
        )
        mock_repository.get_by_documento = AsyncMock(return_value=cliente_existente)
        
        use_case = CriarClienteUseCase(mock_repository)
        
        with pytest.raises(ValidationException, match="Já existe cliente"):
            await use_case.execute(dto_cliente)


class TestAtualizarClienteUseCase:
    """Testes para caso de uso Atualizar Cliente"""
    
    @pytest.fixture
    def mock_repository(self):
        repo = AsyncMock()
        return repo
    
    @pytest.fixture
    def cliente_existente(self):
        return Cliente(
            razao_social="Empresa Original",
            documento=CNPJ("11222333000181"),
            email="original@empresa.com",
            ativo=True
        )
    
    @pytest.mark.asyncio
    async def test_atualizar_cliente_sucesso(self, mock_repository, cliente_existente):
        """Deve atualizar cliente com sucesso"""
        mock_repository.get_by_id = AsyncMock(return_value=cliente_existente)
        mock_repository.update = AsyncMock(return_value=cliente_existente)
        
        use_case = AtualizarClienteUseCase(mock_repository)
        dto = ClienteUpdateDTO(razao_social="Empresa Atualizada")
        
        result = await use_case.execute(cliente_existente.id, dto)
        
        mock_repository.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_atualizar_cliente_nao_encontrado(self, mock_repository):
        """Deve falhar ao atualizar cliente inexistente"""
        mock_repository.get_by_id = AsyncMock(return_value=None)
        
        use_case = AtualizarClienteUseCase(mock_repository)
        dto = ClienteUpdateDTO(razao_social="Nova Razão")
        
        with pytest.raises(EntityNotFoundException):
            await use_case.execute(uuid4(), dto)


class TestBuscarClienteUseCase:
    """Testes para caso de uso Buscar Cliente"""
    
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()
    
    @pytest.fixture
    def cliente(self):
        return Cliente(
            razao_social="Empresa Teste",
            documento=CNPJ("11222333000181")
        )
    
    @pytest.mark.asyncio
    async def test_buscar_cliente_existente(self, mock_repository, cliente):
        """Deve retornar cliente existente"""
        mock_repository.get_by_id = AsyncMock(return_value=cliente)
        
        use_case = BuscarClienteUseCase(mock_repository)
        result = await use_case.execute(cliente.id)
        
        assert result.razao_social == "Empresa Teste"
    
    @pytest.mark.asyncio
    async def test_buscar_cliente_nao_encontrado(self, mock_repository):
        """Deve falhar ao buscar cliente inexistente"""
        mock_repository.get_by_id = AsyncMock(return_value=None)
        
        use_case = BuscarClienteUseCase(mock_repository)
        
        with pytest.raises(EntityNotFoundException):
            await use_case.execute(uuid4())


class TestListarClientesUseCase:
    """Testes para caso de uso Listar Clientes"""
    
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()
    
    @pytest.fixture
    def clientes(self):
        return [
            Cliente(razao_social="Empresa A", documento=CNPJ("11222333000181")),
            Cliente(razao_social="Empresa B", documento=CNPJ("45997418000153")),
        ]
    
    @pytest.mark.asyncio
    async def test_listar_todos_clientes(self, mock_repository, clientes):
        """Deve listar todos os clientes"""
        mock_repository.get_all = AsyncMock(return_value=clientes)
        
        use_case = ListarClientesUseCase(mock_repository)
        result = await use_case.execute()
        
        assert len(result) == 2
    
    @pytest.mark.asyncio
    async def test_listar_apenas_ativos(self, mock_repository, clientes):
        """Deve listar apenas clientes ativos"""
        mock_repository.get_ativos = AsyncMock(return_value=clientes[:1])
        
        use_case = ListarClientesUseCase(mock_repository)
        result = await use_case.execute(apenas_ativos=True)
        
        assert len(result) == 1
        mock_repository.get_ativos.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_buscar_por_termo(self, mock_repository, clientes):
        """Deve buscar clientes por termo"""
        mock_repository.search = AsyncMock(return_value=clientes[:1])
        
        use_case = ListarClientesUseCase(mock_repository)
        result = await use_case.execute(termo_busca="Empresa A")
        
        assert len(result) == 1
        mock_repository.search.assert_called_once_with("Empresa A", 0, 100)
