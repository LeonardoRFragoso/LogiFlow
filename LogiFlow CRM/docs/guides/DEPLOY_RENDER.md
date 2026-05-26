# 🚀 Deploy LogiFlow CRM no Render.com

## 📋 **PRÉ-REQUISITOS**

1. ✅ Conta no [Render.com](https://render.com)
2. ✅ Repositório GitHub com o código
3. ✅ Credenciais das APIs externas (opcional)

---

## 🔧 **PASSO A PASSO**

### **1. Conectar Repositório GitHub**

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **"New +"** → **"Blueprint"**
3. Conecte seu repositório GitHub
4. Selecione o repositório `LogiFlow CRM`
5. O Render detectará automaticamente o arquivo `render.yaml`

---

### **2. Configurar Variáveis de Ambiente**

No painel do Render, adicione manualmente as seguintes variáveis:

#### **Backend (logiflow-api)**:

**Obrigatórias**:
```bash
SECRET_KEY=seu-secret-key-aqui-gere-um-aleatório
DATABASE_URL=postgresql://...  # Auto-preenchido pelo Render
REDIS_URL=redis://...           # Auto-preenchido pelo Render
```

**Opcionais (Integrações)**:
```bash
# Melhor Envio
MELHOR_ENVIO_TOKEN=seu_token_aqui
MELHOR_ENVIO_SANDBOX=false

# Frenet
FRENET_TOKEN=seu_token_frenet

# Google Maps
GOOGLE_MAPS_DISTANCE_MATRIX_KEY=sua_api_key

# Omie ERP
OMIE_APP_KEY=seu_app_key
OMIE_APP_SECRET=seu_app_secret

# Bling ERP
BLING_API_KEY=sua_api_key

# WhatsApp (Evolution API)
EVOLUTION_API_URL=http://sua-instancia.com
EVOLUTION_API_KEY=sua_api_key
```

---

### **3. Deploy Automático**

1. Após configurar, clique em **"Apply"**
2. O Render criará automaticamente:
   - ✅ **logiflow-api** (Backend FastAPI)
   - ✅ **logiflow-frontend** (Frontend Vue)
   - ✅ **logiflow-db** (PostgreSQL)
   - ✅ **logiflow-redis** (Redis)

3. **Tempo de deploy**: ~10-15 minutos

---

### **4. Verificar Deploy**

#### **Backend**:
```bash
# Health Check
curl https://logiflow-api.onrender.com/health

# Docs
https://logiflow-api.onrender.com/docs
```

#### **Frontend**:
```bash
https://logiflow-frontend.onrender.com
```

---

## 🔐 **CONFIGURAÇÕES DE SEGURANÇA**

### **1. Atualizar CORS no Backend**

Edite `backend/config.py`:
```python
ALLOWED_ORIGINS = [
    "https://logiflow-frontend.onrender.com",
    "http://localhost:8080"
]
```

### **2. Configurar Domínio Customizado (Opcional)**

No painel do Render:
1. Vá em **logiflow-frontend** → **Settings** → **Custom Domains**
2. Adicione `app.logiflow.com.br`
3. Configure DNS no seu provedor:
   ```
   CNAME app logiflow-frontend.onrender.com
   ```

---

## 📊 **MONITORAMENTO**

### **Logs em Tempo Real**:
```bash
# Backend
https://dashboard.render.com/web/logiflow-api/logs

# Frontend
https://dashboard.render.com/static/logiflow-frontend/logs
```

### **Métricas**:
- CPU, Memória, Requisições
- Health Check status
- Deploy history

---

## 🔄 **DEPLOY CONTÍNUO (CI/CD)**

O Render faz deploy automático a cada push na branch `main`:

```bash
git add .
git commit -m "Update: nova feature"
git push origin main
```

**Render detectará e fará deploy automaticamente!** ✅

---

## 💰 **CUSTOS (Plano Starter)**

| Serviço | Custo Mensal |
|---------|--------------|
| Backend (Web Service) | $7/mês |
| Frontend (Static Site) | Grátis |
| PostgreSQL | $7/mês |
| Redis | $10/mês |
| **TOTAL** | **~$24/mês** |

**Plano Free**: 750 horas/mês gratuitas (suficiente para testes)

---

## 🐛 **TROUBLESHOOTING**

### **Erro: "Build failed"**

**Solução**:
```bash
# Verificar requirements.txt
cd "LogiFlow CRM/backend"
pip freeze > requirements.txt

# Verificar Python version
python --version  # Deve ser 3.11+
```

### **Erro: "Database connection failed"**

**Solução**:
1. Verificar `DATABASE_URL` nas env vars
2. Aguardar 2-3 minutos (banco inicializando)
3. Rodar migrações manualmente:
   ```bash
   # No shell do Render
   cd "LogiFlow CRM/backend"
   alembic upgrade head
   ```

### **Erro: "CORS blocked"**

**Solução**:
Adicionar frontend URL no `ALLOWED_ORIGINS`:
```python
ALLOWED_ORIGINS = [
    "https://logiflow-frontend.onrender.com"
]
```

---

## 🔧 **COMANDOS ÚTEIS**

### **Rodar Migrações**:
```bash
# No Render Shell (logiflow-api)
cd "LogiFlow CRM/backend"
alembic upgrade head
```

### **Criar Usuário Admin**:
```bash
# No Render Shell (logiflow-api)
cd "LogiFlow CRM/backend"
python -c "
from database import SessionLocal
from models import User
from passlib.context import CryptContext

db = SessionLocal()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

admin = User(
    email='admin@logiflow.com.br',
    password_hash=pwd_context.hash('Admin@123'),
    is_active=True,
    role='admin',
    tenant_id='default'
)
db.add(admin)
db.commit()
print('✅ Admin criado!')
"
```

---

## 📝 **CHECKLIST PÓS-DEPLOY**

- [ ] Backend `/health` retorna 200 OK
- [ ] Frontend carrega corretamente
- [ ] Login funciona
- [ ] API Docs acessível (`/docs`)
- [ ] Database conectado
- [ ] Redis conectado
- [ ] CORS configurado
- [ ] Variáveis de ambiente setadas
- [ ] Logs sem erros críticos
- [ ] Health checks passing

---

## 🌐 **URLs FINAIS**

Após deploy bem-sucedido:

```
Frontend:  https://logiflow-frontend.onrender.com
Backend:   https://logiflow-api.onrender.com
API Docs:  https://logiflow-api.onrender.com/docs
Health:    https://logiflow-api.onrender.com/health
```

---

## 🎉 **DEPLOY CONCLUÍDO!**

Seu LogiFlow CRM está rodando em produção no Render.com! 🚀

**Próximos Passos**:
1. Configurar domínio customizado
2. Adicionar SSL/TLS (automático no Render)
3. Configurar backups do banco
4. Monitorar logs e métricas
5. Configurar alertas (Slack, Email)

---

**Suporte**: contato@logiflow.com.br  
**Docs**: https://render.com/docs

**✅ Production Ready!**

