# 🐳 LogiFlow CRM - Guia Completo de Execução via Docker

**Status:** ✅ **PRONTO PARA EXECUÇÃO**  
**Data:** 15 de Dezembro de 2025

---

## 📋 Pré-requisitos

### **Software Necessário**

- ✅ **Docker Desktop** 20.10+
  - Windows: [Download](https://www.docker.com/products/docker-desktop/)
  - Mac: [Download](https://www.docker.com/products/docker-desktop/)
  - Linux: `sudo apt install docker-ce docker-compose-plugin`

- ✅ **Git** (para clonar o projeto)

### **Recursos Mínimos**

- **RAM:** 8GB (recomendado 16GB)
- **Disco:** 20GB livres
- **CPU:** 4 cores

---

## 🚀 Início Rápido (5 minutos)

### **Opção 1: Windows (Recomendado)**

```batch
# 1. Abrir PowerShell ou CMD como Administrador
cd "C:\Users\leona\OneDrive\Documentos\Projetos\LogiFlow\LogiFlow CRM"

# 2. Executar script automático
start-docker.bat
```

### **Opção 2: Linux/Mac**

```bash
# 1. Dar permissão de execução
chmod +x start-docker.sh

# 2. Executar script
./start-docker.sh
```

### **Opção 3: Manual**

```bash
# 1. Copiar variáveis de ambiente
cp .env.docker .env

# 2. Iniciar serviços
docker-compose up -d

# 3. Aguardar inicialização (2-3 minutos)
docker-compose logs -f
```

---

## 📦 O Que Será Iniciado

### **9 Serviços Docker**

| Serviço | Porta | Descrição | Container |
|---------|-------|-----------|-----------|
| **MariaDB** | 3306 | Banco de dados | `logiflow_db` |
| **Redis** | 6379 | Cache/Fila | `logiflow_redis` |
| **SuiteCRM** | - | CRM Backend | `logiflow_suitecrm` |
| **Nginx** | 8080, 8443 | Web Server | `logiflow_nginx` |
| **FastAPI** | 8000 | API Backend | `logiflow_api` |
| **Frontend** | 3001 | App Vue.js | `logiflow_frontend` |
| **Site** | 5173 | Landing Page | `logiflow_site` |
| **Celery Worker** | - | Tarefas Async | `logiflow_celery_worker` |
| **Celery Beat** | - | Scheduler | `logiflow_celery_beat` |
| **Adminer** | 8082 | DB Admin (dev) | `logiflow_adminer` |

---

## 🌐 URLs de Acesso

Após iniciar, acesse:

```
✅ SuiteCRM:        http://localhost:8080
✅ API FastAPI:     http://localhost:8000
✅ API Docs:        http://localhost:8000/api/v1/docs
✅ Frontend Vue:    http://localhost:3001
✅ Site:            http://localhost:5173
✅ Adminer (DB):    http://localhost:8082
```

---

## 🔧 Configuração Inicial

### **1. Variáveis de Ambiente (.env)**

O script cria automaticamente `.env` a partir de `.env.docker`.

**Edite `.env` para configurar:**

```env
# OAuth2 SuiteCRM (obrigatório para integração)
SUITECRM_CLIENT_ID=seu_client_id_aqui
SUITECRM_CLIENT_SECRET=seu_client_secret_aqui

# Integrações opcionais
FOCUSNFE_TOKEN=seu_token_focus_nfe
GOOGLE_MAPS_API_KEY=sua_key_google
MERCADOPAGO_ACCESS_TOKEN=seu_token_mp
```

### **2. SuiteCRM - Primeira Execução**

**2.1. Acessar:** http://localhost:8080

**2.2. Se aparecer instalação:**
- Database: MariaDB
- Host: `db`
- Database: `logiflow_crm`
- User: `logiflow`
- Password: `logiflow123`
- Admin user: criar conforme desejar

**2.3. Configurar OAuth2:**
1. Login como Admin
2. **Admin → OAuth2 Clients and Tokens**
3. **Create OAuth2 Client**
4. Copiar Client ID e Secret
5. Adicionar no `.env`

**Guia detalhado:** `@CONFIGURAR_OAUTH2_SUITECRM.md`

### **3. Executar Scripts SQL**

```bash
# Acessar container do banco
docker exec -i logiflow_db mysql -u root -p"rootpass123" logiflow_crm < SCRIPTS_SQL_INSTALACAO.sql

# OU via Adminer (http://localhost:8082)
# System: MySQL
# Server: db
# Username: logiflow
# Password: logiflow123
# Database: logiflow_crm
# Copiar e executar conteúdo de SCRIPTS_SQL_INSTALACAO.sql
```

### **4. Quick Repair no SuiteCRM**

```
Admin → Repair → Quick Repair and Rebuild
Admin → Repair → Rebuild Relationships
Admin → Display Modules → Habilitar os 6 módulos customizados
```

---

## ✅ Testar Integração

### **1. Testar API FastAPI**

```bash
# Healthcheck
curl http://localhost:8000/health

# Deve retornar:
# {"status":"ok","redis":true}
```

### **2. Testar SuiteCRM**

```bash
# Acessar
http://localhost:8080

# Login com credenciais criadas na instalação
```

### **3. Testar Integração SuiteCRM ↔ FastAPI**

```bash
# Entrar no container da API
docker exec -it logiflow_api bash

# Executar testes
python tests/test_suitecrm_integration.py

# Deve mostrar:
# ✅ 12 testes | 100% sucesso
```

---

## 📊 Monitoramento

### **Ver Logs**

```bash
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f api

# Apenas SuiteCRM
docker-compose logs -f suitecrm nginx

# Últimas 100 linhas
docker-compose logs --tail=100
```

### **Ver Status**

```bash
# Status de todos os containers
docker-compose ps

# Uso de recursos
docker stats
```

### **Entrar nos Containers**

```bash
# API FastAPI
docker exec -it logiflow_api bash

# SuiteCRM
docker exec -it logiflow_suitecrm bash

# Banco de dados
docker exec -it logiflow_db mysql -u root -p
```

---

## 🛠️ Comandos Úteis

### **Gerenciamento Básico**

```bash
# Iniciar tudo
docker-compose up -d

# Parar tudo
docker-compose down

# Reiniciar serviço específico
docker-compose restart api

# Rebuild após mudanças no código
docker-compose up -d --build

# Ver logs em tempo real
docker-compose logs -f api
```

### **Limpeza e Manutenção**

```bash
# Parar e remover volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Remover imagens antigas
docker image prune -a

# Limpar tudo (build cache, containers parados, etc)
docker system prune -a --volumes
```

### **Backup de Dados**

```bash
# Backup do banco de dados
docker exec logiflow_db mysqldump -u root -p"rootpass123" logiflow_crm > backup.sql

# Restaurar backup
docker exec -i logiflow_db mysql -u root -p"rootpass123" logiflow_crm < backup.sql
```

---

## 🐛 Troubleshooting

### **Problema 1: Docker não inicia**

```
❌ Erro: Cannot connect to Docker daemon
```

**Solução:**
- Inicie o Docker Desktop
- Windows: Procurar "Docker Desktop" no menu iniciar
- Aguarde ícone ficar verde

---

### **Problema 2: Porta já em uso**

```
❌ Bind for 0.0.0.0:8080 failed: port is already allocated
```

**Solução:**
```bash
# Windows: Descobrir processo
netstat -ano | findstr :8080
taskkill /PID <numero_pid> /F

# Linux/Mac
lsof -ti :8080 | xargs kill -9

# Ou alterar porta no docker-compose.yml
```

---

### **Problema 3: Containers não ficam healthy**

```bash
# Ver logs detalhados
docker-compose logs api

# Verificar healthcheck
docker inspect logiflow_api | grep -A 10 Health

# Reiniciar container específico
docker-compose restart api
```

---

### **Problema 4: SuiteCRM dá erro 500**

**Causa comum:** Permissões de arquivo

**Solução:**
```bash
# Entrar no container
docker exec -it logiflow_suitecrm bash

# Ajustar permissões
chown -R www:www /var/www/html
chmod -R 755 /var/www/html

# Quick Repair
# Admin → Repair → Quick Repair
```

---

### **Problema 5: API não conecta ao banco**

**Verificar:**
```bash
# 1. Banco está rodando?
docker-compose ps db

# 2. Testar conexão
docker exec logiflow_api python -c "from database import test_connection; test_connection()"

# 3. Ver logs do banco
docker-compose logs db
```

---

### **Problema 6: Frontend não carrega**

**Verificar:**
```bash
# 1. Build completou?
docker-compose logs frontend

# 2. Nginx está servindo?
curl http://localhost:3001

# 3. Rebuild
docker-compose up -d --build frontend
```

---

## 🔄 Atualizar Código

### **Após mudanças no código:**

```bash
# 1. Backend (API)
docker-compose restart api
# Uvicorn está com --reload, atualiza automaticamente

# 2. Frontend (requer rebuild)
docker-compose up -d --build frontend

# 3. SuiteCRM (vardefs, hooks)
# Entrar no container e executar Quick Repair
docker exec -it logiflow_suitecrm bash
# No SuiteCRM: Admin → Repair → Quick Repair
```

---

## 📈 Performance

### **Otimizações:**

**1. Aumentar recursos do Docker Desktop:**
- Settings → Resources → Memory: 8GB+
- CPU: 4+ cores

**2. Build cache:**
```bash
# Usar cache do Docker
docker-compose build

# Sem cache (mais lento, mas limpo)
docker-compose build --no-cache
```

**3. Volumes de desenvolvimento:**
- Backend e SuiteCRM usam bind mounts (hot reload)
- Frontend é build estático (mais rápido)

---

## 🚀 Produção

### **Para deploy em produção:**

**1. Usar docker-compose.prod.yml** (criar se não existir)

**2. Configurações de segurança:**
```env
DEBUG=False
SECRET_KEY=use-strong-random-key-here
ALLOWED_HOSTS=seudominio.com
SUITECRM_URL=https://crm.seudominio.com
```

**3. SSL/HTTPS:**
- Usar nginx com certificados
- Let's Encrypt via Certbot

**4. Banco de dados:**
- Usar volume persistente
- Backups automáticos
- Considerar RDS (AWS) ou DBaaS

**5. Monitoramento:**
- Prometheus + Grafana
- Logs centralizados (ELK, Loki)
- APM (New Relic, Datadog)

---

## 📚 Documentação Relacionada

### **Setup e Configuração:**
- `@CONFIGURAR_OAUTH2_SUITECRM.md` - Configurar OAuth2
- `@SCRIPTS_SQL_INSTALACAO.sql` - Scripts do banco
- `@INSTALACAO_COMPLETA_SUITECRM.md` - Instalação SuiteCRM
- `@.env.docker` - Variáveis de ambiente

### **Integração:**
- `@STATUS_INTEGRACAO_SUITECRM.md` - Status da integração
- `@INTEGRACAO_COMPLETA_FINAL.md` - Guia de integração
- `@backend/tests/test_suitecrm_integration.py` - Testes

### **Implementação:**
- `@IMPLEMENTACAO_FINAL_RESUMO.md` - Resumo geral
- `@ANALISE_IMPLEMENTACAO_SUITECRM.md` - Análise técnica

---

## ✅ Checklist de Verificação

### **Antes de iniciar:**
- [ ] Docker Desktop instalado e rodando
- [ ] 8GB+ RAM disponível
- [ ] 20GB+ disco livre
- [ ] Portas 8080, 8000, 3001, 5173 livres

### **Após iniciar:**
- [ ] Todos containers rodando (`docker-compose ps`)
- [ ] SuiteCRM acessível (http://localhost:8080)
- [ ] API healthcheck OK (http://localhost:8000/health)
- [ ] Frontend carregando (http://localhost:3001)
- [ ] Logs sem erros críticos

### **Configuração:**
- [ ] `.env` criado e configurado
- [ ] OAuth2 Client criado no SuiteCRM
- [ ] Credenciais OAuth2 no `.env`
- [ ] Scripts SQL executados
- [ ] Quick Repair executado
- [ ] Módulos habilitados

### **Integração:**
- [ ] Testes de integração passando (100%)
- [ ] API conectando ao SuiteCRM
- [ ] CRUD funcionando nos 6 módulos

---

## 🎯 Próximos Passos Após Instalação

1. ✅ **Configurar integrações externas**
   - Focus NFe (CT-e/MDF-e)
   - Evolution API (WhatsApp)
   - Google Maps
   - Mercado Pago

2. ✅ **Criar usuários e permissões**
   - Roles no SuiteCRM
   - Tenants no FastAPI
   - Security Groups

3. ✅ **Importar dados iniciais**
   - Clientes de teste
   - Motoristas
   - Veículos

4. ✅ **Configurar workflows**
   - AOW no SuiteCRM
   - Celery tasks no backend

5. ✅ **Testar fluxo completo**
   - Criar cotação
   - Aprovar e gerar pedido
   - Atribuir motorista/veículo
   - Registrar entrega
   - Verificar notificações

---

## 📞 Suporte

### **Logs importantes:**
```bash
# API
docker-compose logs -f api

# SuiteCRM + Nginx
docker-compose logs -f suitecrm nginx

# Banco de dados
docker-compose logs -f db

# Workers (Celery)
docker-compose logs -f celery_worker celery_beat
```

### **Arquivos de configuração:**
- `docker-compose.yml` - Orquestração
- `.env` - Variáveis de ambiente
- `docker/*/Dockerfile` - Images customizadas
- `docker/nginx/sites/` - Configuração Nginx

---

## 🎉 Resumo

**Tempo estimado de setup:** 30-45 minutos

**Passos principais:**
1. ⏱️ 5 min - Executar `start-docker.bat`
2. ⏱️ 10 min - Configurar OAuth2 no SuiteCRM
3. ⏱️ 5 min - Executar scripts SQL
4. ⏱️ 5 min - Quick Repair
5. ⏱️ 5 min - Testar integração
6. ⏱️ 10 min - Configurar integrações (opcional)

**Status:** ✅ **100% Pronto para Docker!**

---

**LogiFlow CRM está pronto para rodar via Docker!** 🐳🚀

**Última atualização:** 15 de Dezembro de 2025
