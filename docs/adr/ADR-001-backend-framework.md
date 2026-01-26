# ADR-001: Framework Backend

## Status
Proposta

## Contexto
O projeto possui um backend em Python que expõe uma API para múltiplos frontends (CRM, App Motorista, Portal Cliente e Site). A aplicação precisa suportar:

- API REST com OpenAPI/Swagger
- Autenticação (JWT + refresh)
- Integrações externas (Focus NFe, MercadoPago, WhatsApp/Evolution, ERPs, GPS, Maps)
- Background jobs (worker + scheduler)
- Multi-tenancy

O repositório já está implementado com **FastAPI** e Uvicorn.

## Decisão
Manter **FastAPI** como framework backend principal.

## Consequências
### Positivas
- Performance alta e boa ergonomia para APIs
- OpenAPI nativo, facilitando documentação e testes
- Integra bem com Pydantic (validação/DTOs)
- Boa compatibilidade com async e com `httpx`

### Negativas
- Exige disciplina de arquitetura para evitar “routers gordos” (lógica de negócio no controller)
- Ecossistema de “baterias inclusas” menor que Django (admin, ORM integrado, etc.)

## Alternativas Consideradas
- **Django + DRF**: descartado porque adicionaria esforço de migração significativo e mudaria completamente o estilo da base atual.
- **Flask**: descartado por exigir montagem manual de várias peças (OpenAPI, validação, async), e por não trazer benefícios claros vs FastAPI.
