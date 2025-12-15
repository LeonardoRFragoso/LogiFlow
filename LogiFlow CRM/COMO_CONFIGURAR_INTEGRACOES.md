# ⚡ Como Configurar Integrações - Guia para Clientes LogiFlow

## 📋 Visão Geral

Como cliente LogiFlow, você pode integrar seus próprios serviços:

### 🗺️ **Google Maps**
- Calcular distâncias
- Estimar rotas
- Precificar fretes

### 🏢 **ERPs**
- **Omie**: Sincronizar clientes, produtos, pedidos
- **Bling**: Gestão de vendas e estoque

### 🛰️ **GPS** (Ver guia separado)
- Sascar, Autotrac, Onixsat

---

## 🎯 Processo Geral

```
1. Você tem conta no serviço (Google/Omie/Bling)
   ↓
2. Obtém credenciais de API
   ↓
3. Testa no LogiFlow
   ↓
4. Salva se funcionar ✅
   ↓
5. Usa normalmente!
```

---

## 🗺️ GOOGLE MAPS

### 1️⃣ Obter API Key

1. Acesse: https://console.cloud.google.com
2. Crie um projeto (ou selecione existente)
3. Vá em: **APIs & Services → Library**
4. Pesquise: **"Distance Matrix API"**
5. Clique em **"Enable"**
6. Vá em: **Credentials → Create Credentials → API Key**
7. Copie a API Key

**💡 Dica**: Restrinja a API Key para maior segurança!

### 2️⃣ Configurar no LogiFlow

**Via Swagger** (http://localhost:8000/docs):
```http
POST /api/v1/integrations-config/test/google-maps
{
  "integration_type": "maps",
  "credentials": {
    "api_key": "AIzaSyD..."
  }
}
```

Se retornar ✅ **success: true**, salve:
```http
POST /api/v1/integrations-config/configure
{
  "integration_type": "maps",
  "provider": "google_maps",
  "credentials": {
    "api_key": "AIzaSyD..."
  }
}
```

### 💰 Custo Google Maps
- **$0.005** por requisição
- **Free tier**: $200/mês (~40,000 requisições)

---

## 🏢 ERP OMIE

### 1️⃣ Obter Credenciais

1. Acesse: https://app.omie.com.br
2. Vá em: **Configurações → Integrações → API**
3. Clique em **"Criar Nova Integração"**
4. Anote:
   - **App Key**
   - **App Secret**

### 2️⃣ Testar no LogiFlow

```http
POST /api/v1/integrations-config/test/erp-omie
{
  "integration_type": "erp",
  "credentials": {
    "app_key": "1234567890",
    "app_secret": "abc123..."
  }
}
```

### 2️⃣ Salvar

```http
POST /api/v1/integrations-config/configure
{
  "integration_type": "erp",
  "provider": "omie",
  "credentials": {
    "app_key": "1234567890",
    "app_secret": "abc123..."
  }
}
```

---

## 🏢 ERP BLING

### 1️⃣ Obter API Key

1. Acesse: https://www.bling.com.br
2. Vá em: **Configurações → API**
3. Clique em **"Gerar Nova Chave"**
4. Copie a **API Key**

### 2️⃣ Testar no LogiFlow

```http
POST /api/v1/integrations-config/test/erp-bling
{
  "integration_type": "erp",
  "credentials": {
    "api_key": "sua_api_key_aqui"
  }
}
```

### 3️⃣ Salvar

```http
POST /api/v1/integrations-config/configure
{
  "integration_type": "erp",
  "provider": "bling",
  "credentials": {
    "api_key": "sua_api_key_aqui"
  }
}
```

---

## ✅ Ver Minhas Integrações

```http
GET /api/v1/integrations-config/my-integrations
X-Tenant-ID: {seu_tenant_id}
```

**Resposta:**
```json
{
  "success": true,
  "integrations": {
    "maps": [
      {
        "provider": "google_maps",
        "is_active": true,
        "created_at": "2025-12-15T10:00:00Z"
      }
    ],
    "erp": [
      {
        "provider": "omie",
        "is_active": true
      }
    ]
  }
}
```

---

## 🗑️ Remover Integração

```http
DELETE /api/v1/integrations-config/remove/maps/google_maps
```

---

## 🆘 Troubleshooting

### **Google Maps: "API not enabled"**
→ Habilite a Distance Matrix API no Google Cloud Console

### **Omie: "Invalid credentials"**
→ Verifique App Key e App Secret no painel Omie

### **Bling: "Unauthorized"**
→ Gere uma nova API Key no painel Bling

---

## 📊 Integrações Disponíveis

```http
GET /api/v1/integrations-config/supported
```

Lista todas as integrações que você pode configurar.

---

## 💡 Benefícios

✅ **Self-Service**: Configure sozinho  
✅ **Seguro**: Credenciais criptografadas  
✅ **Flexível**: Use seus próprios serviços  
✅ **Teste Antes**: Valide antes de salvar  
✅ **Multi-Provider**: Configure vários ao mesmo tempo

---

## 📞 Suporte

**Problemas com credenciais?**  
→ Contate o provedor (Google/Omie/Bling)

**Problemas com integração?**  
→ suporte@logiflow.com.br

---

**Pronto!** 🎉  
Suas integrações estão configuradas!

