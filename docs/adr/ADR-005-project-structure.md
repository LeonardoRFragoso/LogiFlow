# ADR-005: Estrutura de Pastas e Arquitetura em Camadas

## Status
Proposta

## Contexto
O backend está hoje concentrado em:

- `routers/` (HTTP)
- `services/` (lógica e integrações)
- `integrations/` (clientes externos)
- `models.py`/`models/` (persistência)

Isso funciona, mas dificulta:

- evolução incremental para Clean Architecture
- organização de testes espelhando camadas
- controle de dependências (evitar routers chamando ORM direto)

## Decisão
Evoluir para **Layered/Clean Architecture** com a seguinte estrutura alvo (incremental):

- `/src/domain`
  - entidades, regras de negócio, interfaces (ports)
- `/src/application`
  - casos de uso (use cases), serviços de aplicação, DTOs de entrada/saída
- `/src/infrastructure`
  - repos SQLAlchemy, implementações de integrações externas, providers
- `/src/presentation`
  - controllers/routers FastAPI, schemas HTTP, wiring de DI
- `/src/shared`
  - cross-cutting (logging, config, utils comuns)

> Migração será gradual, mantendo compatibilidade até completar.

## Consequências
### Positivas
- Dependências ficam mais claras e controladas
- Facilita testes unitários vs integração
- Facilita evolução para microserviços no futuro (se necessário)

### Negativas
- Refatoração inicial pode ser extensa
- Necessita ajustes de imports e entrypoints

## Alternativas Consideradas
- **Manter estrutura atual**: descartado por manter o acoplamento alto e dificultar testes e governança de arquitetura.
- **Monolito modular sem camadas**: descartado porque não resolve o problema de dependências e responsabilidades misturadas.
