# ADR-002: Escolha do FastAPI como Framework Backend

## Status
**Aceita**

## Data
Janeiro 2026

## Contexto

O LogiFlow CRM necessita de um backend robusto para servir múltiplas aplicações frontend (CRM, App Motorista, Portal Cliente, Site) com:

- Alta performance para operações em tempo real (GPS tracking)
- Suporte a operações assíncronas (integrações externas)
- Documentação automática de API (Swagger/OpenAPI)
- Validação de dados robusta
- Facilidade de manutenção e escalabilidade

### Requisitos Técnicos
1. API REST com JSON
2. Autenticação JWT
3. Multi-tenancy
4. Integração com PostgreSQL
5. Suporte a WebSockets (GPS em tempo real)
6. Background tasks (Celery)
7. Cache (Redis)

## Decisão

Escolhemos **FastAPI** como framework backend principal.

```python
# Stack escolhido
fastapi>=0.104.0      # Framework web assíncrono
uvicorn[standard]     # Servidor ASGI
pydantic>=2.5.0       # Validação de dados
SQLAlchemy>=2.0.0     # ORM
```

## Consequências

### Positivas

- **Performance excepcional**: Um dos frameworks Python mais rápidos (comparável a Node.js/Go)
- **Documentação automática**: Swagger UI e ReDoc gerados automaticamente
- **Validação com Pydantic**: Type hints + validação em runtime
- **Async nativo**: Suporte completo a async/await
- **Type hints**: Melhor DX e detecção de erros
- **Ecossistema maduro**: Compatível com todo ecossistema Python
- **Dependency Injection**: Sistema de DI nativo e elegante
- **Testabilidade**: Fácil de testar com pytest-asyncio

### Negativas

- **Curva de aprendizado**: Async programming pode ser complexo
- **Ecossistema menor**: Menos plugins que Django/Flask
- **Sem ORM próprio**: Necessita SQLAlchemy/Tortoise-ORM
- **Sem admin panel**: Necessita implementação própria ou terceiros

### Riscos Mitigados

| Risco | Mitigação |
|-------|-----------|
| Complexidade async | Treinamento da equipe + patterns bem definidos |
| Falta de admin | Uso de Adminer para DB + endpoints admin customizados |
| ORM externo | SQLAlchemy 2.0 com suporte async nativo |

## Alternativas Consideradas

### Django + DRF
- ✅ Ecossistema completo (ORM, Admin, Auth)
- ✅ Maturidade e documentação
- ❌ Performance inferior
- ❌ Async ainda em evolução
- ❌ Overhead para APIs simples

**Descartado por**: Performance e simplicidade eram prioridades.

### Flask + Extensions
- ✅ Simplicidade e flexibilidade
- ✅ Grande ecossistema
- ❌ Sem async nativo
- ❌ Validação manual
- ❌ Documentação manual

**Descartado por**: Falta de features nativas (validação, docs, async).

### Node.js (Express/NestJS)
- ✅ Performance excelente
- ✅ Grande ecossistema
- ❌ Mudança de linguagem (Python → JavaScript)
- ❌ Callback hell / Promises complexity
- ❌ Tipagem opcional

**Descartado por**: Equipe tem expertise em Python.

## Validação

A decisão foi validada através de:

1. **Benchmark de performance**: FastAPI 3x mais rápido que Flask
2. **POC de integração**: Todas as integrações funcionaram sem problemas
3. **Feedback da equipe**: Produtividade aumentou com type hints

## Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI vs Flask vs Django Benchmarks](https://www.techempower.com/benchmarks/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
