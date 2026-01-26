# 💬 Configuração Evolution API - WhatsApp - LogiFlow CRM

## 📋 O que é Evolution API?

Evolution API é uma API open-source para integração com WhatsApp, permitindo enviar mensagens, receber webhooks e criar chatbots.

**Funcionalidades no LogiFlow:**
- ✅ Envio de mensagens (texto, imagem, documento, localização)
- ✅ Notificações automáticas de pedidos
- ✅ Atualização de status para motoristas
- ✅ Chatbot para consulta de rastreamento
- ✅ Histórico de conversas no CRM
- ✅ Webhooks de mensagens recebidas

---

## 🚀 Opções de Instalação

### Opção 1: Evolution API Cloud (Recomendado)

Serviço hospedado oficial - mais fácil e rápido.

1. Acesse: https://evolution-api.com
2. Crie uma conta
3. Crie uma instância
4. Obtenha credenciais

**Vantagens:**
- ✅ Sem necessidade de servidor
- ✅ Atualizações automáticas
- ✅ Suporte oficial
- ✅ Alta disponibilidade

**Custos:**
- Starter: $9.90/mês (1 instância)
- Pro: $29.90/mês (5 instâncias)
- Enterprise: Custom

### Opção 2: Self-Hosted com Docker (Gratuito)

Instale em seu próprio servidor.

#### Pré-requisitos:
- VPS com Ubuntu 20.04+
- Docker e Docker Compose
- Domínio com SSL (Let's Encrypt)
- 2GB RAM mínimo

#### Instalação Rápida:

```bash
# 1. Clonar repositório
git clone https://github.com/EvolutionAPI/evolution-api.git
cd evolution-api

# 2. Configurar .env
cp .env.example .env
nano .env

# Editar:
AUTHENTICATION_API_KEY=CRIE_UMA_CHAVE_FORTE_AQUI
SERVER_URL=https://api.seudominio.com.br
CORS_ORIGIN=*
CORS_CREDENTIALS=true

# 3. Subir containers
docker-compose up -d

# 4. Verificar logs
docker-compose logs -f
```

A API estará disponível em: `http://localhost:8080`

**⚠️ IMPORTANTE:** Configure SSL com Nginx Reverse Proxy!

---

## 🔧 Configuração no LogiFlow

### 1. Obter Credenciais

#### Evolution API Cloud:

1. Faça login no painel
2. Vá em **"API Keys"**
3. Copie:
   - **API Key:** `evo_123abc...`
   - **Instance Name:** `logiflow-prod`
   - **API URL:** `https://api.evolution-api.com`

#### Self-Hosted:

1. A API Key é a definida no `.env`: `AUTHENTICATION_API_KEY`
2. Instance Name: será criado no próximo passo
3. API URL: `https://api.seudominio.com.br`

### 2. Criar Instância

```bash
curl -X POST https://api.evolution-api.com/instance/create \
  -H "apikey: SUA_API_KEY_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "logiflow-prod",
    "token": "OUTRO_TOKEN_FORTE_AQUI",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS"
  }'
```

Resposta:
```json
{
  "instance": {
    "instanceName": "logiflow-prod",
    "status": "created"
  },
  "qrcode": {
    "code": "1@abc123...",
    "base64": "data:image/png;base64,iVBORw0KG..."
  }
}
```

### 3. Conectar WhatsApp

#### Via QR Code:

1. Abra WhatsApp no celular
2. Vá em **Dispositivos Conectados**
3. Toque em **Conectar um dispositivo**
4. Escaneie o QR Code retornado

#### Ou via Painel Web:

Acesse: `https://api.evolution-api.com/manager`

### 4. Configurar Webhook

```bash
curl -X POST https://api.evolution-api.com/webhook/set/logiflow-prod \
  -H "apikey: SUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://api.logiflow.com.br/api/v1/whatsapp/webhook",
    "webhook_by_events": true,
    "events": [
      "MESSAGES_UPSERT",
      "MESSAGES_UPDATE",
      "CONNECTION_UPDATE"
    ]
  }'
```

### 5. Configurar Variáveis no LogiFlow

Edite `.env`:

```bash
# Evolution API - WhatsApp
EVOLUTION_API_URL=https://api.evolution-api.com
EVOLUTION_API_KEY=evo_123abc456def789ghi012jkl345mno678pqr901stu234
EVOLUTION_INSTANCE_NAME=logiflow-prod
```

---

## ✅ Validação

### Teste 1: Verificar Conexão

```bash
docker-compose exec backend python -c "
import os
import requests

api_url = os.getenv('EVOLUTION_API_URL')
api_key = os.getenv('EVOLUTION_API_KEY')
instance = os.getenv('EVOLUTION_INSTANCE_NAME')

response = requests.get(
    f'{api_url}/instance/connectionState/{instance}',
    headers={'apikey': api_key}
)

print(f'Status: {response.status_code}')
print(f'Resposta: {response.json()}')
"
```

Resposta esperada:
```json
{
  "instance": "logiflow-prod",
  "state": "open"
}
```

### Teste 2: Enviar Mensagem de Teste

Crie `test_whatsapp.py`:

```python
import sys
sys.path.append('/app')

from services.whatsapp_service import whatsapp_service

# IMPORTANTE: Substitua pelo seu número!
numero_teste = "5511999999999"  # Formato: DDI + DDD + Número

resultado = whatsapp_service.send_text_message(
    phone_number=numero_teste,
    message="🧪 Teste LogiFlow CRM - WhatsApp funcionando!"
)

if resultado["success"]:
    print("✅ Mensagem enviada com sucesso!")
else:
    print(f"❌ Erro: {resultado.get('error')}")
```

Execute:
```bash
docker-compose exec backend python test_whatsapp.py
```

### Teste 3: Webhook

1. Envie uma mensagem para o WhatsApp conectado
2. Verifique os logs:

```bash
docker-compose logs -f backend | grep "WhatsApp"
```

Deve aparecer:
```
📩 Webhook WhatsApp recebido: MESSAGES_UPSERT
✅ Mensagem processada
```

---

## 🚨 Troubleshooting

### Erro: "Instance not found"

**Causa:** Nome da instância incorreto ou não criada

**Solução:**
```bash
# Listar instâncias
curl https://api.evolution-api.com/instance/fetchInstances \
  -H "apikey: SUA_API_KEY"
```

### Erro: "WhatsApp disconnected"

**Causa:** WhatsApp desconectado do celular

**Solução:**
1. Gere novo QR Code:
```bash
curl https://api.evolution-api.com/instance/connect/logiflow-prod \
  -H "apikey: SUA_API_KEY"
```
2. Escaneie novamente no celular

### Erro: "Message not sent - rate limit"

**Causa:** Muitas mensagens em pouco tempo

**Solução:**
- WhatsApp limita: ~1000 mensagens/dia
- Adicione delay entre mensagens
- Considere WhatsApp Business API oficial

### Webhook não funciona

**Causas Comuns:**

1. **URL não acessível:**
   ```bash
   # Testar de fora
   curl https://api.logiflow.com.br/api/v1/whatsapp/webhook
   ```

2. **SSL inválido:**
   - Evolution API requer HTTPS válido
   - Teste em: https://www.ssllabs.com/ssltest/

3. **Firewall bloqueando:**
   - Libere IP da Evolution API
   - Ou use `0.0.0.0/0` (menos seguro)

**Testar webhook manualmente:**
```bash
curl -X POST https://api.logiflow.com.br/api/v1/whatsapp/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "messages.upsert",
    "instance": "logiflow-prod",
    "data": {
      "key": {
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": false
      },
      "message": {
        "conversation": "Teste"
      }
    }
  }'
```

---

## 📊 Recursos Avançados

### 1. Templates de Mensagens

Já implementados em `backend/services/whatsapp_service.py`:

```python
# Notificação de pedido confirmado
whatsapp_service.notify_order_confirmed(
    phone="5511999999999",
    customer_name="João Silva",
    order_code="PED-12345",
    estimated_date="25/01/2026"
)

# Notificação de coleta realizada
whatsapp_service.notify_pickup_completed(
    phone="5511999999999",
    order_code="PED-12345"
)

# Notificação de entrega
whatsapp_service.notify_delivery_completed(
    phone="5511999999999",
    order_code="PED-12345"
)
```

### 2. Envio de Arquivos

```python
# Imagem
whatsapp_service.send_image(
    phone="5511999999999",
    image_url="https://exemplo.com/comprovante.jpg",
    caption="Comprovante de entrega"
)

# PDF
whatsapp_service.send_document(
    phone="5511999999999",
    document_url="https://exemplo.com/cte.pdf",
    filename="CT-e-12345.pdf"
)
```

### 3. Localização

```python
whatsapp_service.send_location(
    phone="5511999999999",
    latitude=-23.550520,
    longitude=-46.633308,
    name="Sua entrega chegou!",
    address="Avenida Paulista, 1578"
)
```

### 4. Chatbot Simples

Já implementado em `backend/services/chatbot_service.py`:

**Comandos suportados:**
- "rastrear PED-12345" → Retorna status da entrega
- "onde está minha carga" → Solicita código
- "previsão" → Retorna data estimada
- "falar com humano" → Escalona para atendente

---

## 💡 Boas Práticas

### 1. Rate Limiting

```python
# Adicionar delay entre mensagens
import time

for cliente in clientes:
    whatsapp_service.send_text_message(...)
    time.sleep(1)  # 1 segundo entre mensagens
```

### 2. Opt-in/Opt-out

```python
# Verificar se cliente aceitou receber mensagens
if cliente.whatsapp_opt_in:
    whatsapp_service.send_text_message(...)
```

### 3. Horário Comercial

```python
from datetime import datetime

now = datetime.now()
if 8 <= now.hour < 22:  # Das 8h às 22h
    whatsapp_service.send_text_message(...)
else:
    # Agendar para manhã seguinte
    pass
```

### 4. Monitoramento

```bash
# Logs de WhatsApp
docker-compose logs backend | grep "WhatsApp" | tail -100

# Mensagens enviadas hoje
docker-compose exec backend python -c "
from database import SessionLocal
from models import WhatsAppMessage
from datetime import datetime, timedelta

db = SessionLocal()
hoje = datetime.now().date()

count = db.query(WhatsAppMessage).filter(
    WhatsAppMessage.created_at >= hoje
).count()

print(f'Mensagens enviadas hoje: {count}')
"
```

---

## 🎯 Checklist de Produção

- [ ] Evolution API instalada/contratada
- [ ] Instância criada
- [ ] WhatsApp conectado via QR Code
- [ ] Webhook configurado
- [ ] URL pública acessível (HTTPS)
- [ ] Variáveis configuradas no `.env`
- [ ] Teste de envio funcionando
- [ ] Teste de recebimento (webhook) funcionando
- [ ] Templates personalizados
- [ ] Rate limiting implementado
- [ ] Opt-in/opt-out configurado
- [ ] Monitoramento ativo

---

## 📞 Suporte

**Evolution API:**
- GitHub: https://github.com/EvolutionAPI/evolution-api
- Documentação: https://doc.evolution-api.com
- Discord: https://discord.gg/evolutionapi
- Email: contato@evolution-api.com

**WhatsApp Business API Oficial:**
- Para alto volume (>10k mensagens/dia)
- Meta Business: https://business.facebook.com/products/whatsapp

**LogiFlow CRM:**
- Código: `backend/services/whatsapp_service.py`
- Router: `backend/routers/whatsapp.py`
- Chatbot: `backend/services/chatbot_service.py`

---

**Última atualização:** 23 de Janeiro de 2026
