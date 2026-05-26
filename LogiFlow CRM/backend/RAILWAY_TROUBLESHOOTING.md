# Railway Deployment - Troubleshooting 404 Error

## 🚨 Problema Atual

O backend está retornando **404 "Application not found"** no Railway, apesar dos logs mostrarem que a aplicação iniciou.

```bash
curl https://logiflow-crm-production.up.railway.app/health
# Response: 404 "Application not found"
# Header: x-railway-fallback: true
```

## Diagnóstico

O header `x-railway-fallback: true` indica que o Railway não consegue rotear as requisições para o container da aplicação.

## Possíveis Causas e Soluções

### 1. Verificar Status do Deployment no Railway

Acesse o Railway Dashboard:
1. Vá para: https://railway.app/project/logiflow-crm-production
2. Verifique se o serviço está **Active** (verde)
3. Clique no serviço backend
4. Vá em **Deployments** e verifique o status do último deploy

**Se o deploy falhou:**
- Clique no deployment falhado
- Verifique os logs de build e runtime
- Corrija os erros e faça redeploy

### 2. Verificar Variáveis de Ambiente

No Railway Dashboard, vá em **Variables** e verifique se todas estão configuradas:

**Variáveis Críticas:**
```bash
# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}  # Deve estar vinculado ao serviço PostgreSQL

# Redis
REDIS_URL=${{Redis.REDIS_URL}}  # Deve estar vinculado ao serviço Redis

# CORS - IMPORTANTE!
ALLOWED_ORIGINS=https://logi-flow-blush.vercel.app,https://logi-flow-z3t5.vercel.app,https://logi-flow-wuhp.vercel.app

# Outras variáveis necessárias
SECRET_KEY=<sua-chave-secreta>
DEBUG=False
```

### 3. Verificar Configuração do Serviço

No Railway Dashboard:
1. Clique no serviço backend
2. Vá em **Settings**
3. Verifique:
   - **Start Command:** Deve estar vazio (usa o Procfile)
   - **Root Directory:** Deve ser `/LogiFlow CRM/backend` ou vazio se o Procfile está na raiz
   - **Health Check Path:** Configure como `/health` ou `/api/v1/health`

### 4. Verificar o Procfile

O Procfile está correto:
```
release: python add_cargo_column.py && alembic upgrade head
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Mas verifique:**
- O arquivo está na raiz do projeto que o Railway está usando?
- Se o Railway está configurado com Root Directory, o Procfile deve estar lá

### 5. Verificar Logs em Tempo Real

No Railway Dashboard:
1. Clique no serviço backend
2. Vá em **Deployments**
3. Clique no deployment ativo
4. Veja os logs em tempo real

**Procure por:**
- Erros de inicialização
- Porta incorreta
- Falhas de conexão com PostgreSQL ou Redis
- Erros de importação de módulos

### 6. Testar Health Check

Depois de verificar os logs, teste:

```bash
# Teste direto
curl -v https://logiflow-crm-production.up.railway.app/health

# Deve retornar 200 OK com:
# {"status": "healthy", ...}
```

### 7. Verificar Vinculação de Serviços

No Railway Dashboard:
1. Verifique se PostgreSQL e Redis estão **vinculados** ao serviço backend
2. Vá em **Settings** > **Service Variables**
3. Deve haver referências como `${{Postgres.DATABASE_URL}}` e `${{Redis.REDIS_URL}}`

### 8. Redeploy Forçado

Se tudo estiver correto mas ainda não funcionar:

```bash
# Via CLI do Railway
railway up --service backend

# Ou no Dashboard:
# Deployments > três pontos > Redeploy
```

## Checklist de Verificação

- [ ] Serviço está Active no Railway Dashboard
- [ ] Último deployment foi bem-sucedido
- [ ] DATABASE_URL está configurado e vinculado ao PostgreSQL
- [ ] REDIS_URL está configurado e vinculado ao Redis
- [ ] ALLOWED_ORIGINS inclui todas as URLs do Vercel
- [ ] Procfile está no diretório correto
- [ ] Root Directory está configurado corretamente (se aplicável)
- [ ] Health Check Path está configurado
- [ ] Logs não mostram erros críticos
- [ ] Porta $PORT está sendo usada corretamente

## Comandos Úteis

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Listar projetos
railway list

# Vincular ao projeto
railway link

# Ver logs
railway logs

# Redeploy
railway up
```

## Próximos Passos

1. **Verifique os logs no Railway Dashboard** - Isso é crítico
2. **Confirme que DATABASE_URL e REDIS_URL estão configurados**
3. **Verifique se o serviço está realmente rodando** (não apenas em "deploying")
4. **Teste o health check** após corrigir qualquer problema
5. **Atualize ALLOWED_ORIGINS** para incluir todas as URLs do Vercel

## Informações Adicionais

- **Procfile Location:** `/home/leonardo/dev/LogiFlow/LogiFlow CRM/backend/Procfile`
- **Expected Port:** Railway fornece via variável `$PORT`
- **Health Endpoint:** `/health` (sem prefixo /api)
- **Docs Endpoint:** `/api/v1/docs` (apenas se DEBUG=True)
