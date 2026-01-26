# ADR-004: Padrões de Design Utilizados

## Status
Proposta

## Contexto
O código atual tem sinais de mistura de responsabilidades:

- Routers contendo regras de negócio e persistência (inclusive em memória)
- Integrações externas chamadas diretamente por endpoints
- Multi-tenancy e autorização parcialmente mockadas

Para evoluir o projeto para padrão pleno e facilitar testes/CI/CD, precisamos de:

- isolamento de acesso a dados
- contratos estáveis entre camadas
- substituição fácil de integrações externas por mocks

## Decisão
Adotar os seguintes padrões (onde aplicável):

- **Repository Pattern**: abstrair persistência (SQLAlchemy) por entidade/agregado.
- **DTOs (Pydantic)**: separar modelos de entrada/saída da API de modelos de domínio/persistência.
- **Dependency Injection (DI)**: injetar repos/services nas rotas/use cases (via FastAPI Depends e/ou container).
- **Strategy Pattern**: encapsular variações de algoritmos (ex.: múltiplos provedores GPS/ERP/Maps) sob uma interface.
- **Factory Pattern**: centralizar construção de clientes externos (ex.: FocusNFeClient por tenant, ERP clients, GPS clients).

## Consequências
### Positivas
- Testabilidade maior (mocks substituem repos e integrações)
- Código mais modular e manutenível
- Redução de acoplamento entre camada HTTP e camada de negócio

### Negativas
- Aumento de quantidade de arquivos/código (mais abstrações)
- Curva de aprendizado e disciplina de arquitetura

## Alternativas Consideradas
- **Manter lógica nos routers**: descartado por dificultar testes e manutenção e por aumentar risco de regressão.
- **Service Layer sem repositories**: descartado porque a persistência continuaria vazando para a camada de aplicação.
