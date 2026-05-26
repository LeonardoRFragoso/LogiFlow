# 📋 Empresas e Serviços para Integração Completa

Aqui está a lista completa de **empresas e credenciais** necessárias para que **TODAS as funcionalidades** do LogiFlow CRM funcionem 100%:

---

## 🏢 IMPORTANTE: Quem Contrata O Quê?

### **LogiFlow (Você) Contrata:**
- ✅ Google Maps API
- ✅ Focus NFe
- ✅ Evolution API

**Custo LogiFlow:** ~R$ 80/mês (fixo)

### **Cliente LogiFlow Configura (Opcional):**
- 🟡 **Frete** (Melhor Envio/Frenet) - Plano Pro+ - Cliente tem conta própria
- 🟢 **ERP** (Omie/Bling/Tiny) - Plano Pro+ - Cliente já usa
- 🔵 **GPS** (Sascar/Autotrac/Onixsat) - Plano Enterprise - Cliente tem frota rastreada

**Custo Cliente:** Variável (cada um paga seu próprio serviço)

**IMPORTANTE:** Melhor Envio e Frenet são do CLIENTE porque:
- Cada empresa tem sua própria conta e contratos
- Descontos negociados diretamente com transportadoras
- Cliente paga frete diretamente à transportadora
- Volumes e condições variam por cliente

---

## 🔴 CRÍTICAS (LogiFlow Precisa Contratar)

### 1. **Google Maps API** ⚠️
**O que é:** Cálculo de distâncias, rotas e mapas  
**Onde contratar:** https://cloud.google.com/maps-platform  
**O que precisa:**
- ✅ Criar conta Google Cloud
- ✅ Ativar APIs: Distance Matrix, Geocoding, Maps JavaScript
- ✅ Obter: `GOOGLE_MAPS_API_KEY`

**Custo:** ~US$ 5-20/mês (depende do uso)

---

### 2. **Focus NFe** ⚠️
**O que é:** Emissão de CT-e e MDF-e (documentos fiscais)  
**Onde contratar:** https://focusnfe.com.br  
**O que precisa:**
- ✅ Criar conta Focus NFe
- ✅ Obter: `FOCUSNFE_TOKEN`

**Custo:** ~R$ 50-150/mês (depende do volume)

---

### 3. **Evolution API (WhatsApp)** ⚠️
**O que é:** Envio de mensagens WhatsApp  
**Onde contratar:** https://evolution-api.com  
**O que precisa:**
- ✅ Instalar Evolution API (já está no Docker)
- ✅ Configurar: `EVOLUTION_API_URL` e `EVOLUTION_API_KEY`
- ✅ Conectar número WhatsApp

**Custo:** Gratuito (self-hosted) ou ~R$ 30/mês (cloud)

---

## 🟡 IMPORTANTES (Funcionalidades Avançadas)

### 4. **Melhor Envio** 
**O que é:** Cotação de frete com múltiplas transportadoras  
**Onde contratar:** https://melhorenvio.com.br  
**O que precisa:**
- ✅ Criar conta Melhor Envio
- ✅ Obter: `MELHOR_ENVIO_TOKEN`
- ✅ Configurar: `MELHOR_ENVIO_SANDBOX=false` (produção)

**Custo:** Gratuito (paga apenas o frete usado)

---

### 5. **Frenet**
**O que é:** Cotação de frete alternativa  
**Onde contratar:** https://frenet.com.br  
**O que precisa:**
- ✅ Criar conta Frenet
- ✅ Obter: `FRENET_TOKEN`

**Custo:** Gratuito (paga apenas o frete usado)

---

## 🟢 OPCIONAIS (Cliente Configura no LogiFlow)

### 6. **Omie ERP** (Opcional - Cliente Configura)
**O que é:** Integração com ERP Omie  
**Onde contratar:** https://omie.com.br  
**Quem contrata:** O cliente LogiFlow (se usar Omie)  
**O que precisa:**
- ✅ Cliente ter conta Omie ativa
- ✅ Cliente obter: `OMIE_APP_KEY` e `OMIE_APP_SECRET`
- ✅ Cliente inserir credenciais em: **Configurações → Integrações → ERP**

**Custo:** Cliente paga (depende do plano Omie)  
**Disponível em:** Plano Pro e Enterprise

---

### 7. **Bling ERP** (Opcional - Cliente Configura)
**O que é:** Integração com ERP Bling  
**Onde contratar:** https://bling.com.br  
**Quem contrata:** O cliente LogiFlow (se usar Bling)  
**O que precisa:**
- ✅ Cliente ter conta Bling ativa
- ✅ Cliente obter: `BLING_ACCESS_TOKEN`
- ✅ Cliente inserir credenciais em: **Configurações → Integrações → ERP**

**Custo:** Cliente paga (depende do plano Bling)  
**Disponível em:** Plano Pro e Enterprise

---

### 8. **Tiny ERP** (Opcional - Cliente Configura)
**O que é:** Integração com ERP Tiny  
**Onde contratar:** https://tiny.com.br  
**Quem contrata:** O cliente LogiFlow (se usar Tiny)  
**O que precisa:**
- ✅ Cliente ter conta Tiny ativa
- ✅ Cliente obter: `TINY_TOKEN`
- ✅ Cliente inserir credenciais em: **Configurações → Integrações → ERP**

**Custo:** Cliente paga (depende do plano Tiny)  
**Disponível em:** Plano Pro e Enterprise

---

## 🔵 AVANÇADAS (Cliente Configura - Plano Enterprise)

### 9. **Sascar** (Cliente Configura)
**O que é:** Rastreamento GPS de veículos  
**Onde contratar:** https://sascar.com.br  
**Quem contrata:** O cliente LogiFlow (se tiver frota rastreada)  
**O que precisa:**
- ✅ Cliente contratar rastreadores Sascar
- ✅ Cliente obter: `SASCAR_API_KEY` e `SASCAR_API_SECRET`
- ✅ Cliente inserir credenciais em: **Configurações → Integrações → GPS**

**Custo:** Cliente paga ~R$ 80-150/veículo/mês  
**Disponível em:** Plano Enterprise

---

### 10. **Autotrac** (Cliente Configura)
**O que é:** Rastreamento GPS alternativo  
**Onde contratar:** https://autotrac.com.br  
**Quem contrata:** O cliente LogiFlow (se tiver frota rastreada)  
**O que precisa:**
- ✅ Cliente contratar rastreadores Autotrac
- ✅ Cliente obter: `AUTOTRAC_USERNAME` e `AUTOTRAC_PASSWORD`
- ✅ Cliente inserir credenciais em: **Configurações → Integrações → GPS**

**Custo:** Cliente paga ~R$ 70-130/veículo/mês  
**Disponível em:** Plano Enterprise

---

### 11. **Onixsat** (Cliente Configura)
**O que é:** Rastreamento GPS alternativo  
**Onde contratar:** https://onixsat.com.br  
**Quem contrata:** O cliente LogiFlow (se tiver frota rastreada)  
**O que precisa:**
- ✅ Cliente contratar rastreadores Onixsat
- ✅ Cliente obter: `ONIXSAT_API_TOKEN`
- ✅ Cliente inserir credenciais em: **Configurações → Integrações → GPS**

**Custo:** Cliente paga ~R$ 60-120/veículo/mês  
**Disponível em:** Plano Enterprise

---

## 📊 Resumo por Prioridade

### ⚠️ LOGIFLOW CONTRATA (3)
1. **Google Maps API** - Mapas e distâncias (todos os planos)
2. **Focus NFe** - Documentos fiscais (todos os planos)
3. **Evolution API** - WhatsApp (todos os planos)

### 🟡 CLIENTE CONFIGURA - FRETE (2) - Plano Pro+
4. **Melhor Envio** - Cotação de frete (cliente tem conta própria)
5. **Frenet** - Cotação de frete (cliente tem conta própria)

### 🟢 CLIENTE CONFIGURA - ERP (3) - Plano Pro+
6. **Omie ERP** - Se cliente usar Omie
7. **Bling ERP** - Se cliente usar Bling
8. **Tiny ERP** - Se cliente usar Tiny

### 🔵 CLIENTE CONFIGURA - GPS (3) - Plano Enterprise
9. **Sascar** - Rastreamento GPS (cliente tem frota)
10. **Autotrac** - Rastreamento GPS (cliente tem frota)
11. **Onixsat** - Rastreamento GPS (cliente tem frota)

---

## 💰 Estimativa de Custos Mensais

### 💰 **Custo LogiFlow (Fixo)**
- Google Maps: ~R$ 30/mês
- Focus NFe: ~R$ 50/mês
- Evolution API: R$ 0 (self-hosted)
- **Total LogiFlow: ~R$ 80/mês** (você paga, divide entre clientes)

### 💳 **Custo Cliente - Plano Pro** (Opcional)
- Melhor Envio: R$ 0 (cliente paga por uso)
- Frenet: R$ 0 (cliente paga por uso)
- Omie/Bling/Tiny: R$ 50-200/mês (cliente já paga)
- **Total Cliente Pro: R$ 50-200/mês** (se usar ERP)

### 💎 **Custo Cliente - Plano Enterprise** (Opcional)
- Tudo do Pro +
- Sascar/Autotrac/Onixsat: ~R$ 80-150/veículo/mês (cliente já paga)
- **Total Cliente Enterprise: R$ 50-200/mês + GPS** (se tiver frota)

---

## 📝 Checklist de Contratação

### Fase 1: Essencial (Fazer Agora)
- [ ] Criar conta Google Cloud → Obter API Key
- [ ] Contratar Focus NFe → Obter Token
- [ ] Configurar Evolution API → Conectar WhatsApp

### Fase 2: Orientar Clientes (Documentação)
- [ ] Criar guia para cliente configurar Melhor Envio
- [ ] Criar guia para cliente configurar Frenet
- [ ] Criar guia para cliente configurar ERP
- [ ] Criar guia para cliente configurar GPS

### Fase 3: Sistema de Permissões
- [ ] Implementar verificação de plano no backend
- [ ] Bloquear funcionalidades por plano no frontend
- [ ] Criar middleware de autorização por plano

---

## 🔧 Arquivo .env Completo

Depois de obter todas as credenciais, seu `.env` ficará assim:

```bash
# OBRIGATÓRIAS
GOOGLE_MAPS_API_KEY=sua_chave_google_aqui
FOCUSNFE_TOKEN=seu_token_focus_aqui
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_chave_evolution

# RECOMENDADAS
MELHOR_ENVIO_TOKEN=seu_token_melhor_envio
MELHOR_ENVIO_SANDBOX=false
FRENET_TOKEN=seu_token_frenet

# OPCIONAIS (ERP)
OMIE_APP_KEY=sua_chave_omie
OMIE_APP_SECRET=seu_secret_omie
BLING_ACCESS_TOKEN=seu_token_bling
TINY_TOKEN=seu_token_tiny

# FUTURAS (GPS)
SASCAR_API_KEY=sua_chave_sascar
SASCAR_API_SECRET=seu_secret_sascar
SASCAR_SIMULATION_MODE=false

AUTOTRAC_USERNAME=seu_usuario_autotrac
AUTOTRAC_PASSWORD=sua_senha_autotrac
AUTOTRAC_SIMULATION_MODE=false

ONIXSAT_API_TOKEN=seu_token_onixsat
ONIXSAT_SIMULATION_MODE=false
```

---

## ✅ Resumo Executivo

**Total de Empresas:** 11  
**LogiFlow Contrata:** 3 (Google, Focus NFe, Evolution API)  
**Cliente Configura - Frete:** 2 (Melhor Envio, Frenet) - Plano Pro+  
**Cliente Configura - ERP:** 3 (Omie, Bling, Tiny) - Plano Pro+  
**Cliente Configura - GPS:** 3 (Sascar, Autotrac, Onixsat) - Enterprise

**Custo LogiFlow:** ~R$ 80/mês (fixo, você paga)  
**Custo Cliente:** Variável (cada um paga suas integrações)  
**Sistema Funciona Agora:** ✅ Sim (modo simulação)  
**Pronto para Produção:** ✅ Sim (após configurar as 3 do LogiFlow)
