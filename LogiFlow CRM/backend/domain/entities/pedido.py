"""
Pedido Entity - Representa um pedido de frete no domínio
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.endereco import Endereco


class StatusPedido(str, Enum):
    AGUARDANDO_COLETA = "aguardando_coleta"
    COLETADO = "coletado"
    EM_TRANSITO = "em_transito"
    EM_TRANSFERENCIA = "em_transferencia"
    SAIU_PARA_ENTREGA = "saiu_para_entrega"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"
    DEVOLVIDO = "devolvido"


@dataclass
class Pedido:
    """
    Entidade Pedido - representa um pedido de transporte.
    """
    cliente_id: UUID
    cotacao_id: Optional[UUID]
    origem: Endereco
    destino: Endereco
    
    # Identificação
    numero: Optional[str] = None
    status: StatusPedido = StatusPedido.AGUARDANDO_COLETA
    
    # Carga
    peso_kg: Decimal = Decimal("0")
    volume_m3: Decimal = Decimal("0")
    valor_mercadoria: Decimal = Decimal("0")
    descricao_carga: Optional[str] = None
    
    # Valores
    valor_frete: Decimal = Decimal("0")
    valor_seguro: Decimal = Decimal("0")
    valor_total: Decimal = Decimal("0")
    
    # Datas
    data_coleta_prevista: Optional[datetime] = None
    data_coleta_realizada: Optional[datetime] = None
    data_entrega_prevista: Optional[datetime] = None
    data_entrega_realizada: Optional[datetime] = None
    
    # Rastreamento
    motorista_id: Optional[UUID] = None
    veiculo_id: Optional[UUID] = None
    
    # Documentos fiscais
    cte_numero: Optional[str] = None
    cte_chave: Optional[str] = None
    nfe_chave: Optional[str] = None
    
    # Metadata
    observacoes: Optional[str] = None
    
    # Campos de identidade
    _id: UUID = field(default_factory=uuid4)
    _created_at: datetime = field(default_factory=datetime.utcnow)
    _updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def coletar(self) -> None:
        """Marca o pedido como coletado"""
        if self.status != StatusPedido.AGUARDANDO_COLETA:
            raise ValueError(f"Não é possível coletar pedido com status {self.status}")
        self.status = StatusPedido.COLETADO
        self.data_coleta_realizada = datetime.utcnow()
        self._updated_at = datetime.utcnow()
    
    def iniciar_transporte(self) -> None:
        """Inicia o transporte do pedido"""
        if self.status != StatusPedido.COLETADO:
            raise ValueError(f"Não é possível iniciar transporte com status {self.status}")
        self.status = StatusPedido.EM_TRANSITO
        self._updated_at = datetime.utcnow()
    
    def sair_para_entrega(self) -> None:
        """Marca que saiu para entrega final"""
        if self.status not in [StatusPedido.EM_TRANSITO, StatusPedido.EM_TRANSFERENCIA]:
            raise ValueError(f"Não é possível sair para entrega com status {self.status}")
        self.status = StatusPedido.SAIU_PARA_ENTREGA
        self._updated_at = datetime.utcnow()
    
    def entregar(self) -> None:
        """Marca o pedido como entregue"""
        if self.status != StatusPedido.SAIU_PARA_ENTREGA:
            raise ValueError(f"Não é possível entregar pedido com status {self.status}")
        self.status = StatusPedido.ENTREGUE
        self.data_entrega_realizada = datetime.utcnow()
        self._updated_at = datetime.utcnow()
    
    def cancelar(self, motivo: Optional[str] = None) -> None:
        """Cancela o pedido"""
        if self.status in [StatusPedido.ENTREGUE, StatusPedido.CANCELADO]:
            raise ValueError(f"Não é possível cancelar pedido com status {self.status}")
        self.status = StatusPedido.CANCELADO
        if motivo:
            self.observacoes = f"{self.observacoes or ''}\nCancelado: {motivo}".strip()
        self._updated_at = datetime.utcnow()
    
    def atribuir_motorista(self, motorista_id: UUID, veiculo_id: UUID) -> None:
        """Atribui motorista e veículo ao pedido"""
        self.motorista_id = motorista_id
        self.veiculo_id = veiculo_id
        self._updated_at = datetime.utcnow()
    
    def vincular_cte(self, numero: str, chave: str) -> None:
        """Vincula CT-e ao pedido"""
        self.cte_numero = numero
        self.cte_chave = chave
        self._updated_at = datetime.utcnow()
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pedido):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
