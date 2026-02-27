# 🚀 Como Executar Migrations no Railway

## Problema Encontrado

O banco de dados do Railway (`logiflow-db.railway.internal`) não é acessível de fora da rede interna do Railway. Portanto, as migrations precisam ser executadas **dentro do container do Railway**.

## ✅ Solução

### Opção 1: Executar via Railway CLI (Recomendado)

1. **Linkar o projeto (já feito):**
   ```bash
   cd "LogiFlow CRM/backend"
   railway link
   # Selecionar: luminous-heart > production > logiflow-api
   ```

2. **Executar migrations dentro do container:**
   ```bash
   railway run alembic upgrade head
   ```

### Opção 2: Executar via Deploy Hook

Adicionar ao `Procfile` ou `railway.json` um comando que execute as migrations antes de iniciar a aplicação:

```yaml
# railway.json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "startCommand": "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

### Opção 3: Executar via SSH no Railway

1. **Conectar ao container:**
   ```bash
   railway shell
   ```

2. **Executar migrations:**
   ```bash
   cd /app
   alembic upgrade head
   ```

## 📋 Passos Recomendados

### 1. Verificar Variáveis de Ambiente

```bash
railway variables
```

Deve conter:
- `DATABASE_URL` - URL do PostgreSQL
- `PYTHONUNBUFFERED=1`

### 2. Executar Migrations

```bash
cd "LogiFlow CRM/backend"
railway run alembic upgrade head
```

### 3. Verificar Status

```bash
railway run alembic current
railway run alembic history
```

### 4. Se Houver Erro

Verificar logs:
```bash
railway logs
```

## 🔍 Diagnóstico

### Verificar Conectividade

```bash
railway run psql $DATABASE_URL -c "SELECT version();"
```

### Verificar Migrations Pendentes

```bash
railway run alembic upgrade head --sql
```

Isso mostra o SQL que será executado sem realmente executar.

## 📝 Checklist

- [ ] Railway CLI instalado (`railway --version`)
- [ ] Projeto linkado (`railway project list`)
- [ ] Variáveis de ambiente configuradas (`railway variables`)
- [ ] Migrations executadas (`railway run alembic upgrade head`)
- [ ] Status verificado (`railway run alembic current`)
- [ ] Logs verificados (`railway logs`)

## ⚠️ Importante

**NÃO execute as migrations localmente** pois o banco local não está configurado. Execute sempre no Railway onde o banco está disponível.

## 🎯 Próximas Ações

1. ✅ Executar: `railway run alembic upgrade head`
2. ✅ Verificar: `railway run alembic current`
3. ✅ Testar fluxo completo
4. ✅ Deploy em produção

---

**Status:** Pronto para executar migrations no Railway
**Data:** 27 de Fevereiro de 2026
**Comando:** `railway run alembic upgrade head`
