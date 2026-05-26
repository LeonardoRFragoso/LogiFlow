# 🚨 URGENTE - Corrigir CORS no Railway

## Erro Atual

```
Access to fetch at 'https://logiflow-api-production-3447.up.railway.app/api/v1/admin/leads/'
from origin 'https://logi-flow-blush.vercel.app' has been blocked by CORS policy:
Response to preflight request doesn't pass access control check:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## Causa

O backend no Railway **NÃO está configurado** para aceitar requisições do frontend Vercel.

## ✅ Solução Imediata

### 1. Acessar Railway Dashboard

1. Vá para: https://railway.app
2. Selecione o projeto `luminous-heart`
3. Clique no serviço **`logiflow-api`**
4. Vá em **Variables**

### 2. Adicionar/Atualizar Variável ALLOWED_ORIGINS

**Adicione ou edite a variável:**

**Nome da Variável:**
```
ALLOWED_ORIGINS
```

**Valor da Variável:**
```
https://logi-flow-blush.vercel.app,https://logi-flow-z3t5.vercel.app,https://logi-flow-wuhp.vercel.app,https://logi-flow-app-motorista.vercel.app,http://localhost:3000,http://localhost:8080
```

### 3. Salvar e Redeploy

1. Clique em **Add Variable** ou **Save**
2. O Railway vai fazer **redeploy automático**
3. Aguarde o deploy completar (1-2 minutos)

### 4. Verificar

Após o redeploy, teste:

```bash
curl -H "Origin: https://logi-flow-blush.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: authorization,content-type" \
     -X OPTIONS \
     https://logiflow-api-production-3447.up.railway.app/api/v1/admin/leads/ \
     -v 2>&1 | grep -i "access-control"
```

Deve retornar headers como:
```
access-control-allow-origin: https://logi-flow-blush.vercel.app
access-control-allow-credentials: true
access-control-allow-methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
```

## 📋 Checklist

- [ ] Acessei Railway Dashboard
- [ ] Selecionei o serviço `logiflow-api`
- [ ] Fui em Variables
- [ ] Adicionei/editei `ALLOWED_ORIGINS` com todas as URLs do Vercel
- [ ] Salvei a variável
- [ ] Aguardei o redeploy completar
- [ ] Testei o frontend - leads carregam corretamente

## 🔍 Configuração Atual vs Necessária

### ❌ Configuração Atual (código)
```python
# config.py linha 18
ALLOWED_ORIGINS = "http://localhost:3000,http://localhost:8080,https://logi-flow-blush.vercel.app"
```

### ✅ Configuração Necessária (Railway)
```
ALLOWED_ORIGINS=https://logi-flow-blush.vercel.app,https://logi-flow-z3t5.vercel.app,https://logi-flow-wuhp.vercel.app,https://logi-flow-app-motorista.vercel.app,http://localhost:3000,http://localhost:8080
```

## ⚠️ Importante

- A variável de ambiente no Railway **sobrescreve** o valor padrão do código
- Sem essa variável configurada, o Railway usa apenas o valor padrão do `config.py`
- O valor padrão inclui apenas `https://logi-flow-blush.vercel.app`, mas pode estar desatualizado

## 🎯 Resultado Esperado

Após configurar corretamente:
- ✅ Frontend carrega leads sem erro
- ✅ Estatísticas aparecem corretamente
- ✅ Todas as requisições funcionam
- ✅ Sem erros de CORS no console

## 📞 Se Ainda Não Funcionar

1. Verifique se o redeploy completou com sucesso
2. Verifique os logs do Railway para erros
3. Limpe o cache do navegador (Ctrl+Shift+R)
4. Teste em aba anônima
5. Verifique se a variável foi salva corretamente no Railway

## 🔗 Links Úteis

- Railway Dashboard: https://railway.app
- Projeto: luminous-heart
- Serviço: logiflow-api
- Frontend: https://logi-flow-blush.vercel.app
