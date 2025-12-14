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
- 🟢 ERP (Omie/Bling/Tiny) - Se usar
- 🔵 GPS (Sascar/Autotrac/Onixsat) - Se tiver
- 🟡 Frete (Melhor Envio/Frenet) - Se quiser

**Custo Cliente:** Variável (cada um paga seu próprio serviço)

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

### ⚠️ OBRIGATÓRIAS (3)
1. **Google Maps API** - Mapas e distâncias
2. **Focus NFe** - Documentos fiscais
3. **Evolution API** - WhatsApp

### 🟡 RECOMENDADAS (2)
4. **Melhor Envio** - Cotação de frete
5. **Frenet** - Cotação de frete alternativa

### 🟢 OPCIONAIS (3)
6. **Omie ERP** - Se usar Omie
7. **Bling ERP** - Se usar Bling
8. **Tiny ERP** - Se usar Tiny

### 🔵 FUTURAS (3)
9. **Sascar** - Rastreamento GPS
10. **Autotrac** - Rastreamento GPS
11. **Onixsat** - Rastreamento GPS

---

## 💰 Estimativa de Custos Mensais

### Mínimo (Obrigatórias)
- Google Maps: ~R$ 30/mês
- Focus NFe: ~R$ 50/mês
- Evolution API: R$ 0 (self-hosted)
- **Total Mínimo: ~R$ 80/mês**

### Recomendado (+ Cotação Frete)
- Melhor Envio: R$ 0 (paga por uso)
- Frenet: R$ 0 (paga por uso)
- **Total: ~R$ 80/mês + frete usado**

### Com ERP (Opcional)
- Omie/Bling/Tiny: R$ 50-200/mês
- **Total: ~R$ 130-280/mês**

### Com GPS (Futuro - 10 veículos)
- Sascar/Autotrac/Onixsat: ~R$ 800-1.500/mês
- **Total: ~R$ 880-1.580/mês**

---

## 📝 Checklist de Contratação

### Fase 1: Essencial (Fazer Agora)
- [ ] Criar conta Google Cloud → Obter API Key
- [ ] Contratar Focus NFe → Obter Token
- [ ] Configurar Evolution API → Conectar WhatsApp

### Fase 2: Cotação (Fazer Logo)
- [ ] Criar conta Melhor Envio → Obter Token
- [ ] Criar conta Frenet → Obter Token

### Fase 3: ERP (Se Necessário)
- [ ] Verificar se usa Omie/Bling/Tiny
- [ ] Obter credenciais do ERP escolhido

### Fase 4: GPS (Quando Crescer)
- [ ] Avaliar fornecedores GPS
- [ ] Contratar rastreadores
- [ ] Obter credenciais API

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
**Obrigatórias:** 3 (Google, Focus NFe, Evolution API)  
**Recomendadas:** 2 (Melhor Envio, Frenet)  
**Opcionais:** 3 (Omie, Bling, Tiny)  
**Futuras:** 3 (Sascar, Autotrac, Onixsat)

**Custo Inicial:** ~R$ 80/mês  
**Sistema Funciona Agora:** ✅ Sim (modo simulação para GPS e frete)  
**Pronto para Produção:** ✅ Sim (após configurar as 3 obrigatórias)
