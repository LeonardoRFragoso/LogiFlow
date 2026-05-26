# 📝 GUIA: Commit e Deploy LogiFlow CRM

## 🎯 **PASSO A PASSO PARA GITHUB**

### **1. Abrir Terminal no Diretório Correto**

**Opção A: PowerShell**
```powershell
cd "C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM"
```

**Opção B: CMD**
```cmd
cd /d "C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM"
```

---

### **2. Inicializar Git (se ainda não foi feito)**

```bash
git init
```

---

### **3. Configurar Git (primeira vez)**

```bash
git config user.name "Leonardo Fragoso"
git config user.email "leonardo.fragoso@ictsi.com"
```

---

### **4. Adicionar Todos os Arquivos**

```bash
git add .
```

**Ou especificamente o LogiFlow CRM**:
```bash
git add "LogiFlow CRM/"
git add tasks/
```

---

### **5. Criar Commit**

```bash
git commit -m "Deploy: LogiFlow CRM 100% Concluído - 201/201 Tasks - Production Ready"
```

**Ou commit mais detalhado**:
```bash
git commit -m "Deploy: LogiFlow CRM v1.0.0

✅ 201/201 Tasks Concluídas (100%)

Features Implementadas:
- Backend FastAPI completo (30+ routers)
- Frontend Vue 3 responsivo
- GPS Tracking tempo real (Sascar, Autotrac, Onixsat)
- Cotação Automática (Melhor Envio, Frenet, Tabela Própria)
- NPS/CSAT automático com scheduler
- Multi-tenancy completo
- Integrações self-service (ERP, GPS, Frete)
- PWAs (App Motorista + Portal Cliente)
- Documentação completa (11 docs)
- Configuração Render.com

Pronto para deploy em produção!"
```

---

### **6. Criar Repositório no GitHub**

1. Acesse: https://github.com/new
2. Nome: `logiflow-crm`
3. Descrição: `Sistema Completo de Gestão Logística com GPS, NPS e Multi-Tenancy`
4. Público ou Privado: **Privado** (recomendado)
5. **NÃO** adicione README, .gitignore ou licença (já temos)
6. Clique em **"Create repository"**

---

### **7. Conectar ao Repositório Remoto**

```bash
git remote add origin https://github.com/SEU_USUARIO/logiflow-crm.git
```

**Ou com SSH**:
```bash
git remote add origin git@github.com:SEU_USUARIO/logiflow-crm.git
```

---

### **8. Verificar Remote**

```bash
git remote -v
```

**Deve mostrar**:
```
origin  https://github.com/SEU_USUARIO/logiflow-crm.git (fetch)
origin  https://github.com/SEU_USUARIO/logiflow-crm.git (push)
```

---

### **9. Enviar para GitHub**

**Primeira vez (criar branch main)**:
```bash
git branch -M main
git push -u origin main
```

**Próximas vezes**:
```bash
git push origin main
```

---

### **10. Verificar no GitHub**

Acesse: `https://github.com/SEU_USUARIO/logiflow-crm`

Você deve ver:
- ✅ Pasta `LogiFlow CRM/`
- ✅ Pasta `tasks/`
- ✅ Arquivo `render.yaml`
- ✅ Arquivo `README.md`
- ✅ Todos os arquivos commitados

---

## 🚀 **DEPLOY NO RENDER.COM**

### **1. Acessar Render Dashboard**

🔗 https://dashboard.render.com

### **2. Criar Blueprint**

1. Clique em **"New +"** (canto superior direito)
2. Selecione **"Blueprint"**
3. Clique em **"Connect a repository"**
4. **Autorize** o Render a acessar seu GitHub
5. Selecione o repositório: `logiflow-crm`
6. Branch: `main`

### **3. Configurar**

O Render detectará automaticamente o arquivo `render.yaml` em `LogiFlow CRM/render.yaml`.

Clique em **"Apply"**

### **4. Configurar Variáveis de Ambiente**

Após criar os serviços, adicione manualmente:

#### **Backend (logiflow-api)**:

**Obrigatórias**:
```
SECRET_KEY = gere-uma-chave-aleatoria-aqui-64-caracteres
```

**Opcionais (adicione conforme precisar)**:
```
MELHOR_ENVIO_TOKEN = seu_token_melhor_envio
FRENET_TOKEN = seu_token_frenet
GOOGLE_MAPS_DISTANCE_MATRIX_KEY = sua_api_key_google
```

### **5. Aguardar Deploy**

⏱️ **Tempo estimado**: 10-15 minutos

O Render criará:
- ✅ `logiflow-api` (Backend FastAPI)
- ✅ `logiflow-frontend` (Frontend Vue)
- ✅ `logiflow-db` (PostgreSQL)
- ✅ `logiflow-redis` (Redis)

### **6. Verificar Deploy**

**URLs finais**:
```
Frontend:  https://logiflow-frontend.onrender.com
Backend:   https://logiflow-api.onrender.com
API Docs:  https://logiflow-api.onrender.com/docs
Health:    https://logiflow-api.onrender.com/health
```

---

## 🐛 **TROUBLESHOOTING**

### **Erro: "Git not found"**

**Solução**: Instalar Git
```
https://git-scm.com/download/win
```

### **Erro: "Permission denied (publickey)"**

**Solução 1**: Usar HTTPS em vez de SSH
```bash
git remote set-url origin https://github.com/SEU_USUARIO/logiflow-crm.git
```

**Solução 2**: Configurar SSH
```bash
ssh-keygen -t ed25519 -C "seu@email.com"
# Adicionar chave no GitHub: Settings → SSH Keys
```

### **Erro: "Remote origin already exists"**

**Solução**: Remover e adicionar novamente
```bash
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/logiflow-crm.git
```

### **Erro: "Failed to push - rejected"**

**Solução**: Pull primeiro
```bash
git pull origin main --rebase
git push origin main
```

---

## 📋 **CHECKLIST FINAL**

Antes de fazer deploy:

- [ ] Código commitado no GitHub
- [ ] Repositório acessível
- [ ] Arquivo `render.yaml` presente
- [ ] `.gitignore` configurado
- [ ] `requirements.txt` atualizado
- [ ] `runtime.txt` presente
- [ ] Documentação completa
- [ ] Variáveis de ambiente documentadas

---

## 📞 **SUPORTE**

**Documentação Completa**:
- `LogiFlow CRM/DEPLOY_RENDER.md` - Guia detalhado Render
- `LogiFlow CRM/README_FINAL.md` - README completo
- `LogiFlow CRM/docs/` - 11 documentos técnicos

**Links Úteis**:
- Render Docs: https://render.com/docs
- GitHub Docs: https://docs.github.com

---

## 🎉 **PRONTO!**

Após seguir estes passos, seu **LogiFlow CRM** estará:
- ✅ Versionado no GitHub
- ✅ Rodando em produção no Render.com
- ✅ Acessível publicamente via HTTPS
- ✅ Com deploy automático (CD/CI)

**Sucesso no deploy!** 🚀

