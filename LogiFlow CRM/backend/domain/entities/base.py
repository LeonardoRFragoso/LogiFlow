"""
Base Entity - Classe base para todas as entidades de domínio
"""
from abc import ABC
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Entity(ABC):
    """
    Classe base para entidades de domínio.
    Entidades possuem identidade única e ciclo de vida.
    """
    
    def __init__(
        self,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = id or uuid4()
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def touch(self) -> None:
        """Atualiza o timestamp de modificação"""
        self._updated_at = datetime.utcnow()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"
