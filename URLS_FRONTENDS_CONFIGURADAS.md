# 🌐 URLs dos Frontends - Configuração Final

## ✅ Frontends Vercel Configurados

| Aplicação | URL | Status |
|-----------|-----|--------|
| **Frontend Principal** | `https://logi-flow-blush.vercel.app` | ✅ Ativo |
| **App Motorista** | `https://logi-flow-app-motorista.vercel.app` | ✅ Ativo |
| **Portal Cliente** | `https://logi-flow-z315.vercel.app` | ✅ Ativo |
| **Site Divulgação** | `https://logi-flow-wuhp.vercel.app` | ✅ Ativo |

---

## 🔧 Configuração CORS para Railway

Quando configurar as variáveis de ambiente no Railway, use:

```
ALLOWED_ORIGINS=https://logi-flow-blush.vercel.app,https://logi-flow-app-motorista.vercel.app,https://logi-flow-z315.vercel.app,https://logi-flow-wuhp.vercel.app,https://logiflow.com.br
```

---

## 📝 Mapeamento de Arquivos vercel.json

### Frontend Principal
**Arquivo:** `LogiFlow CRM/frontend/vercel.json`
**URL de API:** `https://logiflow-backend.railway.app`
**Status:** ✅ Atualizado

### App Motorista
**Arquivo:** `LogiFlow CRM/app-motorista/vercel.json`
**URL de API:** `https://logiflow-backend.railway.app`
**Status:** ✅ Atualizado

### Portal Cliente
**Arquivo:** `LogiFlow CRM/portal-cliente/vercel.json`
**URL de API:** `https://logiflow-backend.railway.app`
**Status:** ✅ Atualizado

### Site Divulgação
**Arquivo:** `LogiFlow CRM/site-divulgacao/vercel.json`
**Status:** ✅ Sem API (apenas frontend)

---

## 🚀 Próximos Passos

### 1. Deploy do Backend no Railway
Seguir: `GUIA_DEPLOY_PASSO_A_PASSO.md`

### 2. Configurar CORS no Railway
Usar a variável `ALLOWED_ORIGINS` acima em **Settings** → **Variables**

### 3. Testar Integração
```bash
# Verificar cada frontend
curl -I https://logi-flow-blush.vercel.app
curl -I https://logi-flow-app-motorista.vercel.app
curl -I https://logi-flow-z315.vercel.app
curl -I https://logi-flow-wuhp.vercel.app

# Verificar backend
curl https://seu-backend.railway.app/health
```

---

## 📋 Checklist de Validação

- [ ] Backend deployado no Railway
- [ ] CORS configurado com todas as URLs acima
- [ ] Frontend Principal acessível e conectando à API
- [ ] App Motorista acessível e conectando à API
- [ ] Portal Cliente acessível e conectando à API
- [ ] Site Divulgação acessível
- [ ] Autenticação funcionando em todos os frontends
- [ ] Sem erros de CORS no console

---

**Atualizado em:** 27 de Fevereiro de 2026
