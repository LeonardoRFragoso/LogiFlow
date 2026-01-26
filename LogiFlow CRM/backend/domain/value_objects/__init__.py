"""Domain Value Objects - Objetos imutáveis sem identidade"""
from .endereco import Endereco
from .documento import CNPJ, CPF

__all__ = ["Endereco", "CNPJ", "CPF"]
