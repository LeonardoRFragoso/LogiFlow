"""Application Use Cases - Casos de uso da aplicação"""
from .cliente_use_cases import (
    CriarClienteUseCase,
    AtualizarClienteUseCase,
    BuscarClienteUseCase,
    ListarClientesUseCase,
)
from .cotacao_use_cases import (
    CriarCotacaoUseCase,
    EnviarCotacaoUseCase,
    AprovarCotacaoUseCase,
)

__all__ = [
    "CriarClienteUseCase",
    "AtualizarClienteUseCase", 
    "BuscarClienteUseCase",
    "ListarClientesUseCase",
    "CriarCotacaoUseCase",
    "EnviarCotacaoUseCase",
    "AprovarCotacaoUseCase",
]
