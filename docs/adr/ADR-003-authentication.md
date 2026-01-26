# ADR-003: Estratégia de Autenticação

## Status
Proposta

## Contexto
O backend expõe endpoints para múltiplos clientes e precisa suportar autenticação e autorização. Hoje existe:

- `routers/auth.py`: JWT (via `python-jose`) + refresh token persistido
- `middleware/tenant.py`: decodificação de JWT usando `PyJWT` (biblioteca diferente)
- `middleware/rbac.py`: RBAC ainda com lógica “mock” baseada em `request.state.user`

Há necessidade de:

- mecanismo único de JWT/claims
- suporte consistente a `tenant_id` (multi-tenancy)
- padronização de autorização por roles/permissões

## Decisão
Adotar **JWT (access token) + Refresh Token persistido** como padrão, e padronizar a validação/decodificação usando **uma única biblioteca**.

- Access token curto (ex.: 15-60 min)
- Refresh token longo (ex.: 7 dias), revogável no banco
- `tenant_id` como claim obrigatória para rotas multi-tenant

## Consequências
### Positivas
- Funciona bem para SPA/PWA e múltiplos clientes
- Permite revogação e rotação de tokens
- Facilita auditoria e rate limiting por tenant/usuário

### Negativas
- Aumenta complexidade (armazenar e gerenciar refresh tokens)
- Requer cuidado com segurança (armazenamento no cliente, rotação, expiração)

## Alternativas Consideradas
- **Session/cookies server-side**: descartado por ser menos prático para múltiplos clientes e apps (SPA/PWA) e para escala horizontal.
- **OAuth2/OIDC com provedor externo**: descartado por ser overkill neste estágio (pode virar ADR futura quando houver necessidade de SSO).
