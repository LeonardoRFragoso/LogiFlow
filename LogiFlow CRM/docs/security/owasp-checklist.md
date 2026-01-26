# LogiFlow CRM - OWASP Top 10 Checklist

> Checklist de segurança baseado no OWASP Top 10 (2021)

## Status Geral

| # | Vulnerabilidade | Status | Implementação |
|---|-----------------|--------|---------------|
| A01 | Broken Access Control | ✅ Mitigado | Multi-tenancy + RBAC |
| A02 | Cryptographic Failures | ✅ Mitigado | HTTPS + bcrypt + JWT |
| A03 | Injection | ✅ Mitigado | SQLAlchemy ORM + Pydantic |
| A04 | Insecure Design | ✅ Mitigado | Clean Architecture |
| A05 | Security Misconfiguration | ✅ Mitigado | Environment variables |
| A06 | Vulnerable Components | ⚠️ Monitorado | Dependabot + audits |
| A07 | Auth Failures | ✅ Mitigado | JWT + Rate limiting |
| A08 | Data Integrity Failures | ✅ Mitigado | Input validation |
| A09 | Logging Failures | ✅ Mitigado | Loguru + correlation ID |
| A10 | Server-Side Request Forgery | ✅ Mitigado | URL validation |

---

## A01: Broken Access Control

### Implementações

1. **Multi-tenancy Isolation**
   ```python
   # Middleware que injeta tenant_id em todas as queries
   class TenantMiddleware:
       async def __call__(self, request, call_next):
           tenant_id = get_tenant_from_token(request)
           request.state.tenant_id = tenant_id
           return await call_next(request)
   ```

2. **Role-Based Access Control (RBAC)**
   ```python
   # Decorator para verificar permissões
   @require_role(["admin", "operador"])
   async def criar_cliente(...):
       pass
   ```

3. **Row-Level Security**
   - Todas as queries filtram por `tenant_id`
   - Usuários só acessam dados do próprio tenant

### Testes
- [x] Usuário não acessa dados de outro tenant
- [x] Motorista não acessa rotas de admin
- [x] Token expirado é rejeitado

---

## A02: Cryptographic Failures

### Implementações

1. **HTTPS obrigatório em produção**
   ```python
   # Redirect HTTP → HTTPS via Nginx/Load Balancer
   ```

2. **Senhas com bcrypt**
   ```python
   from passlib.context import CryptContext
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   ```

3. **Tokens JWT assinados**
   ```python
   SECRET_KEY = os.getenv("SECRET_KEY")  # 256-bit
   ALGORITHM = "HS256"
   ```

4. **Secrets em variáveis de ambiente**
   - Nunca commitados no código
   - `.env.example` com placeholders

### Checklist
- [x] HTTPS em produção
- [x] Senhas hasheadas com bcrypt
- [x] JWT com secret seguro
- [x] Sem secrets no código

---

## A03: Injection

### Implementações

1. **SQLAlchemy ORM** (previne SQL Injection)
   ```python
   # ✅ Seguro
   db.query(Cliente).filter_by(cnpj=cnpj).first()
   
   # ❌ Vulnerável (nunca fazer)
   db.execute(f"SELECT * FROM clientes WHERE cnpj = '{cnpj}'")
   ```

2. **Pydantic Validation** (previne input malicioso)
   ```python
   class ClienteCreateDTO(BaseModel):
       cnpj: str = Field(..., regex=r'^\d{14}$')
       email: EmailStr
   ```

3. **Escape de HTML** (previne XSS)
   - Vue.js escapa automaticamente
   - Usar `v-html` apenas com dados sanitizados

### Checklist
- [x] Todas as queries via ORM
- [x] Input validado com Pydantic
- [x] Output escapado no frontend

---

## A04: Insecure Design

### Implementações

1. **Clean Architecture**
   - Separação de responsabilidades
   - Validação em múltiplas camadas

2. **Threat Modeling**
   - Identificação de assets críticos
   - Análise de riscos

3. **Princípio do Menor Privilégio**
   - Usuários têm apenas permissões necessárias
   - Tokens com escopo limitado

---

## A05: Security Misconfiguration

### Implementações

1. **Variáveis de ambiente**
   ```bash
   # .env.example (commitado)
   SECRET_KEY=change-me-in-production
   DATABASE_URL=postgresql://user:pass@localhost/db
   
   # .env (não commitado)
   SECRET_KEY=<valor-real-seguro>
   ```

2. **Headers de segurança**
   ```python
   # Configurado no Nginx/CDN
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   X-XSS-Protection: 1; mode=block
   ```

3. **Debug desabilitado em produção**
   ```python
   DEBUG = os.getenv("DEBUG", "false").lower() == "true"
   ```

### Checklist
- [x] DEBUG=false em produção
- [x] Swagger desabilitado em produção
- [x] CORS configurado restritivamente
- [x] Headers de segurança

---

## A06: Vulnerable and Outdated Components

### Implementações

1. **Dependabot** (GitHub)
   - Alerts automáticos de vulnerabilidades
   - PRs automáticos de atualização

2. **Audits regulares**
   ```bash
   # Python
   pip-audit
   safety check
   
   # Node.js
   npm audit
   ```

3. **Trivy** (scan de containers)
   ```yaml
   # CI/CD
   - name: Security Scan
     uses: aquasecurity/trivy-action@master
   ```

---

## A07: Identification and Authentication Failures

### Implementações

1. **Rate Limiting**
   ```python
   # 5 tentativas de login por minuto
   @limiter.limit("5/minute")
   async def login(credentials):
       pass
   ```

2. **Password Policy**
   ```python
   # Mínimo 8 caracteres, 1 maiúscula, 1 número, 1 especial
   PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
   ```

3. **Token Expiration**
   - Access token: 15 minutos
   - Refresh token: 7 dias
   - Logout invalida refresh token

### Checklist
- [x] Rate limiting em login
- [x] Política de senha forte
- [x] Tokens com expiração curta
- [x] Logout funcional

---

## A08: Software and Data Integrity Failures

### Implementações

1. **Input Validation**
   - Pydantic em todas as entradas
   - Validação de tipos e formatos

2. **CI/CD Seguro**
   - Secrets em GitHub Secrets
   - Builds em ambiente isolado

3. **Checksums**
   - Verificação de integridade de arquivos

---

## A09: Security Logging and Monitoring Failures

### Implementações

1. **Logging estruturado**
   ```python
   from loguru import logger
   
   logger.info("Login realizado", user_id=user.id, ip=request.client.host)
   logger.warning("Tentativa de acesso negada", resource="/admin", user_id=user.id)
   ```

2. **Correlation ID**
   ```python
   # Cada request tem ID único para rastreamento
   X-Correlation-ID: 550e8400-e29b-41d4-a716-446655440000
   ```

3. **Eventos de segurança logados**
   - Login/logout
   - Falhas de autenticação
   - Acesso negado
   - Modificações em dados sensíveis

---

## A10: Server-Side Request Forgery (SSRF)

### Implementações

1. **Validação de URLs**
   ```python
   ALLOWED_HOSTS = ["api.mercadopago.com", "api.focusnfe.com.br"]
   
   def validate_external_url(url: str) -> bool:
       parsed = urlparse(url)
       return parsed.hostname in ALLOWED_HOSTS
   ```

2. **Whitelist de IPs/hosts**
   - Apenas hosts conhecidos permitidos
   - Bloqueio de IPs internos (127.0.0.1, 10.x.x.x)

---

## Referências

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
