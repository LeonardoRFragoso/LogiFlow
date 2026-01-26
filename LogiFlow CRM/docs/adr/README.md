# Architecture Decision Records (ADRs)

> Documentação das decisões arquiteturais do LogiFlow CRM

## O que são ADRs?

Architecture Decision Records são documentos curtos que capturam decisões arquiteturais importantes, incluindo o contexto, a decisão tomada, e suas consequências.

## Índice de ADRs

| ID | Título | Status | Data |
|----|--------|--------|------|
| [ADR-001](ADR-001-integracao-suitecrm.md) | Integração com SuiteCRM | **Obsoleta** | 2024 |
| [ADR-002](ADR-002-fastapi-backend.md) | Escolha do FastAPI como Backend | Aceita | Jan 2026 |
| [ADR-003](ADR-003-postgresql-database.md) | Escolha do PostgreSQL | Aceita | Jan 2026 |
| [ADR-004](ADR-004-jwt-authentication.md) | Estratégia de Autenticação JWT | Aceita | Jan 2026 |
| [ADR-005](ADR-005-clean-architecture.md) | Adoção de Clean Architecture | Aceita | Jan 2026 |
| [ADR-006](ADR-006-project-structure.md) | Estrutura de Pastas do Projeto | Aceita | Jan 2026 |

## Status Possíveis

- **Proposta**: Em discussão
- **Aceita**: Implementada e em uso
- **Rejeitada**: Considerada mas não adotada
- **Obsoleta**: Foi substituída por outra decisão

## Template para Novos ADRs

```markdown
# ADR-XXX: [Título da Decisão]

## Status
[Proposta | Aceita | Rejeitada | Obsoleta]

## Data
[Mês/Ano]

## Contexto
[Qual problema estamos tentando resolver?]

## Decisão
[Qual solução escolhemos?]

## Consequências

### Positivas
- [Benefício 1]
- [Benefício 2]

### Negativas
- [Trade-off 1]
- [Trade-off 2]

## Alternativas Consideradas

### [Alternativa 1]
- ✅ Prós
- ❌ Contras

**Descartado por**: [Motivo]

## Referências
- [Links relevantes]
```

## Como Criar um Novo ADR

1. Copie o template acima
2. Nomeie o arquivo como `ADR-XXX-titulo-kebab-case.md`
3. Preencha todas as seções
4. Adicione à tabela de índice neste README
5. Submeta um PR para revisão

## Princípios

1. **Imutabilidade**: ADRs aceitos não devem ser editados, apenas marcados como obsoletos
2. **Contexto**: Sempre documente o contexto e as alternativas
3. **Consequências**: Seja honesto sobre os trade-offs
4. **Referências**: Link para recursos externos relevantes
