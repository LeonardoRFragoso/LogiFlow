# LogiFlow CRM - Secrets Management

> Guia de gerenciamento de secrets e variáveis sensíveis

## Princípios

1. **Nunca commitar secrets** no repositório
2. **Usar variáveis de ambiente** para todos os secrets
3. **Rotacionar secrets** periodicamente
4. **Limitar acesso** a quem realmente precisa

---

## Variáveis de Ambiente

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/logiflow
DATABASE_URL_TEST=postgresql://user:password@host:5432/logiflow_test

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# JWT
SECRET_KEY=your-256-bit-secret-key
JWT_ALGORITHM=HS256

# External APIs
MERCADOPAGO_ACCESS_TOKEN=your-mercadopago-token
FOCUS_NFE_TOKEN=your-focus-nfe-token
WHATSAPP_API_TOKEN=your-whatsapp-token
GOOGLE_MAPS_API_KEY=your-google-maps-key
MELHOR_ENVIO_TOKEN=your-melhor-envio-token

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=<YOUR_APP_PASSWORD_HERE>

# Environment
DEBUG=false
ENVIRONMENT=production
```

### Frontend (.env)

```bash
VITE_API_URL=https://api.logiflow.com.br
VITE_GOOGLE_MAPS_KEY=your-public-maps-key
```

---

## Configuração por Ambiente

### Local (Desenvolvimento)

```bash
# Copiar template
cp .env.example .env

# Editar com valores locais
nano .env
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
  REDIS_PASSWORD: ${{ secrets.REDIS_PASSWORD }}
```

**Configurar em:** GitHub → Settings → Secrets and variables → Actions

### Produção (Render.com)

1. Acesse Dashboard → Environment
2. Adicione cada variável manualmente
3. Marque como "Secret" quando aplicável

---

## Geração de Secrets

### SECRET_KEY (JWT)

```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32
```

### Senhas de Banco

```bash
# Gerar senha aleatória
openssl rand -base64 24
```

---

## Rotação de Secrets

### Quando Rotacionar

- [ ] A cada 90 dias (recomendado)
- [ ] Quando um funcionário sai
- [ ] Após suspeita de vazamento
- [ ] Após incidente de segurança

### Processo de Rotação

1. **Gerar novo secret**
2. **Atualizar em todos os ambientes**
3. **Testar aplicação**
4. **Invalidar secret antigo**

### Rotação de JWT Secret

```python
# Suportar múltiplos secrets durante transição
JWT_SECRETS = [
    os.getenv("SECRET_KEY"),      # Novo
    os.getenv("SECRET_KEY_OLD"),  # Antigo (aceito por 24h)
]

def verify_token(token: str):
    for secret in JWT_SECRETS:
        try:
            return jwt.decode(token, secret, algorithms=[ALGORITHM])
        except JWTError:
            continue
    raise HTTPException(status_code=401)
```

---

## Verificação de Vazamentos

### Git-secrets

```bash
# Instalar
brew install git-secrets

# Configurar
git secrets --install
git secrets --register-aws

# Verificar histórico
git secrets --scan-history
```

### Padrões a Detectar

```bash
# .gitallowed (padrões permitidos - falsos positivos)
# Nenhum por enquanto

# Padrões bloqueados (adicionar ao git-secrets)
git secrets --add 'password\s*=\s*.+'
git secrets --add 'api_key\s*=\s*.+'
git secrets --add 'secret\s*=\s*.+'
```

---

## Checklist de Segurança

### Antes de Commit

- [ ] Nenhum secret hardcoded
- [ ] `.env` está no `.gitignore`
- [ ] Apenas `.env.example` commitado
- [ ] Senhas não estão em logs

### Antes de Deploy

- [ ] Secrets configurados no ambiente
- [ ] DEBUG=false
- [ ] HTTPS habilitado
- [ ] Logs não expõem secrets

### Periodicamente

- [ ] Audit de dependências
- [ ] Rotação de secrets (90 dias)
- [ ] Review de acessos
- [ ] Scan de vazamentos

---

## Arquivos Sensíveis

### .gitignore

```gitignore
# Environment
.env
.env.local
.env.*.local

# Secrets
*.pem
*.key
secrets/
credentials/

# Logs (podem conter dados sensíveis)
logs/
*.log
```

### Nunca Commitar

- Arquivos `.env` com valores reais
- Chaves privadas (`.pem`, `.key`)
- Certificados SSL
- Dumps de banco de dados
- Backups

---

## Referências

- [12 Factor App - Config](https://12factor.net/config)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
