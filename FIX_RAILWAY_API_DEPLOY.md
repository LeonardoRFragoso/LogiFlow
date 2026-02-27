# 🔧 Corrigir Deploy do logiflow-api no Railway

## ❌ Problema Atual

O deploy do `logiflow-api` está falhando com o erro:
```
alembic upgrade head || echo Migration: 1: exec: cd: not found
```

Isso indica que há um "Pre-deploy command" configurado no Railway que está tentando executar migrações.

## ✅ Solução

### Passo 1: Acessar o Railway Dashboard

1. Acesse https://railway.app
2. Clique no projeto **LogiFlow**
3. Clique no serviço **logiflow-api**

### Passo 2: Acessar Settings

1. Clique na aba **Settings**
2. Procure pela seção **"Deploy"** ou **"Build"**

### Passo 3: Limpar Pre-deploy Command

Procure por campos como:
- **"Pre-deploy command"**
- **"Deploy command"**
- **"Run command"**
- **"Build command"**

Se houver qualquer conteúdo nesses campos (como `alembic upgrade head` ou similar):

1. **Clique no campo**
2. **Selecione todo o conteúdo** (Ctrl+A)
3. **Delete** (Delete ou Backspace)
4. Deixe o campo **completamente vazio**

### Passo 4: Salvar e Redeploy

1. Clique em **Save** (se houver botão)
2. Clique em **Redeploy** para forçar um novo deploy

### Passo 5: Aguardar Deploy

O deploy agora deve:
- ✅ Instalar dependências Python
- ✅ Iniciar o uvicorn
- ✅ **NÃO** tentar executar `alembic upgrade head`

## 📝 Notas

- As migrações podem ser executadas manualmente depois via Railway CLI:
  ```bash
  railway run alembic upgrade head
  ```
- O `Procfile` está configurado corretamente para apenas iniciar o uvicorn
- Não há nenhum arquivo no repositório que esteja causando esse erro

## 🚀 Próximos Passos

Após o deploy bem-sucedido:

1. Validar que o serviço está **Online**
2. Testar o health check: `GET /health`
3. Executar migrações manualmente se necessário

---

**Status:** Aguardando ação no Railway Dashboard
