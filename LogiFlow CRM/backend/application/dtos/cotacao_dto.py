"""
Cotação DTOs - Data Transfer Objects para Cotação
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from .cliente_dto import EnderecoDTO


class ItemCotacaoDTO(BaseModel):
    """DTO para item de cotação"""
    descricao: str = Field(..., min_length=1, max_length=200)
    quantidade: int = Field(..., ge=1)
    peso_kg: Decimal = Field(..., gt=0)
    volume_m3: Optional[Decimal] = Field(None, ge=0)
    valor_mercadoria: Optional[Decimal] = Field(None, ge=0)
    observacao: Optional[str] = Field(None, max_length=500)


class CotacaoCreateDTO(BaseModel):
    """DTO para criação de cotação"""
    cliente_id: UUID
    origem: EnderecoDTO
    destino: EnderecoDTO
    itens: List[ItemCotacaoDTO] = Field(..., min_length=1)
    
    tipo_frete: str = Field("CIF", pattern="^(CIF|FOB)$")
    tipo_carga: str = Field("fracionada", pattern="^(fracionada|completa|expressa)$")
    
    valor_frete: Optional[Decimal] = Field(None, ge=0)
    valor_seguro: Optional[Decimal] = Field(None, ge=0)
    valor_outros: Optional[Decimal] = Field(None, ge=0)
    desconto: Optional[Decimal] = Field(None, ge=0)
    
    validade: Optional[date] = None
    observacoes: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('validade')
    @classmethod
    def validade_futura(cls, v: Optional[date]) -> Optional[date]:
        if v and v < date.today():
            raise ValueError("Validade deve ser uma data futura")
        return v


class CotacaoResponseDTO(BaseModel):
    """DTO para resposta de cotação"""
    id: UUID
    numero: str
    cliente_id: UUID
    origem: EnderecoDTO
    destino: EnderecoDTO
    itens: List[ItemCotacaoDTO]
    
    tipo_frete: str
    tipo_carga: str
    status: str
    
    valor_frete: Decimal
    valor_seguro: Decimal
    valor_outros: Decimal
    desconto: Decimal
    valor_total: Decimal
    
    peso_total: Decimal
    volume_total: Decimal
    
    validade: Optional[date]
    observacoes: Optional[str]
    criado_por: Optional[str]
    
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
