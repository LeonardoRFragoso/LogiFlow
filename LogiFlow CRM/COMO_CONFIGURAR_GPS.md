# ⚡ Como Configurar GPS - Guia Rápido para Clientes LogiFlow

## 📋 O que você precisa saber

✅ Você **JÁ TEM** contrato com Sascar/Autotrac/Onixsat?  
✅ Você **TEM** acesso às credenciais de API deles?  
✅ LogiFlow vai **integrar** seu sistema GPS existente

---

## 🎯 Passo a Passo Rápido

### 1️⃣ Obter Credenciais do Provider

**Sascar:**
- Contate: suporte@sascar.com.br
- Peça: "Credenciais de API para integração"
- Você receberá: API Key + URL

**Autotrac:**
- Contate: suporte@autotrac.com.br
- Peça: "Acesso à API de rastreamento"
- Você receberá: Username + Password

**Onixsat:**
- Contate: contato@onixsat.com.br
- Peça: "Token de API"
- Você receberá: API Token

---

### 2️⃣ Configurar no LogiFlow

#### **Via Interface Web**

1. Acesse: **Configurações → Integrações → GPS**
2. Clique em **"Adicionar Provider"**
3. Selecione seu provider (Sascar/Autotrac/Onixsat)
4. Cole suas credenciais
5. Clique em **"Testar Conexão"**
6. Se passar ✅ clique em **"Salvar"**

#### **Via API** (Swagger)

1. Acesse: http://localhost:8000/docs
2. Encontre: `POST /api/v1/gps-config/test-connection`
3. Envie:
```json
{
  "provider": "sascar",
  "credentials": {
    "api_key": "sua_chave_aqui"
  }
}
```
4. Se funcionou, salve em: `POST /api/v1/gps-config/configure`

---

### 3️⃣ Usar o GPS

1. Vá em: **GPS → Rastreamento**
2. Veja seus veículos em tempo real
3. Clique em um veículo para ver detalhes
4. Acesse histórico de rotas

---

## 🆘 Dúvidas Comuns

**"Não tenho as credenciais"**  
→ Contate seu provider GPS (Sascar/Autotrac/Onixsat)

**"O teste falhou"**  
→ Verifique se as credenciais estão corretas  
→ Teste no site do provider primeiro

**"Não vejo meus veículos"**  
→ Verifique se há veículos cadastrados no provider  
→ Verifique permissões da API

---

## 📞 Suporte

**Problemas com credenciais?**  
→ Contate o provider GPS

**Problemas com integração?**  
→ Contate: suporte@logiflow.com.br

---

**Pronto!** 🎉  
Seus veículos agora aparecem no LogiFlow!

