# 🚀 LogiFlow CRM - Checklist de Go Live BETA

**Data de Criação**: 30 de Dezembro de 2024  
**Versão**: 1.0.0-beta  
**Status**: Preparação Final

---

## 📋 CHECKLIST OBRIGATÓRIO ANTES DO BETA

### 🔴 BLOQUEADORES CRÍTICOS (Obrigatório)

- [ ] **1. OAuth2 SuiteCRM Configurado**
  - [ ] OAuth2 Client criado no SuiteCRM
  - [ ] CLIENT_ID e CLIENT_SECRET no `.env`
  - [ ] Teste de conexão passando
  - **Script**: `python backend/scripts/setup_oauth2_suitecrm.py`
  - **Validação**: `docker exec logiflow_api python tests/smoke_test_beta.py`

- [ ] **2. Dados Demo Criados**
  - [ ] Empresa demo existe
  - [ ] Usuário admin@logiflow.demo criado
  - [ ] Motoristas, veículos e clientes demo existem
  - [ ] Cotação e pedido demo existem
  - **Script**: `docker exec logiflow_api python scripts/seed_demo_data.py`

- [ ] **3. Smoke Test End-to-End Passando**
  - [ ] Backend sobe sem erro
  - [ ] Database conectado
  - [ ] Redis conectado
  - [ ] Login funcional
  - [ ] Criar cotação funciona
  - [ ] GPS simulação ativa
  - **Comando**: `docker exec logiflow_api python tests/smoke_test_beta.py`

### 🟡 AJUSTES NECESSÁRIOS (Importante)

- [ ] **4. Feature Flags Ativos**
  - [ ] Endpoint `/api/v1/features` respondendo
  - [ ] Features críticas habilitadas (AUTH, DASHBOARD, COTACOES, PEDIDOS_FRETE)
  - [ ] Features em simulação identificadas (GPS, FISCAL)
  - [ ] Features desabilitadas escondidas (ERP_SYNC_AUTO)
  - **Validação**: `curl http://localhost:8000/api/v1/features`

- [ ] **5. Docker Compose Validado**
  - [ ] `docker compose -f docker/docker-compose.yml.minimal.yml` inicia sem erro
  - [ ] Todos containers healthy (db, redis, suitecrm, nginx, api)
  - [ ] Logs sem erros críticos
  - [ ] Portas corretas expostas (3306, 6379, 8080, 8000)
  - **Comando**: `docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml ps`

- [ ] **6. Variáveis de Ambiente Configuradas**
  - [ ] `backend/.env` existe
  - [ ] SECRET_KEY definido
  - [ ] SUITECRM_CLIENT_ID preenchido
  - [ ] SUITECRM_CLIENT_SECRET preenchido
  - [ ] Modos de simulação ativos (GPS, FISCAL)

### 🟢 DOCUMENTAÇÃO E SUPORTE (Recomendado)

- [ ] **7. Documentação de Acesso**
  - [ ] Credenciais demo documentadas
  - [ ] URLs de acesso listadas
  - [ ] Passos de troubleshooting básico
  - [ ] FAQ para usuários beta

- [ ] **8. Logs e Monitoramento**
  - [ ] Logs do backend acessíveis
  - [ ] Erros sendo capturados
  - [ ] Sistema de alerta configurado (opcional)

---

## 🎯 CRITÉRIOS DE ACEITAÇÃO DO BETA

### ✅ Sistema é considerado "Pronto para BETA" quando:

1. **Usuário consegue acessar** o sistema sem intervenção técnica
2. **Fluxo principal funciona**:
   - Login → Dashboard → Criar Cotação → Ver Pedidos
3. **Dados demo existem** (sistema não vazio)
4. **Funcionalidades não-críticas** estão em modo simulação
5. **Smoke test passa** com 100% de sucesso

### ❌ Bloqueios para BETA:

1. OAuth2 não configurado
2. Login não funciona
3. Backend não sobe
4. Banco de dados inacessível
5. Smoke test com falhas críticas

---

## 🛠️ SCRIPTS DE SETUP DISPONÍVEIS

### Setup Completo (5 minutos)
```batch
# Windows
scripts\setup-beta.bat

# O que faz:
# - Verifica Docker
# - Cria .env
# - Inicia containers
# - Cria dados demo
# - Mostra instruções OAuth2
```

### Setup OAuth2 (2 minutos)
```batch
python backend\scripts\setup_oauth2_suitecrm.py

# O que faz:
# - Mostra instruções para criar OAuth2 Client
# - Coleta CLIENT_ID e CLIENT_SECRET
# - Atualiza backend/.env automaticamente
```

### Seed Dados Demo
```batch
docker exec logiflow_api python scripts/seed_demo_data.py

# Cria:
# - Empresa: LogiFlow Demo BETA
# - Admin: admin@logiflow.demo / admin123
# - Operador: operador@logiflow.demo / operador123
# - 3 Motoristas, 3 Veículos, 3 Clientes
# - 1 Cotação, 1 Pedido, 1 Entrega demo
```

### Smoke Test
```batch
scripts\run-smoke-test.bat

# Ou direto:
docker exec logiflow_api python tests/smoke_test_beta.py

# Testa:
# - Backend health
# - Database
# - Redis
# - Feature flags
# - Autenticação
# - Criar cotação
# - GPS simulação
# - Frontend (se rodando)
```

---

## 📊 FEATURES DISPONÍVEIS NO BETA

### ✅ HABILITADAS (Core)
- **AUTH** - Autenticação e Login
- **DASHBOARD** - Dashboard principal
- **COTACOES** - Criação e gestão de cotações
- **PEDIDOS_FRETE** - Pedidos de frete
- **CLIENTES** - Gestão de clientes

### 🧪 BETA (Em Teste)
- **MOTORISTAS** - Cadastro de motoristas
- **VEICULOS** - Gestão de frota
- **ENTREGAS** - Rastreamento de entregas
- **OCORRENCIAS** - Registro de ocorrências
- **MELHOR_ENVIO** - Cotação de frete
- **FRENET** - Cotação alternativa
- **COTACAO_AUTOMATICA** - Comparação automática
- **NPS** - Pesquisas NPS
- **CSAT** - Satisfação do cliente
- **HEALTH_SCORE** - Score de saúde
- **MERCADO_PAGO** - Pagamentos
- **SUITECRM_SYNC** - Sincronização SuiteCRM

### 🔬 SIMULAÇÃO (Sem Integrações Reais)
- **GPS_TRACKING** - Rastreamento GPS (dados simulados)
- **GPS_SASCAR** - Sascar (simulação)
- **GPS_AUTOTRAC** - Autotrac (simulação)
- **GPS_ONIXSAT** - Onixsat (simulação)
- **FISCAL_CTE** - Emissão CT-e (sandbox)
- **FISCAL_MDFE** - Emissão MDF-e (sandbox)
- **FOCUS_NFE** - Focus NFe (sandbox)
- **WHATSAPP** - WhatsApp (simulação)
- **EMAIL_SMTP** - Email (mock)

### 🚫 DESABILITADAS (Pós-Beta)
- **ERP_OMIE** - Integração Omie ERP
- **ERP_BLING** - Integração Bling ERP
- **ERP_TINY** - Integração Tiny ERP
- **ERP_SYNC_AUTO** - Sincronização automática ERP

---

## 🌐 URLS DE ACESSO

### Backend
- **API Docs**: http://localhost:8000/api/v1/docs
- **Health Check**: http://localhost:8000/health
- **Feature Flags**: http://localhost:8000/api/v1/features

### SuiteCRM
- **URL**: http://localhost:8080
- **Login**: admin / admin123

### Frontend (se rodando)
- **URL**: http://localhost:3001
- **Login**: admin@logiflow.demo / admin123

### Database (Adminer - se rodando)
- **URL**: http://localhost:8082
- **Server**: db
- **Username**: logiflow
- **Password**: logiflow123
- **Database**: logiflow_crm

---

## 🔧 TROUBLESHOOTING RÁPIDO

### Backend não sobe
```bash
# Ver logs
docker logs logiflow_api

# Verificar .env
cat backend/.env | grep SUITECRM

# Reiniciar
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml restart api
```

### OAuth2 falha
```bash
# Testar manualmente
curl http://localhost:8080/legacy/Api/access_token

# Verificar SuiteCRM
curl http://localhost:8080/index.php

# Recriar OAuth2 Client
# Admin → OAuth2 Clients → Create New
```

### Dados demo não criam
```bash
# Verificar tabelas existem
docker exec logiflow_api python -c "from database import engine; print(engine.table_names())"

# Limpar e recriar
docker exec -it logiflow_api bash
python scripts/seed_demo_data.py
```

### Smoke test falha
```bash
# Verificar serviços
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml ps

# Testar individualmente
curl http://localhost:8000/health
curl http://localhost:8080/index.php
docker exec logiflow_db mysql -u root -p"rootpass123" -e "SELECT 1"
```

---

## 📞 SUPORTE TÉCNICO

### Logs Importantes
```bash
# Backend
docker logs -f logiflow_api

# SuiteCRM
docker logs -f logiflow_suitecrm

# Nginx
docker logs -f logiflow_nginx

# Database
docker logs -f logiflow_db
```

### Comandos Úteis
```bash
# Status geral
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml ps

# Restart completo
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml restart

# Rebuild backend
docker compose -f docker/docker-compose.yml -f docker compose -f docker/docker-compose.yml.minimal.yml up -d --build api

# Acessar container
docker exec -it logiflow_api bash
```

---

## ✅ CONFIRMAÇÃO FINAL

### Sistema está pronto para BETA quando:

```
✅ OAuth2 configurado
✅ Dados demo criados
✅ Smoke test 100% passando
✅ Feature flags ativos
✅ Docker rodando sem erros
✅ Documentação disponível
✅ Suporte técnico preparado
```

### Comando Final de Validação:
```bash
scripts\run-smoke-test.bat
```

**Se todos os testes passarem:** 🎉 **SISTEMA PRONTO PARA BETA!**

---

**Última Atualização**: 30/12/2024  
**Responsável**: Principal Software Engineer  
**Versão**: 1.0.0-beta
