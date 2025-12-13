# 📱 Evolution API - Configuração LogiFlow

Guia para configurar a Evolution API para integração WhatsApp com LogiFlow CRM.

## 🚀 Início Rápido

### Passo 1: Iniciar o Container

```bash
cd evolution-api
docker compose up -d
```

### Passo 2: Verificar se está rodando

```bash
docker logs evolution_api
```

Deve mostrar algo como:
```
Evolution API is running on port 8080
```

### Passo 3: Acessar a API

Abra no navegador: http://localhost:8080

---

## 🔧 Configuração no LogiFlow

### Atualizar o `.env` do backend:

```env
# WhatsApp / Evolution API
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=logiflow-evolution-key-2025
EVOLUTION_INSTANCE_NAME=logiflow
```

> ⚠️ **IMPORTANTE:** Em produção, mude a `AUTHENTICATION_API_KEY` no docker-compose.yml!

---

## 📲 Conectar WhatsApp

### Via API do LogiFlow:

```bash
# 1. Criar instância
curl -X POST http://localhost:8000/whatsapp/instancia/criar

# 2. Obter QR Code
curl http://localhost:8000/whatsapp/qrcode
```

### Via API Evolution diretamente:

```bash
# 1. Criar instância
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: logiflow-evolution-key-2025" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "logiflow",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS"
  }'

# 2. Obter QR Code
curl http://localhost:8080/instance/connect/logiflow \
  -H "apikey: logiflow-evolution-key-2025"
```

### Passo 4: Escanear QR Code

1. Abra o WhatsApp no celular
2. Vá em **Configurações** → **Dispositivos Conectados**
3. Toque em **Conectar Dispositivo**
4. Escaneie o QR Code

### Passo 5: Verificar Conexão

```bash
curl http://localhost:8000/whatsapp/status
```

Resposta esperada:
```json
{
  "success": true,
  "data": {
    "state": "open"
  }
}
```

---

## 📤 Testar Envio de Mensagem

```bash
curl -X POST http://localhost:8000/whatsapp/enviar/texto \
  -H "Content-Type: application/json" \
  -d '{
    "telefone": "11999999999",
    "mensagem": "Teste LogiFlow! 🚛"
  }'
```

---

## 🔔 Webhook (Receber Mensagens)

O webhook já está configurado para enviar eventos para:
```
http://host.docker.internal:8000/whatsapp/webhook
```

Eventos configurados:
- ✅ QR Code atualizado
- ✅ Mensagens recebidas
- ✅ Mensagens enviadas
- ✅ Status de conexão

---

## 🛠️ Comandos Úteis

```bash
# Ver logs
docker logs -f evolution_api

# Reiniciar
docker compose restart

# Parar
docker compose down

# Parar e remover dados
docker compose down -v

# Atualizar imagem
docker compose pull
docker compose up -d
```

---

## ⚠️ Troubleshooting

### QR Code não aparece
```bash
# Reiniciar instância
curl -X DELETE http://localhost:8080/instance/logout/logiflow \
  -H "apikey: logiflow-evolution-key-2025"

curl http://localhost:8080/instance/connect/logiflow \
  -H "apikey: logiflow-evolution-key-2025"
```

### Conexão cai frequentemente
- Não use o mesmo número em outro dispositivo
- Mantenha o celular conectado à internet
- Verifique se não está usando WhatsApp Web em outro lugar

### Webhook não funciona
- Verifique se o backend LogiFlow está rodando na porta 8000
- Teste a URL do webhook manualmente

---

## 📚 Links Úteis

- [Documentação Evolution API](https://doc.evolution-api.com/)
- [GitHub Evolution API](https://github.com/EvolutionAPI/evolution-api)
- [Variáveis de Ambiente](https://doc.evolution-api.com/pt/install/env)

---

*LogiFlow CRM - Integração WhatsApp v1.0*
