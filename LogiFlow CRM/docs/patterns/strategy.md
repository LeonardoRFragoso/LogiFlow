# Strategy Pattern - LogiFlow CRM

> **Status:** Implementado  
> **Camada:** Domain / Services  
> **Uso:** Cálculo de frete, notificações, pagamentos

## O que é o Strategy Pattern?

O Strategy Pattern define uma família de algoritmos, encapsula cada um deles e os torna intercambiáveis. Permite que o algoritmo varie independentemente dos clientes que o utilizam.

## Por que usamos?

| Benefício | Descrição |
|-----------|-----------|
| **Flexibilidade** | Trocar algoritmos em runtime |
| **Open/Closed** | Adicionar estratégias sem modificar código existente |
| **Testabilidade** | Cada estratégia testada isoladamente |
| **Single Responsibility** | Uma classe por algoritmo |

## Implementação no LogiFlow

### 1. Strategy para Cálculo de Frete

```python
# backend/domain/strategies/frete_strategy.py

from abc import ABC, abstractmethod
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class FreteInput:
    """Dados para cálculo de frete."""
    peso_kg: Decimal
    distancia_km: Decimal
    valor_mercadoria: Decimal
    volumes: int


@dataclass
class FreteResult:
    """Resultado do cálculo de frete."""
    valor: Decimal
    prazo_dias: int
    transportadora: str


class FreteStrategy(ABC):
    """Interface para estratégias de cálculo de frete."""
    
    @abstractmethod
    def calcular(self, input: FreteInput) -> FreteResult:
        """Calcula o frete."""
        pass
    
    @abstractmethod
    def nome(self) -> str:
        """Nome da estratégia."""
        pass


class FreteExpressoStrategy(FreteStrategy):
    """Frete expresso - mais caro, mais rápido."""
    
    TAXA_KG = Decimal("2.50")
    TAXA_KM = Decimal("0.80")
    
    def calcular(self, input: FreteInput) -> FreteResult:
        valor = (input.peso_kg * self.TAXA_KG) + (input.distancia_km * self.TAXA_KM)
        return FreteResult(
            valor=valor,
            prazo_dias=2,
            transportadora="LogiFlow Expresso"
        )
    
    def nome(self) -> str:
        return "Expresso"


class FreteEconomicoStrategy(FreteStrategy):
    """Frete econômico - mais barato, mais lento."""
    
    TAXA_KG = Decimal("1.20")
    TAXA_KM = Decimal("0.40")
    
    def calcular(self, input: FreteInput) -> FreteResult:
        valor = (input.peso_kg * self.TAXA_KG) + (input.distancia_km * self.TAXA_KM)
        return FreteResult(
            valor=valor,
            prazo_dias=7,
            transportadora="LogiFlow Econômico"
        )
    
    def nome(self) -> str:
        return "Econômico"


class MelhorEnvioStrategy(FreteStrategy):
    """Frete via Melhor Envio API."""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def calcular(self, input: FreteInput) -> FreteResult:
        response = self.api_client.calcular(
            peso=float(input.peso_kg),
            valor=float(input.valor_mercadoria)
        )
        return FreteResult(
            valor=Decimal(str(response['price'])),
            prazo_dias=response['delivery_time'],
            transportadora=response['carrier']
        )
    
    def nome(self) -> str:
        return "Melhor Envio"
```

### 2. Contexto que usa as Strategies

```python
# backend/services/frete_calculator.py

from typing import List
from domain.strategies.frete_strategy import FreteStrategy, FreteInput, FreteResult


class FreteCalculator:
    """Calculadora de frete que usa múltiplas strategies."""
    
    def __init__(self, strategies: List[FreteStrategy]):
        self.strategies = strategies
    
    def calcular_todos(self, input: FreteInput) -> List[FreteResult]:
        """Calcula frete com todas as strategies disponíveis."""
        resultados = []
        for strategy in self.strategies:
            try:
                resultado = strategy.calcular(input)
                resultados.append(resultado)
            except Exception as e:
                # Log error, continue with other strategies
                pass
        return resultados
    
    def calcular_mais_barato(self, input: FreteInput) -> FreteResult:
        """Retorna a opção mais barata."""
        resultados = self.calcular_todos(input)
        return min(resultados, key=lambda r: r.valor)
    
    def calcular_mais_rapido(self, input: FreteInput) -> FreteResult:
        """Retorna a opção mais rápida."""
        resultados = self.calcular_todos(input)
        return min(resultados, key=lambda r: r.prazo_dias)
```

### 3. Strategy para Notificações

```python
# backend/domain/strategies/notification_strategy.py

from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    """Interface para estratégias de notificação."""
    
    @abstractmethod
    async def send(self, to: str, message: str) -> bool:
        pass


class EmailNotificationStrategy(NotificationStrategy):
    """Notificação via Email."""
    
    def __init__(self, smtp_service):
        self.smtp = smtp_service
    
    async def send(self, to: str, message: str) -> bool:
        return await self.smtp.send_email(to, "LogiFlow", message)


class WhatsAppNotificationStrategy(NotificationStrategy):
    """Notificação via WhatsApp."""
    
    def __init__(self, whatsapp_service):
        self.wa = whatsapp_service
    
    async def send(self, to: str, message: str) -> bool:
        return await self.wa.send_message(to, message)


class SMSNotificationStrategy(NotificationStrategy):
    """Notificação via SMS."""
    
    def __init__(self, sms_service):
        self.sms = sms_service
    
    async def send(self, to: str, message: str) -> bool:
        return await self.sms.send_sms(to, message)


class NotificationService:
    """Serviço que usa strategies de notificação."""
    
    def __init__(self, strategies: List[NotificationStrategy]):
        self.strategies = strategies
    
    async def notify_all(self, recipients: dict, message: str):
        """Notifica por todos os canais disponíveis."""
        for strategy in self.strategies:
            channel = strategy.__class__.__name__
            recipient = recipients.get(channel)
            if recipient:
                await strategy.send(recipient, message)
```

### 4. Uso no Router

```python
# backend/routers/cotacao_automatica.py

from domain.strategies.frete_strategy import (
    FreteExpressoStrategy,
    FreteEconomicoStrategy,
    FreteInput
)
from services.frete_calculator import FreteCalculator


@router.post("/calcular")
async def calcular_frete(data: FreteCalcularDTO):
    # Configura strategies
    strategies = [
        FreteExpressoStrategy(),
        FreteEconomicoStrategy(),
    ]
    
    calculator = FreteCalculator(strategies)
    
    input_data = FreteInput(
        peso_kg=data.peso_kg,
        distancia_km=data.distancia_km,
        valor_mercadoria=data.valor_mercadoria,
        volumes=data.volumes
    )
    
    # Calcula com todas as strategies
    resultados = calculator.calcular_todos(input_data)
    
    return {"opcoes": resultados}
```

## Strategies Implementadas

| Strategy | Interface | Uso |
|----------|-----------|-----|
| `FreteExpressoStrategy` | `FreteStrategy` | Cálculo de frete expresso |
| `FreteEconomicoStrategy` | `FreteStrategy` | Cálculo de frete econômico |
| `MelhorEnvioStrategy` | `FreteStrategy` | Integração Melhor Envio |
| `EmailNotificationStrategy` | `NotificationStrategy` | Notificações por e-mail |
| `WhatsAppNotificationStrategy` | `NotificationStrategy` | Notificações por WhatsApp |

## Referências

- [Strategy Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/strategy)
- [Strategy Pattern in Python](https://realpython.com/strategy-pattern-python/)
