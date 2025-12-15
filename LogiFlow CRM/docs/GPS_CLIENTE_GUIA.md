# 🛰️ Guia de Configuração GPS para Clientes LogiFlow

## 📋 Visão Geral

Como cliente LogiFlow, você pode integrar seus próprios serviços de rastreamento GPS:
- **Sascar**
- **Autotrac**
- **Onixsat**
- **Outros providers GPS**

**⚠️ IMPORTANTE**: 
- Você precisa ter **contrato ativo** com o provider GPS
- Você precisará das **credenciais de API** fornecidas pelo provider
- A LogiFlow **NÃO fornece** serviços de rastreamento GPS
- A LogiFlow apenas **integra** seus sistemas existentes

---

## 🎯 Como Funciona

1. Você tem contrato com Sascar/Autotrac/Onixsat
2. Você solicita **credenciais de API** ao provider
3. Você configura essas credenciais no LogiFlow
4. O LogiFlow consulta automaticamente a API do provider
5. Você visualiza seus veículos em tempo real no LogiFlow

---

## 📞 Passo 1: Obter Credenciais do Provider

### **Sascar**
Contate o suporte técnico da Sascar e solicite:
- ✅ Acesso à API de integração
- ✅ API Key ou Token de autenticação
- ✅ Documentação da API (endpoints, formato de dados)
- ✅ URL da API (produção)

**Exemplo do que você receberá:**
```
API Key: sascar_123456789abcdef
Base URL: https://api.sascar.com.br/v1
```

---

### **Autotrac**
Contate o suporte da Autotrac e solicite:
- ✅ Usuário e senha para API
- ✅ Documentação técnica
- ✅ URL da API

**Exemplo:**
```
Username: seu_usuario
Password: sua_senha
Base URL: https://api.autotrac.com.br/v2
```

---

### **Onixsat**
Contate a Onixsat e solicite:
- ✅ Token de API
- ✅ Documentação
- ✅ URL da API

**Exemplo:**
```
API Token: onix_token_abc123
Base URL: https://api.onixsat.com.br
```

---

## ⚙️ Passo 2: Configurar no LogiFlow

### **Via Interface Web** (Recomendado)

1. Acesse: **Configurações → Integrações → GPS**
2. Clique em **"Adicionar Provider GPS"**
3. Selecione o provider (Sascar/Autotrac/Onixsat)
4. Preencha as credenciais
5. Clique em **"Testar Conexão"**
6. Se funcionar, clique em **"Salvar"**

**Screenshot:**
```
┌─────────────────────────────────────────┐
│ Adicionar Provider GPS                  │
├─────────────────────────────────────────┤
│ Provider: [Sascar ▼]                    │
│                                         │
│ API Key: [sascar_123456789abcdef]      │
│ API Secret: [●●●●●●●●●●●●]             │
│ Base URL: [https://api.sascar.com...]  │
│                                         │
│ [Testar Conexão]  [Salvar]             │
└─────────────────────────────────────────┘
```

---

### **Via API** (Avançado)

```bash
POST /api/v1/tenant-credentials/credentials
Authorization: Bearer {seu_token}
Content-Type: application/json

{
  "integration_type": "gps",
  "provider": "sascar",
  "credentials": {
    "api_key": "sascar_123456789abcdef",
    "api_secret": "seu_secret",
    "base_url": "https://api.sascar.com.br/v1"
  },
  "custom_config": {
    "endpoints": {
      "list_vehicles": "/veiculos",
      "get_position": "/veiculos/{placa}/posicao"
    },
    "response_mapping": {
      "latitude": "lat",
      "longitude": "lng",
      "velocidade": "speed"
    }
  }
}
```

---

## 🧪 Passo 3: Testar a Integração

### **Teste Automático**

Após configurar, o sistema testa automaticamente:
1. ✅ Conexão com a API
2. ✅ Validade das credenciais
3. ✅ Acesso aos dados

**Se der erro:**
- Verifique se as credenciais estão corretas
- Verifique se a Base URL está correta
- Contate o suporte do provider GPS

---

### **Teste Manual**

1. Vá em: **GPS → Rastreamento**
2. Você verá seus veículos listados
3. Clique em um veículo para ver a posição em tempo real
4. Teste o histórico de rotas

---

## 📋 Configuração Avançada (Opcional)

Se a integração automática não funcionar perfeitamente, você pode **personalizar** os endpoints e mapeamento de campos:

### **Exemplo: Customizar Endpoints**

```json
{
  "endpoints": {
    "list_vehicles": "/meus-veiculos",
    "get_position": "/posicao/{placa}",
    "get_history": "/historico/{placa}"
  }
}
```

### **Exemplo: Mapear Campos da Resposta**

Se a API do seu provider retorna campos com nomes diferentes:

```json
{
  "response_mapping": {
    "latitude": "location.lat",
    "longitude": "location.lon",
    "velocidade": "speed_kmh",
    "data_hora": "last_update"
  }
}
```

---

## 🔍 Troubleshooting

### **Erro: "Conexão falhou"**
**Causa**: URL incorreta ou credenciais inválidas  
**Solução**: 
- Verifique a Base URL
- Teste as credenciais diretamente no site do provider
- Contate o suporte do provider

---

### **Erro: "Veículos não encontrados"**
**Causa**: Nenhum veículo cadastrado ou problema de permissão  
**Solução**:
- Verifique se há veículos cadastrados no provider
- Verifique permissões da API Key

---

### **Erro: "Formato de resposta inválido"**
**Causa**: A API do provider retorna dados em formato diferente  
**Solução**:
- Configure o `response_mapping` personalizado
- Ou contate o suporte LogiFlow com um exemplo da resposta

---

## 💡 Dicas

### **1. Use Ambiente de Testes Primeiro**
Muitos providers oferecem ambiente "sandbox" para testes:
```json
{
  "base_url": "https://sandbox.sascar.com.br/v1",
  "environment": "sandbox"
}
```

### **2. Mantenha Credenciais Seguras**
- ✅ Nunca compartilhe suas credenciais
- ✅ Elas são criptografadas no banco de dados
- ✅ Use senhas fortes

### **3. Multiple Providers**
Você pode configurar múltiplos providers:
- Sascar para frota própria
- Autotrac para veículos terceirizados
- O LogiFlow consolida tudo em uma única interface

---

## 📞 Suporte

### **Problemas com Credenciais**
Contate o **suporte do seu provider GPS** (Sascar/Autotrac/Onixsat)

### **Problemas com a Integração**
Contate o **suporte LogiFlow**:
- Email: suporte@logiflow.com.br
- Inclua: nome do provider, erro exato, exemplo de resposta da API

---

## ✅ Checklist de Configuração

- [ ] Tenho contrato ativo com provider GPS
- [ ] Obtive as credenciais de API
- [ ] Testei as credenciais no site do provider
- [ ] Configurei no LogiFlow
- [ ] Teste de conexão passou
- [ ] Consigo ver meus veículos
- [ ] Posições estão sendo atualizadas

---

## 🎯 Próximos Passos

Após configurar GPS:
1. Configure **alertas** de posição
2. Configure **webhooks** para notificações em tempo real
3. Integre com **rotas de entrega**
4. Configure **cercas eletrônicas** (geofences)

---

**Configuração concluída!** 🎉

Seus veículos agora são rastreados automaticamente no LogiFlow!

