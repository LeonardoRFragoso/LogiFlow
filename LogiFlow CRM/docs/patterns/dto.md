# DTO Pattern (Data Transfer Objects) - LogiFlow CRM

> **Status:** Implementado  
> **Camada:** Application  
> **Arquivos:** `backend/application/dtos/`

## O que são DTOs?

DTOs (Data Transfer Objects) são objetos simples usados para transferir dados entre camadas ou processos. Eles encapsulam dados sem comportamento de negócio.

```
┌─────────────┐                    ┌─────────────┐                    ┌─────────────┐
│   Client    │ ──── Request ────▶ │    API      │ ──── DTO ────────▶ │  Use Case   │
│  (Frontend) │ ◀─── Response ──── │   Layer     │ ◀─── DTO ──────── │   Layer     │
└─────────────┘                    └─────────────┘                    └─────────────┘
                                         │
                                   CreateDTO                             Entity
                                   UpdateDTO                               │
                                   ResponseDTO                             ▼
                                   ListDTO                            Repository
```

## Por que usamos?

| Benefício | Descrição |
|-----------|-----------|
| **Validação** | Pydantic valida dados na entrada |
| **Segurança** | Controle do que entra e sai da API |
| **Documentação** | Swagger gerado automaticamente |
| **Desacoplamento** | API não expõe entidades internas |
| **Versionamento** | DTOs podem evoluir independentemente |

## Tipos de DTOs

| Tipo | Propósito | Direção |
|------|-----------|---------|
| `CreateDTO` | Dados para criar recurso | Request → API |
| `UpdateDTO` | Dados para atualizar recurso | Request → API |
| `ResponseDTO` | Dados retornados ao cliente | API → Response |
| `ListDTO` | Lista paginada de recursos | API → Response |
| `FilterDTO` | Parâmetros de busca/filtro | Request → API |

## Implementação no LogiFlow

### 1. DTOs com Pydantic v2

```python
# backend/application/dtos/cliente_dto.py

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
import re


class ClienteCreateDTO(BaseModel):
    """DTO para criação de cliente."""
    
    cnpj: str = Field(
        ...,
        min_length=14,
        max_length=18,
        description="CNPJ do cliente (apenas números ou formatado)",
        examples=["12345678000190", "12.345.678/0001-90"]
    )
    razao_social: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Razão social da empresa"
    )
    nome_fantasia: Optional[str] = Field(
        None,
        max_length=200,
        description="Nome fantasia (opcional)"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Email de contato"
    )
    telefone: Optional[str] = Field(
        None,
        max_length=20,
        description="Telefone de contato"
    )
    endereco: Optional[str] = Field(
        None,
        max_length=500,
        description="Endereço completo"
    )
    
    @field_validator('cnpj')
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        """Remove formatação e valida CNPJ."""
        # Remove caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', v)
        
        if len(cnpj) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        
        # Validação do dígito verificador (simplificada)
        if cnpj == cnpj[0] * 14:
            raise ValueError('CNPJ inválido')
        
        return cnpj
    
    @field_validator('telefone')
    @classmethod
    def validate_telefone(cls, v: Optional[str]) -> Optional[str]:
        """Remove formatação do telefone."""
        if v is None:
            return v
        return re.sub(r'[^0-9]', '', v)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cnpj": "12345678000190",
                    "razao_social": "Empresa Exemplo LTDA",
                    "email": "contato@empresa.com",
                    "telefone": "11999998888"
                }
            ]
        }
    }


class ClienteUpdateDTO(BaseModel):
    """DTO para atualização de cliente (campos opcionais)."""
    
    razao_social: Optional[str] = Field(None, min_length=2, max_length=200)
    nome_fantasia: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = Field(None, max_length=500)
    ativo: Optional[bool] = None
    
    @field_validator('telefone')
    @classmethod
    def validate_telefone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return re.sub(r'[^0-9]', '', v)


class ClienteResponseDTO(BaseModel):
    """DTO para resposta de cliente."""
    
    id: str = Field(..., description="ID único do cliente")
    cnpj: str = Field(..., description="CNPJ formatado")
    razao_social: str
    nome_fantasia: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_entity(cls, entity: 'Cliente') -> 'ClienteResponseDTO':
        """Factory method: converte Entity para DTO."""
        return cls(
            id=entity.id,
            cnpj=cls._format_cnpj(str(entity.cnpj)),
            razao_social=entity.razao_social,
            nome_fantasia=entity.nome_fantasia,
            email=str(entity.email) if entity.email else None,
            telefone=cls._format_telefone(entity.telefone),
            endereco=entity.endereco,
            ativo=entity.ativo,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    @staticmethod
    def _format_cnpj(cnpj: str) -> str:
        """Formata CNPJ: 12.345.678/0001-90"""
        if len(cnpj) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj
    
    @staticmethod
    def _format_telefone(telefone: Optional[str]) -> Optional[str]:
        """Formata telefone: (11) 99999-8888"""
        if not telefone:
            return None
        t = re.sub(r'[^0-9]', '', telefone)
        if len(t) == 11:
            return f"({t[:2]}) {t[2:7]}-{t[7:]}"
        elif len(t) == 10:
            return f"({t[:2]}) {t[2:6]}-{t[6:]}"
        return telefone
    
    model_config = {
        "from_attributes": True
    }


class ClienteListDTO(BaseModel):
    """DTO para lista paginada de clientes."""
    
    items: List[ClienteResponseDTO]
    total: int = Field(..., description="Total de registros")
    skip: int = Field(..., description="Registros pulados")
    limit: int = Field(..., description="Limite por página")
    has_more: bool = Field(..., description="Existem mais registros")
    
    @classmethod
    def from_list(
        cls,
        entities: List['Cliente'],
        total: int,
        skip: int,
        limit: int
    ) -> 'ClienteListDTO':
        """Factory method: converte lista de entities para DTO."""
        return cls(
            items=[ClienteResponseDTO.from_entity(e) for e in entities],
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + limit) < total
        )
```

### 2. DTOs de Cotação

```python
# backend/application/dtos/cotacao_dto.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


class StatusCotacao(str, Enum):
    PENDENTE = "pendente"
    ENVIADA = "enviada"
    APROVADA = "aprovada"
    RECUSADA = "recusada"
    EXPIRADA = "expirada"


class EnderecoDTO(BaseModel):
    """DTO para endereço de origem/destino."""
    
    cep: str = Field(..., min_length=8, max_length=9)
    logradouro: str = Field(..., max_length=200)
    numero: str = Field(..., max_length=20)
    complemento: Optional[str] = Field(None, max_length=100)
    bairro: str = Field(..., max_length=100)
    cidade: str = Field(..., max_length=100)
    uf: str = Field(..., min_length=2, max_length=2)
    
    @field_validator('cep')
    @classmethod
    def validate_cep(cls, v: str) -> str:
        return re.sub(r'[^0-9]', '', v)
    
    @field_validator('uf')
    @classmethod
    def validate_uf(cls, v: str) -> str:
        return v.upper()


class CotacaoCreateDTO(BaseModel):
    """DTO para criação de cotação."""
    
    cliente_id: str = Field(..., description="ID do cliente")
    origem: EnderecoDTO
    destino: EnderecoDTO
    peso_kg: Decimal = Field(..., gt=0, description="Peso em KG")
    volumes: int = Field(1, ge=1, description="Quantidade de volumes")
    valor_mercadoria: Optional[Decimal] = Field(None, ge=0)
    observacoes: Optional[str] = Field(None, max_length=1000)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "cliente_id": "uuid-cliente",
                    "origem": {
                        "cep": "01310100",
                        "logradouro": "Av. Paulista",
                        "numero": "1000",
                        "bairro": "Bela Vista",
                        "cidade": "São Paulo",
                        "uf": "SP"
                    },
                    "destino": {
                        "cep": "22041080",
                        "logradouro": "Av. Atlântica",
                        "numero": "500",
                        "bairro": "Copacabana",
                        "cidade": "Rio de Janeiro",
                        "uf": "RJ"
                    },
                    "peso_kg": 10.5,
                    "volumes": 2,
                    "valor_mercadoria": 1500.00
                }
            ]
        }
    }


class CotacaoResponseDTO(BaseModel):
    """DTO para resposta de cotação."""
    
    id: str
    numero: str = Field(..., description="Número da cotação (ex: COT-2026-0001)")
    cliente_id: str
    cliente_nome: str
    origem: EnderecoDTO
    destino: EnderecoDTO
    peso_kg: Decimal
    volumes: int
    valor_frete: Decimal
    valor_mercadoria: Optional[Decimal]
    status: StatusCotacao
    validade: datetime
    observacoes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    @classmethod
    def from_entity(cls, entity: 'Cotacao', cliente_nome: str) -> 'CotacaoResponseDTO':
        return cls(
            id=entity.id,
            numero=entity.numero,
            cliente_id=entity.cliente_id,
            cliente_nome=cliente_nome,
            origem=EnderecoDTO(**entity.origem),
            destino=EnderecoDTO(**entity.destino),
            peso_kg=entity.peso_kg,
            volumes=entity.volumes,
            valor_frete=entity.valor_frete,
            valor_mercadoria=entity.valor_mercadoria,
            status=entity.status,
            validade=entity.validade,
            observacoes=entity.observacoes,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    model_config = {
        "from_attributes": True
    }
```

### 3. Uso nos Routers

```python
# backend/presentation/api/clientes_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from application.dtos.cliente_dto import (
    ClienteCreateDTO,
    ClienteUpdateDTO,
    ClienteResponseDTO,
    ClienteListDTO
)

router = APIRouter(prefix="/v2/clientes", tags=["Clientes v2"])


@router.post(
    "/",
    response_model=ClienteResponseDTO,
    status_code=201,
    summary="Criar cliente",
    description="Cria um novo cliente no sistema"
)
async def criar_cliente(
    dto: ClienteCreateDTO,  # Valida automaticamente
    use_case: CriarClienteUseCase = Depends(get_criar_cliente_use_case),
    tenant_id: str = Depends(get_tenant_id)
):
    return use_case.execute(dto, tenant_id)


@router.get(
    "/",
    response_model=ClienteListDTO,
    summary="Listar clientes"
)
async def listar_clientes(
    skip: int = Query(0, ge=0, description="Registros a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Limite por página"),
    search: Optional[str] = Query(None, description="Busca por nome/CNPJ"),
    use_case: ListarClientesUseCase = Depends(get_listar_clientes_use_case),
    tenant_id: str = Depends(get_tenant_id)
):
    return use_case.execute(tenant_id, skip, limit, search)


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponseDTO,
    summary="Buscar cliente por ID"
)
async def buscar_cliente(
    cliente_id: str,
    use_case: BuscarClienteUseCase = Depends(get_buscar_cliente_use_case),
    tenant_id: str = Depends(get_tenant_id)
):
    cliente = use_case.execute(cliente_id, tenant_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.patch(
    "/{cliente_id}",
    response_model=ClienteResponseDTO,
    summary="Atualizar cliente"
)
async def atualizar_cliente(
    cliente_id: str,
    dto: ClienteUpdateDTO,  # Campos opcionais
    use_case: AtualizarClienteUseCase = Depends(get_atualizar_cliente_use_case),
    tenant_id: str = Depends(get_tenant_id)
):
    return use_case.execute(cliente_id, dto, tenant_id)
```

## Swagger Gerado Automaticamente

Os DTOs com Pydantic geram documentação automática no Swagger:

```
POST /v2/clientes/
├── Request Body (ClienteCreateDTO)
│   ├── cnpj: string (required, 14 chars)
│   ├── razao_social: string (required, 2-200 chars)
│   ├── email: string (optional, email format)
│   └── telefone: string (optional)
│
└── Response (ClienteResponseDTO)
    ├── id: string
    ├── cnpj: string (formatted)
    ├── razao_social: string
    ├── email: string
    ├── created_at: datetime
    └── ...
```

## Boas Práticas

### ✅ Faça

1. **Validação na entrada**
   ```python
   @field_validator('cnpj')
   def validate_cnpj(cls, v): ...
   ```

2. **Factory methods para conversão**
   ```python
   @classmethod
   def from_entity(cls, entity): ...
   ```

3. **Exemplos no schema**
   ```python
   model_config = {"json_schema_extra": {"examples": [...]}}
   ```

### ❌ Evite

1. **Expor entidades diretamente**
   ```python
   return entity  # ❌ Expõe internos
   return ResponseDTO.from_entity(entity)  # ✅
   ```

2. **Lógica de negócio em DTOs**
   ```python
   class DTO:
       def calculate_tax(self): ...  # ❌
   ```

## Referências

- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [DTO Pattern - Martin Fowler](https://martinfowler.com/eaaCatalog/dataTransferObject.html)
