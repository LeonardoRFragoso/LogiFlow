# 🔧 Corrigir Root Directory em Todos os Serviços Railway

## 📊 Status Atual

| Serviço | Root Directory | Status |
|---------|----------------|--------|
| **logiflow-api** | `LogiFlow CRM/backend` | ✅ Correto |
| **logiflocrm** | ❌ Raiz | ❌ Errado |
| **logiflow-app-motorista** | ❌ Raiz | ❌ Errado |
| **logiflow-portal-cliente** | ❌ Raiz | ❌ Errado |
| **logiflow-site** | ❌ Raiz | ❌ Errado |

## 🚀 Solução: Configurar Root Directory em Cada Serviço

### Para cada serviço (exceto logiflow-api que já está correto):

1. **Acesse o Railway Dashboard**
2. **Clique no serviço** (ex: logiflocrm)
3. **Vá em Settings** (ícone de engrenagem)
4. **Role até "Service Settings"**
5. **Configure "Root Directory"** conforme a tabela abaixo:

---

## 📋 Root Directory por Serviço

### 1. logiflocrm (Frontend Principal)
```
Root Directory: LogiFlow CRM/frontend
```

### 2. logiflow-app-motorista
```
Root Directory: LogiFlow CRM/app-motorista
```

### 3. logiflow-portal-cliente
```
Root Directory: LogiFlow CRM/portal-cliente
```

### 4. logiflow-site (Site de Divulgação)
```
Root Directory: LogiFlow CRM/site-divulgacao
```

### 5. logiflow-api (Backend) - JÁ ESTÁ CORRETO ✅
```
Root Directory: LogiFlow CRM/backend
```

---

## ✅ Checklist de Configuração

- [ ] **logiflocrm**: Root Directory = `LogiFlow CRM/frontend`
- [ ] **logiflow-app-motorista**: Root Directory = `LogiFlow CRM/app-motorista`
- [ ] **logiflow-portal-cliente**: Root Directory = `LogiFlow CRM/portal-cliente`
- [ ] **logiflow-site**: Root Directory = `LogiFlow CRM/site-divulgacao`
- [ ] **logiflow-api**: Root Directory = `LogiFlow CRM/backend` (já está ✅)

---

## 🔄 Após Configurar

Após configurar o Root Directory em cada serviço:

1. O Railway fará **redeploy automático**
2. Aguarde o status mudar para **"Success"** (verde)
3. Se houver erro, clique em **"View Logs"** para diagnosticar

---

## 🐛 Por Que Isso Acontece?

O Railway detecta automaticamente o tipo de projeto (Node.js, Python, etc.) baseado nos arquivos na **raiz do repositório**. Como o código está em subpastas (`LogiFlow CRM/frontend`, `LogiFlow CRM/backend`, etc.), você precisa configurar o **Root Directory** para cada serviço apontar para a pasta correta.

---

## 📚 Estrutura do Repositório

```
/home/leonardo/dev/LogiFlow/
├── LogiFlow CRM/
│   ├── backend/              ← logiflow-api (✅ correto)
│   ├── frontend/             ← logiflocrm (❌ precisa corrigir)
│   ├── app-motorista/        ← logiflow-app-motorista (❌ precisa corrigir)
│   ├── portal-cliente/       ← logiflow-portal-cliente (❌ precisa corrigir)
│   └── site-divulgacao/      ← logiflow-site (❌ precisa corrigir)
└── ...
```

---

## 🎯 Resultado Esperado

Após configurar todos os Root Directories:

✅ Todos os serviços farão build com sucesso
✅ Frontends carregarão corretamente
✅ Backend responderá em `/health`
✅ Integração entre frontend e backend funcionará

---

**Próximo passo:** Configurar o Root Directory em cada serviço conforme as instruções acima.
