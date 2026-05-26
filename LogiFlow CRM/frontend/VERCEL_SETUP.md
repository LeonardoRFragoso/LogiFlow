# Configuração do Frontend no Vercel

## Problema Identificado

O erro "Erro ao carregar leads" ocorre porque a variável de ambiente `VITE_API_URL` não está configurada no Vercel.

## Solução

### 1. Configurar Variável de Ambiente no Vercel

Acesse o painel do Vercel e configure a seguinte variável de ambiente:

**Via Dashboard:**
1. Acesse: https://vercel.com/seu-usuario/logi-flow-blush
2. Vá em **Settings** → **Environment Variables**
3. Adicione:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://logiflow-crm-production.up.railway.app`
   - **Environment:** Production, Preview, Development (marque todos)
4. Clique em **Save**

**Via CLI:**
```bash
vercel env add VITE_API_URL
# Quando solicitado, digite: https://logiflow-crm-production.up.railway.app
# Selecione: Production, Preview, Development
```

### 2. Redesploy

Após adicionar a variável de ambiente, faça um novo deploy:

```bash
vercel --prod
```

Ou simplesmente faça um novo commit/push que o Vercel irá redesploy automaticamente.

### 3. Verificar

Após o deploy, acesse a aplicação e verifique se os leads estão carregando corretamente.

## Variáveis de Ambiente Necessárias

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `VITE_API_URL` | `https://logiflow-crm-production.up.railway.app` | URL do backend API no Railway |

## CORS

O backend já está configurado para aceitar requisições do Vercel:
- `https://logi-flow-blush.vercel.app`
- `https://logi-flow-z3t5.vercel.app`
- `https://logi-flow-wuhp.vercel.app`
- `https://logi-flow-app-motorista.vercel.app`

Se você criar um novo deployment no Vercel com URL diferente, adicione-a no backend em:
`/home/leonardo/dev/LogiFlow/LogiFlow CRM/backend/config.py` → `ALLOWED_ORIGINS`

## Desenvolvimento Local

Para desenvolvimento local, crie um arquivo `.env` na raiz do frontend:

```bash
cp .env.example .env
```

E ajuste a URL para o backend local:
```
VITE_API_URL=http://localhost:8080
```
