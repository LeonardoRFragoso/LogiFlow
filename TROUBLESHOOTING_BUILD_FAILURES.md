# 🔧 Troubleshooting: Build Failures no Railway

## 📊 Status Atual

| Serviço | Status | Ação |
|---------|--------|------|
| logiflow-app-motorista | ✅ Online | OK |
| logiflow-site | ✅ Online | OK |
| logiflocrm | ❌ Build failed | Diagnosticar |
| logiflow-portal-cliente | ❌ Build failed | Diagnosticar |
| logiflow-api | ❌ Build failed | Diagnosticar |

---

## 🔍 Como Diagnosticar

Para cada serviço com erro:

1. **Clique no serviço** no Railway Dashboard
2. **Vá em "Deployments"**
3. **Clique em "View Logs"**
4. **Procure por mensagens de erro** (geralmente em vermelho)
5. **Compartilhe os logs comigo**

---

## 🐛 Erros Comuns e Soluções

### Erro 1: "Cannot find module 'vite'"
**Causa:** Dependências não instaladas
**Solução:** 
```bash
# Verificar se package.json existe
# Verificar se package-lock.json existe
```

### Erro 2: "Cannot find 'main.py' or 'requirements.txt'"
**Causa:** Root Directory incorreto
**Solução:** Verificar se Root Directory aponta para a pasta correta

### Erro 3: "Build command failed"
**Causa:** Erro no build (vite, webpack, etc.)
**Solução:** Verificar logs para mensagem específica

### Erro 4: "No build output found"
**Causa:** Output directory incorreto no vercel.json
**Solução:** Verificar se `outputDirectory` está correto

---

## 📋 Checklist para Cada Serviço

### logiflocrm (Frontend)
- [ ] Root Directory: `LogiFlow CRM/frontend`
- [ ] Arquivo existe: `LogiFlow CRM/frontend/package.json`
- [ ] Arquivo existe: `LogiFlow CRM/frontend/vercel.json`
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`

### logiflow-portal-cliente (Frontend)
- [ ] Root Directory: `LogiFlow CRM/portal-cliente`
- [ ] Arquivo existe: `LogiFlow CRM/portal-cliente/package.json`
- [ ] Arquivo existe: `LogiFlow CRM/portal-cliente/vercel.json`
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`

### logiflow-api (Backend)
- [ ] Root Directory: `LogiFlow CRM/backend`
- [ ] Arquivo existe: `LogiFlow CRM/backend/requirements.txt`
- [ ] Arquivo existe: `LogiFlow CRM/backend/main.py`
- [ ] Arquivo existe: `LogiFlow CRM/backend/runtime.txt`
- [ ] Variáveis de ambiente configuradas

---

## 🚀 Próximos Passos

1. **Clique em cada serviço com erro**
2. **Vá em "Deployments" → "View Logs"**
3. **Copie os logs de erro**
4. **Compartilhe comigo os logs**

Assim poderei diagnosticar o problema específico de cada serviço.

---

## 💡 Dicas Rápidas

- **Limpar cache:** Settings → Redeploy (força novo build)
- **Verificar variáveis:** Settings → Variables
- **Verificar logs:** Deployments → View Logs
- **Histórico:** Deployments → ver todos os deploys anteriores

---

**Aguardando os logs dos serviços com erro para diagnosticar.**
