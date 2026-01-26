"""
Repository Interfaces - Contratos para acesso a dados
"""
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from ..entities.cliente import Cliente
from ..entities.cotacao import Cotacao, StatusCotacao
from ..entities.pedido import Pedido, StatusPedido


T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """Interface base para repositories"""
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Busca entidade por ID"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Lista todas as entidades com paginação"""
        pass
    
    @abstractmethod
    async def add(self, entity: T) -> T:
        """Adiciona nova entidade"""
        pass
    
    @abstractmethod
    async def update(self, entity: T) -> T:
        """Atualiza entidade existente"""
        pass
    
    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Remove entidade por ID"""
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """Retorna total de entidades"""
        pass


class IClienteRepository(IRepository[Cliente]):
    """Interface para repository de clientes"""
    
    @abstractmethod
    async def get_by_documento(self, documento: str) -> Optional[Cliente]:
        """Busca cliente por CNPJ ou CPF"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Cliente]:
        """Busca cliente por email"""
        pass
    
    @abstractmethod
    async def search(self, termo: str, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Busca clientes por termo (nome, documento, email)"""
        pass
    
    @abstractmethod
    async def get_ativos(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Lista apenas clientes ativos"""
        pass


class ICotacaoRepository(IRepository[Cotacao]):
    """Interface para repository de cotações"""
    
    @abstractmethod
    async def get_by_numero(self, numero: str) -> Optional[Cotacao]:
        """Busca cotação por número"""
        pass
    
    @abstractmethod
    async def get_by_cliente(
        self, 
        cliente_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Cotacao]:
        """Lista cotações de um cliente"""
        pass
    
    @abstractmethod
    async def get_by_status(
        self, 
        status: StatusCotacao, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Cotacao]:
        """Lista cotações por status"""
        pass
    
    @abstractmethod
    async def get_expiradas(self) -> List[Cotacao]:
        """Lista cotações expiradas"""
        pass


class IPedidoRepository(IRepository[Pedido]):
    """Interface para repository de pedidos"""
    
    @abstractmethod
    async def get_by_numero(self, numero: str) -> Optional[Pedido]:
        """Busca pedido por número"""
        pass
    
    @abstractmethod
    async def get_by_cliente(
        self, 
        cliente_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Pedido]:
        """Lista pedidos de um cliente"""
        pass
    
    @abstractmethod
    async def get_by_status(
        self, 
        status: StatusPedido, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Pedido]:
        """Lista pedidos por status"""
        pass
    
    @abstractmethod
    async def get_by_motorista(
        self, 
        motorista_id: UUID, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Pedido]:
        """Lista pedidos de um motorista"""
        pass
    
    @abstractmethod
    async def get_em_transito(self) -> List[Pedido]:
        """Lista pedidos em trânsito"""
        pass
