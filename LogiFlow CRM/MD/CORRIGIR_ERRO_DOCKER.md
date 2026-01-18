# 🔧 Correção de Erros do Docker

## ❌ Erro que Você Teve

```
[vite:vue] crypto.hash is not a function
Node.js 18.20.8. Vite requires Node.js version 20.19+ or 22.12+
```

## ✅ Solução Aplicada

**1. Dockerfile corrigido** - Node 18 → 20  
**2. Docker Compose Simplificado criado**  
**3. Apenas serviços essenciais**

---

## 🚀 Execute Agora (Versão Corrigida)

### **Opção 1: Modo Mínimo (Recomendado)**

```batch
# Apenas SuiteCRM + API + DB + Redis
start-minimal.bat
```

**Sobe apenas:**
- ✅ MariaDB
- ✅ Redis
- ✅ SuiteCRM
- ✅ Nginx
- ✅ FastAPI

**Não sobe (evita erros de build):**
- ❌ Frontend Vue (opcional)
- ❌ Site (opcional)
- ❌ Celery (opcional)

---

### **Opção 2: Manual Passo a Passo**

```batch
# 1. Criar backend/.env
copy backend\.env.example backend\.env

# 2. Iniciar apenas essenciais
docker-compose -f docker-compose.minimal.yml up -d

# 3. Ver logs
docker-compose -f docker-compose.minimal.yml logs -f
```

---

## 📋 Depois de Iniciar

### **1. Acessar SuiteCRM**
```
URL: http://localhost:8080
```

### **2. Configurar OAuth2**

Siga: `@FINALIZAR_INTEGRACAO_AGORA.md`

1. Admin → OAuth2 Clients
2. Create Client
3. Copiar ID e Secret

### **3. Adicionar no .env**

```batch
# Editar arquivo
notepad backend\.env

# Adicionar:
SUITECRM_CLIENT_ID=seu_id_aqui
SUITECRM_CLIENT_SECRET=seu_secret_aqui

# Salvar
```

### **4. Validar**

```batch
validar-integracao.bat
```

---

## 🐛 Se Ainda Der Erro

### **Problema: Build falha**

**Limpar tudo e tentar novamente:**
```batch
# Parar tudo
docker-compose -f docker-compose.minimal.yml down -v

# Remover imagens antigas
docker image prune -a -f

# Rebuild
docker-compose -f docker-compose.minimal.yml up -d --build
```

### **Problema: SuiteCRM não sobe**

**Ver logs:**
```batch
docker-compose -f docker-compose.minimal.yml logs suitecrm
```

**Verificar permissões (se Linux/Mac):**
```bash
chmod -R 755 suitecrm/
chown -R 1000:1000 suitecrm/
```

### **Problema: API não conecta**

**Verificar .env:**
```batch
type backend\.env | findstr SUITECRM
```

**Deve ter:**
```
SUITECRM_URL=http://suitecrm:9000
SUITECRM_CLIENT_ID=seu_id
SUITECRM_CLIENT_SECRET=seu_secret
```

---

## ✅ Checklist

- [ ] Executar `start-minimal.bat`
- [ ] Aguardar 30 segundos
- [ ] Acessar http://localhost:8080
- [ ] Configurar OAuth2
- [ ] Editar `backend\.env`
- [ ] Executar `validar-integracao.bat`
- [ ] Testes passando 100%

---

## 📚 Arquivos

- `@start-minimal.bat` - Script simplificado
- `@docker-compose.minimal.yml` - Compose minimalista
- `@FINALIZAR_INTEGRACAO_AGORA.md` - Guia OAuth2
- `@validar-integracao.bat` - Validação

---

**Execute:** `start-minimal.bat` 🚀
