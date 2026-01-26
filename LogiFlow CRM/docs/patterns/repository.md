# Repository Pattern - LogiFlow CRM

> **Status:** Implementado  
> **Camada:** Infrastructure  
> **Arquivos:** `backend/infrastructure/repositories/`

## O que é o Repository Pattern?

O Repository Pattern abstrai a camada de persistência de dados, fornecendo uma interface limpa para operações de CRUD. Ele separa a lógica de negócio do acesso a dados.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Use Case   │────▶│ IRepository │◀────│  Repository │
│             │     │ (Interface) │     │   (Impl)    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Database   │
                                        └─────────────┘
```

## Por que usamos?

| Benefício | Descrição |
|-----------|-----------|
| **Testabilidade** | Use cases podem ser testados com mocks |
| **Desacoplamento** | Domínio não conhece SQLAlchemy |
| **Flexibilidade** | Trocar banco sem afetar negócio |
| **Consistência** | Interface única para todos os repositórios |

## Implementação no LogiFlow

### 1. Interface (Contrato)

```python
# backend/domain/interfaces/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from domain.entities.base import Entity

T = TypeVar('T', bound=Entity)

class IRepository(ABC, Generic[T]):
    """Interface base para todos os repositórios."""
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        """Busca entidade por ID."""
        pass
    
    @abstractmethod
    def list(self, tenant_id: str, skip: int = 0, limit: int = 100) -> List[T]:
        """Lista entidades com paginação."""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Cria nova entidade."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Atualiza entidade existente."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Remove entidade por ID."""
        pass


class IClienteRepository(IRepository['Cliente']):
    """Interface específica para repositório de clientes."""
    
    @abstractmethod
    def get_by_cnpj(self, cnpj: str, tenant_id: str) -> Optional['Cliente']:
        """Busca cliente por CNPJ."""
        pass
    
    @abstractmethod
    def search(self, query: str, tenant_id: str) -> List['Cliente']:
        """Busca clientes por texto."""
        pass


class ICotacaoRepository(IRepository['Cotacao']):
    """Interface específica para repositório de cotações."""
    
    @abstractmethod
    def get_by_status(self, status: str, tenant_id: str) -> List['Cotacao']:
        """Lista cotações por status."""
        pass
    
    @abstractmethod
    def get_by_cliente(self, cliente_id: str) -> List['Cotacao']:
        """Lista cotações de um cliente."""
        pass


class IPedidoRepository(IRepository['Pedido']):
    """Interface específica para repositório de pedidos."""
    
    @abstractmethod
    def get_pendentes(self, tenant_id: str) -> List['Pedido']:
        """Lista pedidos pendentes."""
        pass
```

### 2. Implementação Concreta

```python
# backend/infrastructure/repositories/cliente_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from domain.interfaces.repositories import IClienteRepository
from domain.entities.cliente import Cliente
from domain.value_objects import CNPJ, Email
from models import Cliente as ClienteModel


class ClienteRepository(IClienteRepository):
    """Implementação SQLAlchemy do repositório de clientes."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: str) -> Optional[Cliente]:
        """Busca cliente por ID."""
        model = self.db.query(ClienteModel).filter_by(id=id).first()
        return self._to_entity(model) if model else None
    
    def list(self, tenant_id: str, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """Lista clientes do tenant com paginação."""
        models = (
            self.db.query(ClienteModel)
            .filter_by(tenant_id=tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    def create(self, entity: Cliente) -> Cliente:
        """Cria novo cliente."""
        model = self._to_model(entity)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)
    
    def update(self, entity: Cliente) -> Cliente:
        """Atualiza cliente existente."""
        model = self.db.query(ClienteModel).filter_by(id=entity.id).first()
        if not model:
            raise ValueError(f"Cliente {entity.id} não encontrado")
        
        model.cnpj = str(entity.cnpj)
        model.razao_social = entity.razao_social
        model.email = str(entity.email) if entity.email else None
        model.telefone = entity.telefone
        model.endereco = entity.endereco
        
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)
    
    def delete(self, id: str) -> bool:
        """Remove cliente por ID."""
        model = self.db.query(ClienteModel).filter_by(id=id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True
    
    def get_by_cnpj(self, cnpj: str, tenant_id: str) -> Optional[Cliente]:
        """Busca cliente por CNPJ."""
        model = (
            self.db.query(ClienteModel)
            .filter_by(cnpj=cnpj, tenant_id=tenant_id)
            .first()
        )
        return self._to_entity(model) if model else None
    
    def search(self, query: str, tenant_id: str) -> List[Cliente]:
        """Busca clientes por texto (razão social ou CNPJ)."""
        models = (
            self.db.query(ClienteModel)
            .filter(ClienteModel.tenant_id == tenant_id)
            .filter(
                or_(
                    ClienteModel.razao_social.ilike(f"%{query}%"),
                    ClienteModel.cnpj.ilike(f"%{query}%")
                )
            )
            .limit(50)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    # ========================================
    # Métodos de Mapeamento
    # ========================================
    
    def _to_entity(self, model: ClienteModel) -> Cliente:
        """Converte SQLAlchemy model para Domain entity."""
        return Cliente(
            id=model.id,
            cnpj=CNPJ(model.cnpj) if model.cnpj else None,
            razao_social=model.razao_social,
            email=Email(model.email) if model.email else None,
            telefone=model.telefone,
            endereco=model.endereco,
            tenant_id=model.tenant_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Cliente) -> ClienteModel:
        """Converte Domain entity para SQLAlchemy model."""
        return ClienteModel(
            id=entity.id,
            cnpj=str(entity.cnpj) if entity.cnpj else None,
            razao_social=entity.razao_social,
            email=str(entity.email) if entity.email else None,
            telefone=entity.telefone,
            endereco=entity.endereco,
            tenant_id=entity.tenant_id
        )
```

### 3. Uso no Use Case

```python
# backend/application/use_cases/cliente_use_cases.py

from domain.interfaces.repositories import IClienteRepository
from domain.entities.cliente import Cliente
from application.dtos.cliente_dto import ClienteCreateDTO, ClienteResponseDTO


class CriarClienteUseCase:
    """Caso de uso para criar cliente."""
    
    def __init__(self, repository: IClienteRepository):
        self.repository = repository
    
    def execute(self, dto: ClienteCreateDTO, tenant_id: str) -> ClienteResponseDTO:
        # Verifica se CNPJ já existe
        existing = self.repository.get_by_cnpj(dto.cnpj, tenant_id)
        if existing:
            raise ValueError("CNPJ já cadastrado")
        
        # Cria entidade de domínio
        cliente = Cliente(
            cnpj=CNPJ(dto.cnpj),
            razao_social=dto.razao_social,
            email=Email(dto.email) if dto.email else None,
            telefone=dto.telefone,
            endereco=dto.endereco,
            tenant_id=tenant_id
        )
        
        # Valida regras de negócio
        cliente.validate()
        
        # Persiste via repository
        created = self.repository.create(cliente)
        
        # Retorna DTO
        return ClienteResponseDTO.from_entity(created)
```

### 4. Injeção de Dependência

```python
# backend/infrastructure/container.py

from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.persistence.database import SessionLocal
from infrastructure.repositories.cliente_repository import ClienteRepository
from domain.interfaces.repositories import IClienteRepository


def get_db() -> Session:
    """Dependency: Sessão do banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cliente_repository(db: Session = Depends(get_db)) -> IClienteRepository:
    """Dependency: Repository de clientes."""
    return ClienteRepository(db)
```

### 5. Uso no Router

```python
# backend/presentation/api/clientes_router.py

from fastapi import APIRouter, Depends, HTTPException

from domain.interfaces.repositories import IClienteRepository
from application.use_cases.cliente_use_cases import CriarClienteUseCase
from application.dtos.cliente_dto import ClienteCreateDTO, ClienteResponseDTO
from infrastructure.container import get_cliente_repository, get_db

router = APIRouter(prefix="/v2/clientes", tags=["Clientes v2"])


@router.post("/", response_model=ClienteResponseDTO)
async def criar_cliente(
    dto: ClienteCreateDTO,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id)
):
    repository = ClienteRepository(db)
    use_case = CriarClienteUseCase(repository)
    
    try:
        return use_case.execute(dto, tenant_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Testes com Mock

```python
# backend/tests/unit/test_cliente_use_cases.py

import pytest
from unittest.mock import Mock, MagicMock

from domain.entities.cliente import Cliente
from domain.interfaces.repositories import IClienteRepository
from application.use_cases.cliente_use_cases import CriarClienteUseCase
from application.dtos.cliente_dto import ClienteCreateDTO


class TestCriarClienteUseCase:
    
    def setup_method(self):
        self.mock_repo = Mock(spec=IClienteRepository)
        self.use_case = CriarClienteUseCase(self.mock_repo)
    
    def test_criar_cliente_sucesso(self):
        # Arrange
        dto = ClienteCreateDTO(
            cnpj="12345678000190",
            razao_social="Empresa Teste",
            email="teste@email.com"
        )
        self.mock_repo.get_by_cnpj.return_value = None
        self.mock_repo.create.return_value = Cliente(
            id="uuid-123",
            cnpj=CNPJ("12345678000190"),
            razao_social="Empresa Teste",
            tenant_id="tenant-1"
        )
        
        # Act
        result = self.use_case.execute(dto, "tenant-1")
        
        # Assert
        assert result.razao_social == "Empresa Teste"
        self.mock_repo.create.assert_called_once()
    
    def test_criar_cliente_cnpj_duplicado(self):
        # Arrange
        dto = ClienteCreateDTO(cnpj="12345678000190", razao_social="Teste")
        self.mock_repo.get_by_cnpj.return_value = Cliente(id="existing")
        
        # Act & Assert
        with pytest.raises(ValueError, match="CNPJ já cadastrado"):
            self.use_case.execute(dto, "tenant-1")
```

## Repositórios Implementados

| Repositório | Interface | Implementação |
|-------------|-----------|---------------|
| Cliente | `IClienteRepository` | `ClienteRepository` |
| Cotação | `ICotacaoRepository` | `CotacaoRepository` |
| Pedido | `IPedidoRepository` | `PedidoRepository` |

## Próximos Passos

- [ ] Implementar repositórios para Motorista, Veículo, Entrega
- [ ] Adicionar cache no repositório (Redis)
- [ ] Implementar Unit of Work pattern
- [ ] Adicionar soft delete

## Referências

- [Repository Pattern - Martin Fowler](https://martinfowler.com/eaaCatalog/repository.html)
- [Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
