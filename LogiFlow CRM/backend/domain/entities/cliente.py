"""
Cliente Entity - Representa um cliente no domínio
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from .base import Entity
from ..value_objects.endereco import Endereco
from ..value_objects.documento import CNPJ, CPF


@dataclass
class Cliente(Entity):
    """
    Entidade Cliente - representa uma empresa ou pessoa física cliente.
    """
    razao_social: str
    nome_fantasia: Optional[str] = None
    documento: Optional[CNPJ | CPF] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[Endereco] = None
    inscricao_estadual: Optional[str] = None
    ativo: bool = True
    observacoes: Optional[str] = None
    
    # Campos herdados de Entity
    _id: UUID = field(default_factory=uuid4)
    _created_at: datetime = field(default_factory=datetime.utcnow)
    _updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.razao_social or not self.razao_social.strip():
            raise ValueError("Razão social é obrigatória")
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def ativar(self) -> None:
        self.ativo = True
        self._updated_at = datetime.utcnow()
    
    def desativar(self) -> None:
        self.ativo = False
        self._updated_at = datetime.utcnow()
    
    def atualizar_endereco(self, endereco: Endereco) -> None:
        self.endereco = endereco
        self._updated_at = datetime.utcnow()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cliente):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
