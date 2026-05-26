# 🐳 Docker Stack Completo - LogiFlow CRM

## 📦 Componentes do Sistema

### **Arquitetura Completa**

```
┌─────────────────────────────────────────────────────────┐
│                    LOGIFLOW CRM                         │
│                   STACK COMPLETO                        │
└─────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Sistema    │  │  App Motor.  │  │     Site     │  │    Portal    │
│  Principal   │  │   Vue.js     │  │  Divulgação  │  │   Cliente    │
│  Vue.js      │  │   :3002      │  │   Vue.js     │  │   Vue.js     │
│   :3001      │  │              │  │    :5173     │  │    :3003     │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │                  │
       └─────────────────┼──────────────────┼──────────────────┘
                         │
                ┌────────▼────────┐
                │   Backend API   │
                │    FastAPI      │
                │     :8000       │
                └────────┬────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼───────┐ ┌─────▼─────┐ ┌───────▼───────┐
│   SuiteCRM    │ │   MySQL   │ │     Redis     │
│  Nginx+PHP    │ │  MariaDB  │ │    Cache      │
│    :8080      │ │   :3306   │ │    :6379      │
└───────────────┘ └───────────┘ └───────────────┘

┌─────────────────────────────────────────────────────────┐
│              WORKERS & SCHEDULERS                       │
├─────────────────────────────────────────────────────────┤
│  • Celery Worker (tarefas assíncronas)                  │
│  • Celery Beat (agendamentos)                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              FERRAMENTAS DE DEV                         │
├─────────────────────────────────────────────────────────┤
│  • Adminer :8082 (gerenciar MySQL)                      │
│  • Redis Commander :8081 (gerenciar Redis)              │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Como Usar

### **1. Iniciar Stack Completo**

```bash
# Windows
start-all.bat

# Linux/Mac
chmod +x start-all.sh
./start-all.sh
```

**Ou manualmente:**

```bash
# Stack básico (essencial)
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml up -d

# Stack completo (com workers e site)
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml --profile full up -d

# Stack com ferramentas de desenvolvimento
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml --profile dev --profile full up -d
```

---

### **2. Parar Todos os Serviços**

```bash
# Windows
stop-all.bat

# Linux/Mac
./stop-all.sh

# Ou manualmente
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml down
```

---

### **3. Ver Logs**

```bash
# Todos os serviços
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f

# Serviço específico
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f api
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f frontend
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f suitecrm
```

---

## 🌐 Acessos e Portas

| Serviço | URL | Porta | Descrição |
|---------|-----|-------|-----------|
| **Sistema Principal** | http://localhost:3001 | 3001 | Interface principal do CRM (Vue.js) |
| **App Motorista** | http://localhost:3002 | 3002 | App para motoristas (Vue.js) |
| **Portal Cliente** | http://localhost:3003 | 3003 | Portal self-service clientes (Vue.js) |
| **Site Divulgação** | http://localhost:5173 | 5173 | Site institucional (Vue.js) |
| **Backend API** | http://localhost:8000 | 8000 | API FastAPI |
| **API Docs** | http://localhost:8000/api/v1/docs | 8000 | Swagger UI |
| **SuiteCRM** | http://localhost:8080 | 8080 | Interface nativa do CRM |
| **Adminer** | http://localhost:8082 | 8082 | Gerenciar banco MySQL |
| **Redis Commander** | http://localhost:8081 | 8081 | Gerenciar cache Redis |
| **MySQL** | localhost:3306 | 3306 | Banco de dados direto |
| **Redis** | localhost:6379 | 6379 | Cache direto |

---

## 📋 Serviços Incluídos

### **Essenciais (sempre rodando)**

1. ✅ **db** - MariaDB 10.6
   - Banco de dados principal
   - Volumes persistentes
   - Healthcheck configurado

2. ✅ **redis** - Redis 7
   - Cache e fila de mensagens
   - Persistência em disco
   - Senha configurada

3. ✅ **suitecrm** - PHP-FPM 8.1
   - SuiteCRM 8.x
   - Supervisord (cron + php-fpm)
   - Volumes compartilhados

4. ✅ **nginx** - Nginx Alpine
   - Proxy reverso para SuiteCRM
   - SSL/TLS pronto
   - Logs persistentes

5. ✅ **api** - FastAPI (Python 3.11)
   - Backend principal
   - Auto-reload em desenvolvimento
   - Healthcheck configurado

**4 FRONTENDS VUE.JS:**

6. ✅ **frontend** - Sistema Principal (Vue.js 3)
   - Interface CRM completa
   - Dashboard, pedidos, entregas
   - Build otimizado

7. ✅ **app-motorista** - App Motorista (Vue.js 3)
   - Interface para motoristas
   - Entregas, rotas, GPS
   - Mobile-first

8. ✅ **portal-cliente** - Portal Cliente (Vue.js 3)
   - Self-service para clientes
   - Rastreamento, cotações
   - Área do cliente

9. ✅ **site-divulgacao** - Site Institucional (Vue.js 3)
   - Landing page
   - Informações da empresa
   - Marketing

---

### **Opcionais (profile: full)**

10. 🔧 **celery_worker** - Worker Assíncrono
   - Processa tarefas em background
   - Integração com Redis

10. 🔧 **celery_beat** - Scheduler
    - Tarefas agendadas
    - Cron jobs automáticos

---

### **Desenvolvimento (profile: dev)**

11. 🛠️ **adminer** - Gerenciador MySQL
    - Interface web para banco
    - Suporta múltiplos bancos

12. 🛠️ **redis-commander** - Gerenciador Redis
    - Visualizar cache
    - Debug de filas

---

## 🔧 Configuração

### **Variáveis de Ambiente**

Crie um arquivo `.env` na raiz:

```env
# Banco de Dados
DB_ROOT_PASSWORD=rootpass123
DB_NAME=logiflow_crm
DB_USER=logiflow
DB_PASSWORD=logiflow123

# Redis
REDIS_PASSWORD=redis123

# API
DEBUG=True
SECRET_KEY=change-this-in-production-to-a-secure-random-key

# SuiteCRM OAuth2
SUITECRM_CLIENT_ID=seu-client-id-aqui
SUITECRM_CLIENT_SECRET=seu-client-secret-aqui

# Focus NFe (Fiscal)
FOCUSNFE_TOKEN=seu-token-aqui

# Site
SITE_URL=http://localhost:8080
```

---

## 📊 Volumes Persistentes

```yaml
volumes:
  mariadb_data:      # Dados do MySQL
  redis_data:        # Cache Redis
  nginx_logs:        # Logs do Nginx
  static_volume:     # Arquivos estáticos
  media_volume:      # Uploads de mídia
```

**Localização:** Docker gerencia automaticamente em:
- Windows: `C:\ProgramData\docker\volumes\`
- Linux: `/var/lib/docker/volumes/`

---

## 🔍 Troubleshooting

### **Problema: Container não inicia**

```bash
# Ver logs do container
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs nome_do_container

# Verificar status
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml ps

# Reiniciar container específico
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml restart nome_do_container
```

---

### **Problema: Porta já em uso**

```bash
# Windows - Ver quem está usando a porta
netstat -ano | findstr :8000

# Matar processo
taskkill /PID numero_do_pid /F

# Ou alterar porta no docker compose -f docker/docker-compose.yml.production.yml
```

---

### **Problema: Banco não conecta**

```bash
# Verificar se MySQL está rodando
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml ps db

# Testar conexão
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml exec db mysql -u logiflow -plogiflow123 logiflow_crm

# Ver logs do banco
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs db
```

---

### **Problema: API retorna erro 500**

```bash
# Ver logs detalhados
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f api

# Entrar no container
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml exec api sh

# Verificar variáveis de ambiente
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml exec api env
```

---

### **Problema: Frontend não carrega**

```bash
# Rebuild do frontend
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml build --no-cache frontend
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml up -d frontend

# Ver logs
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs frontend
```

---

## 🧹 Manutenção

### **Limpar Tudo (CUIDADO!)**

```bash
# Parar e remover containers + volumes
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml down -v

# Limpar imagens não usadas
docker image prune -a

# Limpar tudo do Docker
docker system prune -a --volumes
```

---

### **Backup do Banco**

```bash
# Exportar banco
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml exec db mysqldump -u logiflow -plogiflow123 logiflow_crm > backup.sql

# Importar banco
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml exec -T db mysql -u logiflow -plogiflow123 logiflow_crm < backup.sql
```

---

### **Atualizar Imagens**

```bash
# Rebuild todas as imagens
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml build --no-cache

# Pull imagens base atualizadas
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml pull

# Recriar containers
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml up -d --force-recreate
```

---

## 📈 Monitoramento

### **Ver Recursos Usados**

```bash
# CPU e memória de cada container
docker stats

# Espaço em disco dos volumes
docker system df -v
```

---

### **Healthchecks**

Todos os serviços essenciais têm healthchecks configurados:

```bash
# Ver status de saúde
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml ps

# Legenda:
# healthy - Serviço funcionando
# unhealthy - Serviço com problemas
# starting - Iniciando
```

---

## 🎯 Profiles Disponíveis

### **Básico (padrão)**
```bash
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml up -d
```
Inicia: db, redis, suitecrm, nginx, api, frontend

### **Completo**
```bash
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml --profile full up -d
```
Adiciona: site, app-motorista, celery_worker, celery_beat

### **Desenvolvimento**
```bash
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml --profile dev up -d
```
Adiciona: adminer, redis-commander

### **Tudo**
```bash
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml --profile full --profile dev up -d
```
Todos os serviços

---

## ✅ Checklist de Inicialização

- [ ] Docker Desktop está rodando
- [ ] Arquivo `.env` configurado
- [ ] Portas 3001, 8000, 8080 estão livres
- [ ] Executar `start-all.bat` ou comando manual
- [ ] Aguardar ~30 segundos para inicialização
- [ ] Acessar http://localhost:3001
- [ ] Verificar http://localhost:8000/api/v1/docs
- [ ] Testar login no SuiteCRM http://localhost:8080

---

## 📞 Suporte

**Logs importantes:**
- API: `docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f api`
- Frontend: `docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f frontend`
- SuiteCRM: `docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f suitecrm nginx`
- Banco: `docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml logs -f db`

**Comandos úteis:**
```bash
# Status de todos os containers
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml ps

# Reiniciar tudo
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml restart

# Parar tudo
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.production.yml down

# Ver uso de recursos
docker stats
```

---

**Stack criado em:** 16/12/2024  
**Versão:** 1.0.0  
**Status:** ✅ Produção Ready
