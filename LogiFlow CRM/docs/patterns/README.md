# Design Patterns - LogiFlow CRM

> Documentação dos padrões de design implementados no projeto

## Padrões Implementados

| Padrão | Status | Camada | Documentação |
|--------|--------|--------|--------------|
| **Repository** | ✅ Implementado | Infrastructure | [repository.md](repository.md) |
| **Dependency Injection** | ✅ Implementado | Infrastructure | [dependency-injection.md](dependency-injection.md) |
| **DTO** | ✅ Implementado | Application | [dto.md](dto.md) |
| **Factory** | ✅ Implementado | Domain | [factory.md](factory.md) |
| **Strategy** | ✅ Implementado | Domain/Services | [strategy.md](strategy.md) |

## Diagrama de Padrões por Camada

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  • DTOs (entrada/saída)                                      │
│  • Dependency Injection (FastAPI Depends)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  • Use Cases                                                 │
│  • DTOs (transformação)                                      │
│  • Factory (criação de responses)                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                            │
│  • Entities                                                  │
│  • Value Objects                                             │
│  • Factory (criação de entidades)                            │
│  • Strategy (algoritmos de negócio)                          │
│  • Repository Interfaces                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                       │
│  • Repository (implementações)                               │
│  • Dependency Injection Container                            │
│  • External Services                                         │
└─────────────────────────────────────────────────────────────┘
```

## Quando Usar Cada Padrão

| Padrão | Quando Usar |
|--------|-------------|
| **Repository** | Acesso a dados, queries complexas |
| **Dependency Injection** | Desacoplar dependências, facilitar testes |
| **DTO** | Transferir dados entre camadas, validação |
| **Factory** | Criação de objetos complexos, regras de criação |
| **Strategy** | Algoritmos intercambiáveis, múltiplas implementações |

## Princípios SOLID Aplicados

- **S** - Single Responsibility: Cada padrão tem uma responsabilidade clara
- **O** - Open/Closed: Strategy permite adicionar novos algoritmos
- **L** - Liskov Substitution: Interfaces respeitadas pelas implementações
- **I** - Interface Segregation: Interfaces específicas por domínio
- **D** - Dependency Inversion: Dependemos de abstrações, não de implementações

## Referências

- [Design Patterns - Gang of Four](https://refactoring.guru/design-patterns)
- [Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Design Patterns](https://python-patterns.guide/)
