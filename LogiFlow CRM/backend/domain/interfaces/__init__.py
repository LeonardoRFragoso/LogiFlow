"""Domain Interfaces - Contratos para repositories"""
from .repositories import (
    IClienteRepository,
    ICotacaoRepository,
    IPedidoRepository,
)

__all__ = [
    "IClienteRepository",
    "ICotacaoRepository", 
    "IPedidoRepository",
]
