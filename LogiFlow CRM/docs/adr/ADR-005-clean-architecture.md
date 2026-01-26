# ADR-005: Adoção de Clean Architecture

## Status
**Aceita** (Parcialmente Implementada)

## Data
Janeiro 2026

## Contexto

O LogiFlow CRM cresceu organicamente e apresenta:

- Lógica de negócio espalhada em routers e services
- Acoplamento direto com frameworks (FastAPI, SQLAlchemy)
- Dificuldade em testar regras de negócio isoladamente
- Código duplicado entre módulos similares

### Problemas Identificados
1. Routers com 500+ linhas misturando HTTP e lógica de negócio
2. Services acoplados diretamente ao SQLAlchemy
3. Ausência de entidades de domínio puras
4. Testes requerem banco de dados real

## Decisão

Adotamos **Clean Architecture** (Uncle Bob) com as seguintes camadas:

```
backend/
├── domain/           # Entidades e regras de negócio (PURO)
├── application/      # Use Cases e DTOs
├── infrastructure/   # Implementações técnicas
└── presentation/     # API endpoints
```

### Regra de Dependência

```
Presentation → Application → Domain ← Infrastructure
```

A camada de domínio não conhece nada sobre as outras camadas.

## Consequências

### Positivas

- **Testabilidade**: Domínio testável sem frameworks
- **Manutenibilidade**: Mudanças isoladas por camada
- **Flexibilidade**: Trocar banco/framework sem afetar negócio
- **Clareza**: Separação clara de responsabilidades
- **Reusabilidade**: Use cases reutilizáveis
- **Onboarding**: Estrutura previsível para novos devs

### Negativas

- **Complexidade inicial**: Mais arquivos e boilerplate
- **Overhead**: Mapeamento entre camadas
- **Curva de aprendizado**: Equipe precisa entender o padrão
- **Migração gradual**: Sistema legado coexiste temporariamente

### Riscos Mitigados

| Risco | Mitigação |
|-------|-----------|
| Over-engineering | Aplicar apenas onde há complexidade |
| Inconsistência | Guias e templates documentados |
| Resistência da equipe | Treinamento + exemplos práticos |

## Implementação

### Estrutura de Pastas

```
backend/
├── domain/
│   ├── entities/
│   │   ├── base.py           # Entity base class
│   │   ├── cliente.py        # Cliente entity
│   │   ├── cotacao.py        # Cotacao entity
│   │   └── pedido.py         # Pedido entity
│   ├── value_objects/
│   │   ├── cnpj.py           # CNPJ value object
│   │   ├── email.py          # Email value object
│   │   └── money.py          # Money value object
│   ├── interfaces/
│   │   └── repositories.py   # Repository interfaces
│   └── exceptions/
│       └── domain_exceptions.py
│
├── application/
│   ├── use_cases/
│   │   ├── cliente_use_cases.py
│   │   └── cotacao_use_cases.py
│   └── dtos/
│       ├── cliente_dto.py
│       ├── cotacao_dto.py
│       └── pedido_dto.py
│
├── infrastructure/
│   ├── repositories/
│   │   ├── cliente_repository.py
│   │   ├── cotacao_repository.py
│   │   └── pedido_repository.py
│   ├── persistence/
│   │   └── database.py
│   └── container.py          # DI Container
│
└── presentation/
    └── api/
        ├── clientes_router.py
        ├── cotacoes_router.py
        └── pedidos_router.py
```

### Exemplo de Implementação

#### Domain Entity
```python
# domain/entities/cliente.py
from dataclasses import dataclass
from typing import Optional
from domain.value_objects import CNPJ, Email

@dataclass
class Cliente:
    id: Optional[str] = None
    cnpj: CNPJ = None
    razao_social: str = ""
    email: Email = None
    tenant_id: str = ""
    
    def validate(self) -> bool:
        if not self.cnpj or not self.cnpj.is_valid():
            raise ValueError("CNPJ inválido")
        if not self.razao_social:
            raise ValueError("Razão social obrigatória")
        return True
```

#### Repository Interface
```python
# domain/interfaces/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Cliente

class IClienteRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def list(self, tenant_id: str, skip: int, limit: int) -> List[Cliente]:
        pass
    
    @abstractmethod
    def create(self, cliente: Cliente) -> Cliente:
        pass
    
    @abstractmethod
    def update(self, cliente: Cliente) -> Cliente:
        pass
```

#### Use Case
```python
# application/use_cases/cliente_use_cases.py
from domain.interfaces import IClienteRepository
from domain.entities import Cliente
from application.dtos import ClienteCreateDTO, ClienteResponseDTO

class CriarClienteUseCase:
    def __init__(self, repository: IClienteRepository):
        self.repository = repository
    
    def execute(self, dto: ClienteCreateDTO, tenant_id: str) -> ClienteResponseDTO:
        cliente = Cliente(
            cnpj=CNPJ(dto.cnpj),
            razao_social=dto.razao_social,
            email=Email(dto.email),
            tenant_id=tenant_id
        )
        cliente.validate()
        
        created = self.repository.create(cliente)
        return ClienteResponseDTO.from_entity(created)
```

#### Repository Implementation
```python
# infrastructure/repositories/cliente_repository.py
from domain.interfaces import IClienteRepository
from domain.entities import Cliente
from sqlalchemy.orm import Session
from models import ClienteModel

class ClienteRepository(IClienteRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: str) -> Optional[Cliente]:
        model = self.db.query(ClienteModel).filter_by(id=id).first()
        return self._to_entity(model) if model else None
    
    def create(self, cliente: Cliente) -> Cliente:
        model = ClienteModel(**cliente.__dict__)
        self.db.add(model)
        self.db.commit()
        return self._to_entity(model)
    
    def _to_entity(self, model: ClienteModel) -> Cliente:
        return Cliente(
            id=model.id,
            cnpj=CNPJ(model.cnpj),
            razao_social=model.razao_social,
            email=Email(model.email),
            tenant_id=model.tenant_id
        )
```

## Estratégia de Migração

### Fase 1: Estrutura (Completa)
- [x] Criar estrutura de pastas
- [x] Implementar para Cliente, Cotação, Pedido
- [x] Configurar DI Container

### Fase 2: Migração Gradual (Em Andamento)
- [ ] Migrar routers restantes incrementalmente
- [ ] Priorizar módulos com mais lógica de negócio
- [ ] Manter retrocompatibilidade

### Fase 3: Consolidação (Futuro)
- [ ] Remover código legado
- [ ] Unificar padrões
- [ ] Documentar guias

## Alternativas Consideradas

### Hexagonal Architecture (Ports & Adapters)
- ✅ Similar em benefícios
- ✅ Foco em ports/adapters
- ❌ Nomenclatura menos intuitiva
- ❌ Menos material de referência

**Considerado equivalente**: Pode ser usado intercambiavelmente.

### CQRS (Command Query Responsibility Segregation)
- ✅ Separação leitura/escrita
- ✅ Escalabilidade extrema
- ❌ Complexidade significativa
- ❌ Event sourcing opcional mas comum

**Descartado por**: Over-engineering para o caso atual.

### MVC Tradicional
- ✅ Simples e conhecido
- ❌ Domínio acoplado ao framework
- ❌ Difícil testar
- ❌ Fat controllers/models

**Descartado por**: Problemas atuais do projeto são causados por MVC.

## Referências

- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [The Clean Architecture in Python](https://www.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/)
- [FastAPI Clean Architecture Example](https://github.com/fastapi-practices/fastapi_best_architecture)
