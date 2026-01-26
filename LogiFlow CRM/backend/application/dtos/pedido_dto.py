"""
Pedido DTOs - Data Transfer Objects para Pedido
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .cliente_dto import EnderecoDTO


class PedidoCreateDTO(BaseModel):
    """DTO para criação de pedido"""
    cliente_id: UUID
    cotacao_id: Optional[UUID] = None
    origem: EnderecoDTO
    destino: EnderecoDTO
    
    peso_kg: Decimal = Field(..., gt=0)
    volume_m3: Optional[Decimal] = Field(None, ge=0)
    valor_mercadoria: Optional[Decimal] = Field(None, ge=0)
    descricao_carga: Optional[str] = Field(None, max_length=500)
    
    valor_frete: Decimal = Field(..., ge=0)
    valor_seguro: Optional[Decimal] = Field(None, ge=0)
    
    data_coleta_prevista: Optional[datetime] = None
    data_entrega_prevista: Optional[datetime] = None
    
    observacoes: Optional[str] = Field(None, max_length=1000)


class PedidoResponseDTO(BaseModel):
    """DTO para resposta de pedido"""
    id: UUID
    numero: str
    cliente_id: UUID
    cotacao_id: Optional[UUID]
    
    origem: EnderecoDTO
    destino: EnderecoDTO
    status: str
    
    peso_kg: Decimal
    volume_m3: Decimal
    valor_mercadoria: Decimal
    descricao_carga: Optional[str]
    
    valor_frete: Decimal
    valor_seguro: Decimal
    valor_total: Decimal
    
    data_coleta_prevista: Optional[datetime]
    data_coleta_realizada: Optional[datetime]
    data_entrega_prevista: Optional[datetime]
    data_entrega_realizada: Optional[datetime]
    
    motorista_id: Optional[UUID]
    veiculo_id: Optional[UUID]
    
    cte_numero: Optional[str]
    cte_chave: Optional[str]
    nfe_chave: Optional[str]
    
    observacoes: Optional[str]
    
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
