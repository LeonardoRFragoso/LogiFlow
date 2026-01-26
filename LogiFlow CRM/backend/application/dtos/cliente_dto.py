"""
Cliente DTOs - Data Transfer Objects para Cliente
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class EnderecoDTO(BaseModel):
    """DTO para endereço"""
    logradouro: str = Field(..., min_length=1, max_length=200)
    numero: str = Field(..., min_length=1, max_length=20)
    bairro: str = Field(..., min_length=1, max_length=100)
    cidade: str = Field(..., min_length=1, max_length=100)
    uf: str = Field(..., min_length=2, max_length=2)
    cep: str = Field(..., min_length=8, max_length=9)
    complemento: Optional[str] = Field(None, max_length=100)
    
    @field_validator('uf')
    @classmethod
    def uf_uppercase(cls, v: str) -> str:
        return v.upper()
    
    @field_validator('cep')
    @classmethod
    def cep_format(cls, v: str) -> str:
        return re.sub(r'\D', '', v)


class ClienteCreateDTO(BaseModel):
    """DTO para criação de cliente"""
    razao_social: str = Field(..., min_length=2, max_length=200)
    nome_fantasia: Optional[str] = Field(None, max_length=200)
    documento: str = Field(..., description="CNPJ ou CPF")
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[EnderecoDTO] = None
    inscricao_estadual: Optional[str] = Field(None, max_length=20)
    observacoes: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('documento')
    @classmethod
    def documento_digits(cls, v: str) -> str:
        return re.sub(r'\D', '', v)
    
    @field_validator('telefone')
    @classmethod
    def telefone_digits(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return re.sub(r'\D', '', v)
        return v


class ClienteUpdateDTO(BaseModel):
    """DTO para atualização de cliente"""
    razao_social: Optional[str] = Field(None, min_length=2, max_length=200)
    nome_fantasia: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[EnderecoDTO] = None
    inscricao_estadual: Optional[str] = Field(None, max_length=20)
    observacoes: Optional[str] = Field(None, max_length=1000)
    ativo: Optional[bool] = None


class ClienteResponseDTO(BaseModel):
    """DTO para resposta de cliente"""
    id: UUID
    razao_social: str
    nome_fantasia: Optional[str]
    documento: str
    documento_formatado: str
    email: Optional[str]
    telefone: Optional[str]
    endereco: Optional[EnderecoDTO]
    inscricao_estadual: Optional[str]
    ativo: bool
    observacoes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
