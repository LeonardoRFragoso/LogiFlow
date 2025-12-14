# 🚀 Guia de Deploy em Produção - LogiFlow CRM

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Infraestrutura](#infraestrutura)
3. [Configuração do Servidor](#configuração-do-servidor)
4. [Deploy do Backend](#deploy-do-backend)
5. [Deploy do Frontend](#deploy-do-frontend)
6. [Deploy do Site](#deploy-do-site)
7. [Configuração de DNS](#configuração-de-dns)
8. [SSL/HTTPS](#sslhttps)
9. [Monitoramento](#monitoramento)
10. [Backup](#backup)
11. [Checklist Final](#checklist-final)

---

## 🔧 Pré-requisitos

### Servidores Necessários

- **1x Servidor de Aplicação** (Backend + Frontend)
  - CPU: 4 cores
  - RAM: 8GB
  - Storage: 100GB SSD
  - OS: Ubuntu 22.04 LTS

- **1x Servidor de Banco de Dados** (PostgreSQL + MySQL)
  - CPU: 4 cores
  - RAM: 16GB
  - Storage: 200GB SSD
  - OS: Ubuntu 22.04 LTS

- **1x Servidor Redis** (Cache)
  - CPU: 2 cores
  - RAM: 4GB
  - Storage: 20GB SSD

### Domínios

- `logiflow.com.br` - Site institucional
- `app.logiflow.com.br` - Aplicação (Frontend)
- `api.logiflow.com.br` - API (Backend)

### Contas Necessárias

- [ ] Mercado Pago (conta de produção)
- [ ] AWS (S3 para arquivos)
- [ ] Google Cloud (Maps API)
- [ ] Sentry (monitoramento de erros)
- [ ] Email SMTP (Gmail ou SendGrid)

---

## 🏗️ Infraestrutura

### Arquitetura Recomendada

```
Internet
   │
   ├─── Cloudflare (CDN + DDoS Protection)
   │
   ├─── logiflow.com.br (Site)
   │    └─── Nginx → Site Vue.js (porta 80/443)
   │
   ├─── app.logiflow.com.br (Frontend)
   │    └─── Nginx → Frontend Vue.js (porta 80/443)
   │
   └─── api.logiflow.com.br (Backend)
        └─── Nginx → FastAPI (porta 8000)
             │
             ├─── PostgreSQL (porta 5432)
             ├─── MySQL (porta 3306)
             └─── Redis (porta 6379)
```

---

## ⚙️ Configuração do Servidor

### 1. Atualizar Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependências

```bash
# Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Nginx
sudo apt install nginx -y

# Certbot (SSL)
sudo apt install certbot python3-certbot-nginx -y

# Git
sudo apt install git -y

# Supervisor (gerenciador de processos)
sudo apt install supervisor -y
```

### 3. Criar Usuário de Deploy

```bash
sudo adduser logiflow
sudo usermod -aG sudo logiflow
su - logiflow
```

---

## 🔙 Deploy do Backend

### 1. Clonar Repositório

```bash
cd /home/logiflow
git clone https://github.com/seu-usuario/logiflow-crm.git
cd logiflow-crm/backend
```

### 2. Configurar Ambiente Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

```bash
cp .env.production.example .env
nano .env
```

**Editar com valores reais**:
- `DATABASE_URL` - PostgreSQL de produção
- `MERCADOPAGO_ACCESS_TOKEN` - Token de produção
- `SECRET_KEY` - Gerar com: `openssl rand -hex 32`
- Demais variáveis conforme `.env.production.example`

### 4. Executar Migrações

```bash
source venv/bin/activate
alembic upgrade head
```

### 5. Configurar Supervisor

```bash
sudo nano /etc/supervisor/conf.d/logiflow-api.conf
```

```ini
[program:logiflow-api]
command=/home/logiflow/logiflow-crm/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/home/logiflow/logiflow-crm/backend
user=logiflow
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/logiflow/api.log
environment=PATH="/home/logiflow/logiflow-crm/backend/venv/bin"
```

```bash
sudo mkdir -p /var/log/logiflow
sudo chown logiflow:logiflow /var/log/logiflow
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start logiflow-api
```

### 6. Configurar Nginx para API

```bash
sudo nano /etc/nginx/sites-available/api.logiflow.com.br
```

```nginx
server {
    listen 80;
    server_name api.logiflow.com.br;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Limite de upload
    client_max_body_size 50M;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/api.logiflow.com.br /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🎨 Deploy do Frontend

### 1. Build do Frontend

```bash
cd /home/logiflow/logiflow-crm/frontend
npm install
```

Criar `.env.production`:
```bash
nano .env.production
```

```env
VITE_API_URL=https://api.logiflow.com.br
VITE_FRONTEND_URL=https://app.logiflow.com.br
```

```bash
npm run build
```

### 2. Configurar Nginx para Frontend

```bash
sudo nano /etc/nginx/sites-available/app.logiflow.com.br
```

```nginx
server {
    listen 80;
    server_name app.logiflow.com.br;
    root /home/logiflow/logiflow-crm/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache de assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_min_length 1000;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/app.logiflow.com.br /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🌐 Deploy do Site

### 1. Build do Site

```bash
cd /home/logiflow/logiflow-crm/site-divulgacao
npm install
```

Criar `.env.production`:
```bash
nano .env.production
```

```env
VITE_API_URL=https://api.logiflow.com.br
VITE_FRONTEND_URL=https://app.logiflow.com.br
```

```bash
npm run build
```

### 2. Configurar Nginx para Site

```bash
sudo nano /etc/nginx/sites-available/logiflow.com.br
```

```nginx
server {
    listen 80;
    server_name logiflow.com.br www.logiflow.com.br;
    root /home/logiflow/logiflow-crm/site-divulgacao/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache de assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    gzip_min_length 1000;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/logiflow.com.br /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🌍 Configuração de DNS

### Registros DNS Necessários

```
# Tipo  | Nome | Valor                    | TTL
A       | @    | IP_DO_SERVIDOR           | 3600
A       | www  | IP_DO_SERVIDOR           | 3600
A       | app  | IP_DO_SERVIDOR           | 3600
A       | api  | IP_DO_SERVIDOR           | 3600
CNAME   | www  | logiflow.com.br          | 3600
```

### Verificar Propagação

```bash
dig logiflow.com.br
dig app.logiflow.com.br
dig api.logiflow.com.br
```

---

## 🔒 SSL/HTTPS

### 1. Instalar Certificados SSL

```bash
# Site
sudo certbot --nginx -d logiflow.com.br -d www.logiflow.com.br

# Frontend
sudo certbot --nginx -d app.logiflow.com.br

# API
sudo certbot --nginx -d api.logiflow.com.br
```

### 2. Renovação Automática

```bash
# Testar renovação
sudo certbot renew --dry-run

# Cron já configurado automaticamente em:
# /etc/cron.d/certbot
```

### 3. Verificar SSL

```bash
curl -I https://api.logiflow.com.br
curl -I https://app.logiflow.com.br
curl -I https://logiflow.com.br
```

---

## 📊 Monitoramento

### 1. Configurar Sentry

No `.env` do backend:
```env
SENTRY_DSN=https://xxx@sentry.io/xxx
```

### 2. Logs

```bash
# Logs da API
sudo tail -f /var/log/logiflow/api.log

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs do Supervisor
sudo tail -f /var/log/supervisor/supervisord.log
```

### 3. Monitoramento de Recursos

```bash
# Instalar htop
sudo apt install htop -y

# Monitorar
htop
```

### 4. Uptime Monitoring

Configurar em serviços como:
- UptimeRobot
- Pingdom
- StatusCake

Monitorar:
- `https://api.logiflow.com.br/health`
- `https://app.logiflow.com.br`
- `https://logiflow.com.br`

---

## 💾 Backup

### 1. Script de Backup do Banco

```bash
sudo nano /home/logiflow/scripts/backup-db.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/logiflow/backups"
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
pg_dump -h localhost -U logiflow_user logiflow_prod | gzip > $BACKUP_DIR/postgres_$DATE.sql.gz

# Backup MySQL (tenants)
mysqldump --all-databases -u root -p$DB_ROOT_PASSWORD | gzip > $BACKUP_DIR/mysql_$DATE.sql.gz

# Upload para S3
aws s3 cp $BACKUP_DIR/postgres_$DATE.sql.gz s3://logiflow-prod-backups/
aws s3 cp $BACKUP_DIR/mysql_$DATE.sql.gz s3://logiflow-prod-backups/

# Limpar backups locais antigos (manter 7 dias)
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
```

```bash
chmod +x /home/logiflow/scripts/backup-db.sh
```

### 2. Agendar Backup (Cron)

```bash
crontab -e
```

```cron
# Backup diário às 2h da manhã
0 2 * * * /home/logiflow/scripts/backup-db.sh >> /var/log/logiflow/backup.log 2>&1
```

### 3. Testar Backup

```bash
/home/logiflow/scripts/backup-db.sh
```

---

## ✅ Checklist Final

### Pré-Deploy

- [ ] Código testado localmente
- [ ] Testes automatizados passando
- [ ] Variáveis de ambiente configuradas
- [ ] Credenciais de produção obtidas
- [ ] DNS configurado e propagado
- [ ] Servidores provisionados

### Deploy

- [ ] Backend deployado e rodando
- [ ] Frontend buildado e servido
- [ ] Site buildado e servido
- [ ] SSL configurado em todos os domínios
- [ ] Nginx configurado corretamente
- [ ] Supervisor gerenciando processos

### Pós-Deploy

- [ ] Endpoints da API respondendo
- [ ] Frontend carregando corretamente
- [ ] Site institucional acessível
- [ ] Webhook do Mercado Pago configurado
- [ ] Emails sendo enviados
- [ ] Logs sendo gerados
- [ ] Backup agendado
- [ ] Monitoramento ativo
- [ ] Sentry capturando erros

### Testes de Produção

- [ ] Criar lead pelo site
- [ ] Fazer checkout de plano
- [ ] Processar pagamento teste
- [ ] Verificar provisionamento de tenant
- [ ] Testar login no sistema
- [ ] Criar veículo/motorista/pedido
- [ ] Verificar limites de plano
- [ ] Testar upgrade de plano
- [ ] Verificar emails recebidos

---

## 🔄 Processo de Atualização

### Deploy de Nova Versão

```bash
cd /home/logiflow/logiflow-crm

# 1. Backup
/home/logiflow/scripts/backup-db.sh

# 2. Pull do código
git pull origin main

# 3. Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo supervisorctl restart logiflow-api

# 4. Frontend
cd ../frontend
npm install
npm run build

# 5. Site
cd ../site-divulgacao
npm install
npm run build

# 6. Verificar
curl https://api.logiflow.com.br/health
```

---

## 🆘 Troubleshooting

### API não responde

```bash
# Verificar status
sudo supervisorctl status logiflow-api

# Reiniciar
sudo supervisorctl restart logiflow-api

# Ver logs
sudo tail -f /var/log/logiflow/api.log
```

### Frontend não carrega

```bash
# Verificar Nginx
sudo nginx -t
sudo systemctl status nginx

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

### Banco de dados

```bash
# PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql

# MySQL
sudo systemctl status mysql
sudo mysql -u root -p
```

### SSL expirado

```bash
# Renovar manualmente
sudo certbot renew

# Verificar validade
openssl s_client -connect api.logiflow.com.br:443 -servername api.logiflow.com.br | openssl x509 -noout -dates
```

---

## 📞 Suporte

Em caso de problemas:
1. Verificar logs: `/var/log/logiflow/`
2. Verificar Sentry para erros
3. Contatar equipe de desenvolvimento

---

## 🎉 Deploy Completo!

Seu LogiFlow CRM está agora rodando em produção! 🚀

**URLs de Acesso**:
- Site: https://logiflow.com.br
- Aplicação: https://app.logiflow.com.br
- API: https://api.logiflow.com.br
- Docs API: https://api.logiflow.com.br/docs

**Próximos Passos**:
1. Monitorar logs nas primeiras 24h
2. Testar todos os fluxos críticos
3. Configurar alertas de uptime
4. Documentar procedimentos operacionais
5. Treinar equipe de suporte
