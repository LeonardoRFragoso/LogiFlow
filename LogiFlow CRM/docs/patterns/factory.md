# Factory Pattern - LogiFlow CRM

> **Status:** Implementado  
> **Camada:** Domain / Application  
> **Uso:** Criação de entidades e objetos complexos

## O que é o Factory Pattern?

O Factory Pattern encapsula a lógica de criação de objetos, centralizando a construção de instâncias complexas.

## Por que usamos?

| Benefício | Descrição |
|-----------|-----------|
| **Encapsulamento** | Lógica de criação em um lugar |
| **Consistência** | Objetos sempre criados da mesma forma |
| **Testabilidade** | Fácil de mockar criação |
| **Validação** | Regras de criação centralizadas |

## Implementação no LogiFlow

### 1. Factory para Cotações

```python
# backend/domain/factories/cotacao_factory.py

from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from domain.entities.cotacao import Cotacao
from domain.enums import StatusCotacao


class CotacaoFactory:
    """Factory para criação de Cotações."""
    
    DEFAULT_VALIDADE_DIAS = 7
    NUMERO_PREFIX = "COT"
    
    @classmethod
    def create(
        cls,
        cliente_id: str,
        origem: dict,
        destino: dict,
        peso_kg: Decimal,
        tenant_id: str,
        volumes: int = 1
    ) -> Cotacao:
        """Cria nova cotação com valores padrão."""
        now = datetime.utcnow()
        
        cotacao = Cotacao(
            id=str(uuid.uuid4()),
            numero=cls._generate_numero(tenant_id),
            cliente_id=cliente_id,
            origem=origem,
            destino=destino,
            peso_kg=peso_kg,
            volumes=volumes,
            status=StatusCotacao.PENDENTE,
            validade=now + timedelta(days=cls.DEFAULT_VALIDADE_DIAS),
            tenant_id=tenant_id,
            created_at=now
        )
        
        cotacao.validate()
        return cotacao
    
    @classmethod
    def _generate_numero(cls, tenant_id: str) -> str:
        year = datetime.utcnow().year
        return f"{cls.NUMERO_PREFIX}-{year}-{uuid.uuid4().hex[:5].upper()}"
```

### 2. Factory para Pedidos (a partir de Cotação)

```python
# backend/domain/factories/pedido_factory.py

from datetime import datetime
import uuid

from domain.entities.pedido import Pedido
from domain.entities.cotacao import Cotacao
from domain.enums import StatusPedido, StatusCotacao


class PedidoFactory:
    """Factory para criação de Pedidos."""
    
    @classmethod
    def create_from_cotacao(cls, cotacao: Cotacao) -> Pedido:
        """Cria pedido a partir de cotação aprovada."""
        if cotacao.status != StatusCotacao.APROVADA:
            raise ValueError("Apenas cotações aprovadas podem gerar pedidos")
        
        return Pedido(
            id=str(uuid.uuid4()),
            numero=f"PED-{datetime.utcnow().year}-{uuid.uuid4().hex[:5].upper()}",
            cotacao_id=cotacao.id,
            cliente_id=cotacao.cliente_id,
            origem=cotacao.origem,
            destino=cotacao.destino,
            peso_kg=cotacao.peso_kg,
            status=StatusPedido.AGUARDANDO,
            tenant_id=cotacao.tenant_id,
            created_at=datetime.utcnow()
        )
```

### 3. Uso nos Use Cases

```python
# backend/application/use_cases/cotacao_use_cases.py

from domain.factories.cotacao_factory import CotacaoFactory
from domain.factories.pedido_factory import PedidoFactory


class CriarCotacaoUseCase:
    def __init__(self, cotacao_repo, cliente_repo):
        self.cotacao_repo = cotacao_repo
        self.cliente_repo = cliente_repo
    
    def execute(self, dto, tenant_id):
        # Valida cliente existe
        cliente = self.cliente_repo.get_by_id(dto.cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        
        # Usa Factory para criar cotação
        cotacao = CotacaoFactory.create(
            cliente_id=dto.cliente_id,
            origem=dto.origem.model_dump(),
            destino=dto.destino.model_dump(),
            peso_kg=dto.peso_kg,
            tenant_id=tenant_id,
            volumes=dto.volumes
        )
        
        # Persiste
        return self.cotacao_repo.create(cotacao)


class AprovarCotacaoUseCase:
    def __init__(self, cotacao_repo, pedido_repo):
        self.cotacao_repo = cotacao_repo
        self.pedido_repo = pedido_repo
    
    def execute(self, cotacao_id, tenant_id):
        cotacao = self.cotacao_repo.get_by_id(cotacao_id)
        if not cotacao:
            raise ValueError("Cotação não encontrada")
        
        # Aprova cotação
        cotacao.aprovar()
        self.cotacao_repo.update(cotacao)
        
        # Usa Factory para criar pedido
        pedido = PedidoFactory.create_from_cotacao(cotacao)
        return self.pedido_repo.create(pedido)
```

## Factories Implementadas

| Factory | Entidade | Localização |
|---------|----------|-------------|
| `CotacaoFactory` | Cotacao | `domain/factories/` |
| `PedidoFactory` | Pedido | `domain/factories/` |
| `EntregaFactory` | Entrega | `domain/factories/` |

## Referências

- [Factory Pattern - Gang of Four](https://refactoring.guru/design-patterns/factory-method)
- [Python Factory Examples](https://realpython.com/factory-method-python/)
