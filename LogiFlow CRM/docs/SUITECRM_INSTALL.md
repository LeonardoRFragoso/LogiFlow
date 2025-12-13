# 🚀 Instalação do SuiteCRM - LogiFlow CRM

## Pré-requisitos

- Docker Desktop instalado e rodando
- Mínimo 4GB RAM disponível
- Portas 8080 e 3306 livres

## Instalação Rápida

### 1. Iniciar os containers

```powershell
cd "LogiFlow CRM"
docker compose -f docker-compose.suitecrm.yml up -d
```

### 2. Aguardar inicialização

A primeira inicialização pode demorar **3-5 minutos**. Acompanhe:

```powershell
docker logs -f logiflow_suitecrm
```

Aguarde até ver: `suitecrm is ready`

### 3. Acessar o SuiteCRM

- **URL:** http://localhost:8080
- **Usuário:** `admin`
- **Senha:** `LogiFlow@2025`

---

## Configuração OAuth2 (API)

### 1. Acessar Admin > OAuth2 Clients

No SuiteCRM, vá em:
- Admin → OAuth2 Clients and Tokens → New OAuth2 Client

### 2. Criar Client para LogiFlow

Preencha:
- **Name:** `LogiFlow CRM API`
- **Secret:** (gere um ou use) `logiflow-secret-2025`
- **Redirect URI:** `http://localhost:8000/auth/callback`
- **Allowed Grant Types:** ✅ Client Credentials, ✅ Password

### 3. Salvar e copiar credenciais

Após salvar, copie:
- **Client ID:** (gerado automaticamente)
- **Client Secret:** `logiflow-secret-2025`

### 4. Configurar no Backend

Edite o arquivo `.env` do backend:

```env
SUITECRM_URL=http://localhost:8080
SUITECRM_CLIENT_ID=<cole-o-client-id>
SUITECRM_CLIENT_SECRET=logiflow-secret-2025
```

---

## Comandos Úteis

```powershell
# Iniciar
docker compose -f docker-compose.suitecrm.yml up -d

# Parar
docker compose -f docker-compose.suitecrm.yml down

# Ver logs
docker logs -f logiflow_suitecrm

# Reiniciar
docker compose -f docker-compose.suitecrm.yml restart

# Remover tudo (incluindo dados)
docker compose -f docker-compose.suitecrm.yml down -v
```

---

## Credenciais Padrão

| Item | Valor |
|------|-------|
| URL | http://localhost:8080 |
| Admin User | `admin` |
| Admin Password | `LogiFlow@2025` |
| Database Host | `suitecrm_db` |
| Database Name | `suitecrm` |
| Database User | `suitecrm` |
| Database Password | `suitecrm123` |

---

## Troubleshooting

### Container não inicia
```powershell
# Verificar se portas estão livres
netstat -an | findstr 8080
netstat -an | findstr 3306

# Reiniciar Docker Desktop
```

### Erro de conexão com banco
```powershell
# Verificar se db está healthy
docker ps

# Aguardar db ficar ready
docker logs logiflow_suitecrm_db
```

### Resetar instalação
```powershell
docker compose -f docker-compose.suitecrm.yml down -v
docker compose -f docker-compose.suitecrm.yml up -d
```

---

## Próximos Passos

1. ✅ SuiteCRM instalado
2. ⏳ Configurar OAuth2
3. ⏳ Importar módulos customizados
4. ⏳ Configurar webhooks
5. ⏳ Testar integração com backend

---

*Documentação LogiFlow CRM - 2025*
