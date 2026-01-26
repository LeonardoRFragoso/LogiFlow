"""
Cotação Entity - Representa uma cotação de frete no domínio
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from ..value_objects.endereco import Endereco


class StatusCotacao(str, Enum):
    RASCUNHO = "rascunho"
    ENVIADA = "enviada"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    EXPIRADA = "expirada"
    CONVERTIDA = "convertida"


class TipoFrete(str, Enum):
    CIF = "CIF"  # Frete por conta do remetente
    FOB = "FOB"  # Frete por conta do destinatário


class TipoCarga(str, Enum):
    FRACIONADA = "fracionada"
    COMPLETA = "completa"
    EXPRESSA = "expressa"


@dataclass
class ItemCotacao:
    """Value Object - Item de uma cotação"""
    descricao: str
    quantidade: int
    peso_kg: Decimal
    volume_m3: Optional[Decimal] = None
    valor_mercadoria: Optional[Decimal] = None
    observacao: Optional[str] = None
    
    def __post_init__(self):
        if self.quantidade < 1:
            raise ValueError("Quantidade deve ser maior que zero")
        if self.peso_kg <= 0:
            raise ValueError("Peso deve ser maior que zero")


@dataclass
class Cotacao:
    """
    Entidade Cotação - representa uma proposta de frete.
    """
    cliente_id: UUID
    origem: Endereco
    destino: Endereco
    itens: List[ItemCotacao]
    
    # Dados da cotação
    numero: Optional[str] = None
    tipo_frete: TipoFrete = TipoFrete.CIF
    tipo_carga: TipoCarga = TipoCarga.FRACIONADA
    status: StatusCotacao = StatusCotacao.RASCUNHO
    
    # Valores
    valor_frete: Decimal = Decimal("0")
    valor_seguro: Decimal = Decimal("0")
    valor_outros: Decimal = Decimal("0")
    desconto: Decimal = Decimal("0")
    
    # Datas
    validade: Optional[date] = None
    
    # Metadata
    observacoes: Optional[str] = None
    criado_por: Optional[str] = None
    
    # Campos de identidade
    _id: UUID = field(default_factory=uuid4)
    _created_at: datetime = field(default_factory=datetime.utcnow)
    _updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.itens:
            raise ValueError("Cotação deve ter pelo menos um item")
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    @property
    def valor_total(self) -> Decimal:
        return self.valor_frete + self.valor_seguro + self.valor_outros - self.desconto
    
    @property
    def peso_total(self) -> Decimal:
        return sum(item.peso_kg * item.quantidade for item in self.itens)
    
    @property
    def volume_total(self) -> Decimal:
        return sum(
            (item.volume_m3 or Decimal("0")) * item.quantidade 
            for item in self.itens
        )
    
    def enviar(self) -> None:
        """Envia a cotação para o cliente"""
        if self.status != StatusCotacao.RASCUNHO:
            raise ValueError(f"Não é possível enviar cotação com status {self.status}")
        self.status = StatusCotacao.ENVIADA
        self._updated_at = datetime.utcnow()
    
    def aprovar(self) -> None:
        """Cliente aprova a cotação"""
        if self.status != StatusCotacao.ENVIADA:
            raise ValueError(f"Não é possível aprovar cotação com status {self.status}")
        self.status = StatusCotacao.APROVADA
        self._updated_at = datetime.utcnow()
    
    def rejeitar(self) -> None:
        """Cliente rejeita a cotação"""
        if self.status != StatusCotacao.ENVIADA:
            raise ValueError(f"Não é possível rejeitar cotação com status {self.status}")
        self.status = StatusCotacao.REJEITADA
        self._updated_at = datetime.utcnow()
    
    def converter_em_pedido(self) -> None:
        """Marca a cotação como convertida em pedido"""
        if self.status != StatusCotacao.APROVADA:
            raise ValueError("Apenas cotações aprovadas podem ser convertidas")
        self.status = StatusCotacao.CONVERTIDA
        self._updated_at = datetime.utcnow()
    
    def esta_expirada(self) -> bool:
        """Verifica se a cotação está expirada"""
        if not self.validade:
            return False
        return date.today() > self.validade
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cotacao):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
