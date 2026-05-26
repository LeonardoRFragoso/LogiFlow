# 📱 Configuração WhatsApp / Evolution API

Este guia explica como configurar a integração do LogiFlow CRM com WhatsApp usando Evolution API.

## 📋 Pré-requisitos

- Docker instalado
- Número de WhatsApp dedicado (recomendado chip empresarial)
- VPS ou servidor para produção (opcional para testes locais)

---

## 🚀 Passo 1: Instalar Evolution API

### Opção A: Docker (Recomendado)

```bash
# Criar pasta
mkdir evolution-api && cd evolution-api

# Criar docker compose -f docker/docker-compose.yml
cat > docker compose -f docker/docker-compose.yml << 'EOF'
version: '3.8'

services:
  evolution-api:
    image: atendai/evolution-api:latest
    container_name: evolution_api
    restart: always
    ports:
      - "8080:8080"
    environment:
      - SERVER_URL=http://localhost:8080
      - AUTHENTICATION_API_KEY=sua-chave-api-aqui
      - AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=true
      - DATABASE_ENABLED=true
      - DATABASE_PROVIDER=postgresql
      - DATABASE_CONNECTION_URI=postgresql://postgres:postgres@postgres:5432/evolution
      - DATABASE_SAVE_DATA_INSTANCE=true
      - DATABASE_SAVE_DATA_NEW_MESSAGE=true
      - DATABASE_SAVE_MESSAGE_UPDATE=true
      - DATABASE_SAVE_DATA_CONTACTS=true
      - DATABASE_SAVE_DATA_CHATS=true
    volumes:
      - evolution_instances:/evolution/instances
    networks:
      - evolution-network
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    container_name: evolution_postgres
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=evolution
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - evolution-network

volumes:
  evolution_instances:
  postgres_data:

networks:
  evolution-network:
    driver: bridge
EOF

# Iniciar
docker compose -f docker/docker-compose.yml up -d
```

### Opção B: Usando apenas Evolution (sem banco)

```bash
docker run -d \
  --name evolution_api \
  -p 8080:8080 \
  -e AUTHENTICATION_API_KEY=sua-chave-api-aqui \
  atendai/evolution-api:latest
```

---

## 🔧 Passo 2: Configurar Credenciais

### 2.1 Definir API Key

Edite o arquivo `.env` do backend LogiFlow:

```env
# WhatsApp / Evolution API
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua-chave-api-aqui
EVOLUTION_INSTANCE_NAME=logiflow
```

### 2.2 Criar Instância

Acesse a API ou use o endpoint do LogiFlow:

```bash
# Via LogiFlow API
curl -X POST http://localhost:8000/whatsapp/instancia/criar

# Ou diretamente na Evolution
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: sua-chave-api-aqui" \
  -H "Content-Type: application/json" \
  -d '{"instanceName": "logiflow", "qrcode": true}'
```

---

## 📱 Passo 3: Conectar WhatsApp

### 3.1 Obter QR Code

```bash
curl http://localhost:8000/whatsapp/qrcode
```

Ou acesse diretamente: `http://localhost:8080/instance/connect/logiflow`

### 3.2 Escanear QR Code

1. Abra o WhatsApp no celular
2. Vá em **Configurações** → **Dispositivos Conectados**
3. Clique em **Conectar um dispositivo**
4. Escaneie o QR Code

### 3.3 Verificar Conexão

```bash
curl http://localhost:8000/whatsapp/status
```

Resposta esperada:
```json
{
  "success": true,
  "data": {
    "state": "open",
    "status": "connected"
  }
}
```

---

## 📤 Passo 4: Testar Envio

### Enviar mensagem de teste

```bash
curl -X POST http://localhost:8000/whatsapp/enviar/texto \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "11999999999",
    "mensagem": "Teste de integração LogiFlow! 🚛"
  }'
```

### Enviar notificação de pedido

```bash
curl -X POST http://localhost:8000/whatsapp/notificar/pedido \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "11999999999",
    "cliente_nome": "João Silva",
    "pedido_numero": "PED-2024-001234",
    "tipo": "pedido_confirmado",
    "codigo_rastreio": "LF1234567890",
    "previsao_entrega": "15/12/2024"
  }'
```

---

## 🔔 Passo 5: Configurar Webhook (Opcional)

Para receber mensagens e confirmações de entrega:

### 5.1 Configurar na Evolution API

```bash
curl -X POST http://localhost:8080/webhook/set/logiflow \
  -H "apikey: sua-chave-api-aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook": {
      "enabled": true,
      "url": "http://seu-servidor:8000/whatsapp/webhook",
      "webhookByEvents": true,
      "events": [
        "messages.upsert",
        "messages.update",
        "connection.update"
      ]
    }
  }'
```

---

## 📋 Tipos de Notificação Disponíveis

| Tipo | Descrição | Quando usar |
|------|-----------|-------------|
| `pedido_confirmado` | Pedido criado | Após confirmar pedido |
| `coleta_realizada` | Carga coletada | Motorista coletou |
| `em_transito` | Em trânsito | Carga saiu para destino |
| `saiu_entrega` | Saiu para entrega | Última milha |
| `entregue` | Entrega realizada | Pedido entregue |
| `ocorrencia` | Ocorrência registrada | Problema na entrega |
| `tentativa_falha` | Tentativa sem sucesso | Destinatário ausente |

---

## ⚠️ Boas Práticas

1. **Intervalo entre mensagens**: Mínimo 5 segundos para evitar bloqueio
2. **Horário de envio**: Evite mensagens entre 22h e 8h
3. **Conteúdo**: Mantenha mensagens informativas, não spam
4. **Opt-out**: Sempre ofereça opção de descadastro
5. **Backup**: Use número empresarial dedicado

---

## 🔧 Troubleshooting

### QR Code não aparece
```bash
# Reiniciar instância
curl -X DELETE http://localhost:8080/instance/logout/logiflow -H "apikey: sua-chave"
curl -X GET http://localhost:8080/instance/connect/logiflow -H "apikey: sua-chave"
```

### Mensagem não enviada
- Verifique se o número está no formato correto (apenas números)
- Confirme se o WhatsApp está conectado
- Verifique logs: `docker logs evolution_api`

### Conexão perdida frequentemente
- Não use o mesmo número em outro dispositivo
- Mantenha o celular com WhatsApp conectado à internet
- Considere usar WhatsApp Business API oficial para produção

---

## 📚 Documentação Adicional

- [Evolution API Docs](https://doc.evolution-api.com/)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)

---

*LogiFlow CRM - Integração WhatsApp v1.0*
