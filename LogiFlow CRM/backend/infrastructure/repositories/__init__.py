"""Infrastructure Repositories - Implementações concretas dos repositories"""
from .cliente_repository import ClienteRepository
from .cotacao_repository import CotacaoRepository
from .pedido_repository import PedidoRepository

__all__ = ["ClienteRepository", "CotacaoRepository", "PedidoRepository"]
