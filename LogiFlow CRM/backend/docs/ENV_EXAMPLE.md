# LogiFlow CRM - Exemplo de Variáveis de Ambiente (.env)

```
# App
DEBUG=true
SECRET_KEY=change-this-in-production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
API_PREFIX=/api
API_VERSION=v1

# Database (SQLite default se não setar)
DB_HOST=db
DB_NAME=logiflow_crm
DB_USER=logiflow
DB_PASSWORD=logiflow123
DB_PORT=3306

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis123

# SuiteCRM
SUITECRM_URL=http://logiflow_suitecrm:8080
SUITECRM_CLIENT_ID=
SUITECRM_CLIENT_SECRET=

# Focus NFe
FOCUSNFE_TOKEN=

# WhatsApp / Evolution API
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE_NAME=logiflow

# Google Maps
GOOGLE_MAPS_API_KEY=
GOOGLE_MAPS_DISTANCE_MATRIX_KEY=

# Pagamentos (Mercado Pago)
MERCADOPAGO_ACCESS_TOKEN=
MERCADOPAGO_PUBLIC_KEY=
CHECKOUT_SUCCESS_URL=http://localhost:3001/checkout/success
CHECKOUT_FAILURE_URL=http://localhost:3001/checkout/failure
CHECKOUT_PENDING_URL=http://localhost:3001/checkout/pending

# Frete
MELHOR_ENVIO_TOKEN=
MELHOR_ENVIO_SANDBOX=true
FRENET_TOKEN=

# Criptografia de credenciais por tenant
CREDENTIALS_ENCRYPTION_KEY=
```

