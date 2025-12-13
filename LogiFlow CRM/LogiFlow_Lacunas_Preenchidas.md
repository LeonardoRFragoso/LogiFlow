# LogiFlow CRM - Lacunas Estratégicas Preenchidas

> Documento complementar ao LogiFlow_Plan_Completo.txt
> Data: Dezembro 2024

---

## LACUNA 1: Diferenciação de Mercado

### 1.1 USP (Unique Selling Proposition)

**Proposta de Valor Principal:**
> "LogiFlow é o único CRM brasileiro que une gestão comercial, operacional e fiscal para transportadoras em uma única plataforma, com emissão de CT-e/MDF-e integrada e rastreamento em tempo real — sem precisar de múltiplos sistemas."

**Diferenciais-Chave:**
| Diferencial | Benefício para o Cliente |
|-------------|-------------------------|
| **Tudo em um só lugar** | Elimina 3-4 sistemas separados (CRM + TMS + Emissor fiscal + Rastreamento) |
| **Preço acessível** | 60-70% mais barato que soluções enterprise (SAP, TOTVS) |
| **Setup em 48h** | Sem projetos de meses; cliente opera em 2 dias |
| **Sem contrato de fidelidade** | Pagamento mensal, cancela quando quiser |
| **Suporte em português** | Atendimento humano, não bot |

**Tagline sugerida:**
- "Sua transportadora no controle. Do comercial à entrega."
- "CRM + TMS + Fiscal em um só sistema."

---

### 1.2 Análise de Concorrentes

#### Concorrentes Diretos (CRM + Logística)

| Solução | Pontos Fortes | Pontos Fracos | Preço Estimado |
|---------|---------------|---------------|----------------|
| **Ploomes** | CRM robusto, boa UX, integrações | NÃO é especializado em logística, sem CT-e | R$ 249-699/mês |
| **Agendor** | Simples, barato, bom para PME | Genérico, sem módulos de transporte | R$ 53-106/usuário |
| **RD Station CRM** | Grátis até 4 usuários, marketing | Zero funcionalidades de logística | Grátis - R$ 59/usuário |
| **Fleetsmart** | Rastreamento GPS, gestão frota | Foco em frota, não em vendas/CRM | R$ 29-89/veículo |
| **SSW (TMS)** | Completo para logística, CT-e | Caro, complexo, setup demorado | R$ 1.500-5.000/mês |
| **TOTVS Logística** | Enterprise, completo | Muito caro, burocrático | R$ 3.000-15.000/mês |
| **Gestran** | TMS nacional, bom suporte | Sem CRM comercial integrado | R$ 800-2.500/mês |

#### Matriz de Posicionamento

```
                    PREÇO ALTO
                        │
         TOTVS ●        │        ● SSW
         SAP ●          │
                        │
    ────────────────────┼──────────────────── ESPECIALIZAÇÃO
    GENÉRICO            │              LOGÍSTICA
                        │
         Ploomes ●      │    ★ LogiFlow (posição alvo)
         Agendor ●      │        ● Gestran
         RD Station ●   │        ● Fleetsmart
                        │
                    PREÇO BAIXO
```

#### Oportunidade de Mercado

**Nicho mal atendido:** Transportadoras de pequeno/médio porte (5-100 veículos)
- **Problema:** Não podem pagar TOTVS/SSW, mas Agendor/Ploomes não resolvem operação
- **Tamanho:** ~50.000 transportadoras no Brasil (ANTT)
- **TAM:** R$ 180M/ano (50k x R$ 300/mês x 12)
- **SAM realista (1%):** R$ 1.8M/ano = 500 clientes

---

### 1.3 Funcionalidades "Killer"

**Top 5 funcionalidades que vendem:**

1. **Emissão de CT-e/MDF-e integrada**
   - Cliente não precisa de sistema fiscal separado
   - Economia de R$ 100-300/mês só nisso
   - Integração via API (Focus NFe, Webmania, ou própria)

2. **Portal do Cliente (tracking público)**
   - Cliente final rastreia entrega sem ligar
   - Link compartilhável por WhatsApp
   - Reduz 50%+ das ligações "cadê minha carga?"

3. **App do Motorista (PWA)**
   - Aceita/recusa cargas
   - Atualiza status em tempo real
   - Foto de comprovante de entrega
   - Funciona offline

4. **Dashboard de SLA em tempo real**
   - Visualização de entregas atrasadas
   - Alertas automáticos para gerentes
   - KPIs de performance por motorista/cliente

5. **WhatsApp integrado (Evolution API)**
   - Notificações automáticas ao cliente
   - Chatbot para consulta de status
   - Histórico no CRM

---

## LACUNA 2: Onboarding e Adoção

### 2.1 Estratégia de Migração de Dados

#### Fontes de Dados Típicas
| Origem | Formato | Prioridade |
|--------|---------|------------|
| Planilhas Excel/Google | XLSX, CSV | Alta |
| Sistema anterior (TMS) | Export SQL/CSV | Alta |
| Contatos do celular | vCard, CSV | Média |
| E-mails (clientes) | Manual | Baixa |

#### Processo de Migração (5 passos)

```
1. COLETA (Dia 1)
   └── Cliente envia planilhas/exports
   └── Template padrão LogiFlow (Excel)

2. VALIDAÇÃO (Dia 1-2)
   └── Script Python valida dados
   └── Relatório de inconsistências
   └── Cliente corrige ou aprova "como está"

3. MAPEAMENTO (Dia 2)
   └── Campos origem → campos LogiFlow
   └── Regras de transformação (ex: CNPJ sem pontos)

4. IMPORTAÇÃO (Dia 2)
   └── Script de importação via API
   └── Ambiente de homologação primeiro
   └── Validação com cliente

5. GO-LIVE (Dia 3)
   └── Importação em produção
   └── Treinamento de conferência
```

#### Templates de Migração a Criar
- `template_clientes.xlsx` (Nome, CNPJ, Endereço, Contato, Condição Pgto)
- `template_motoristas.xlsx` (Nome, CPF, CNH, Categoria, Vencimento)
- `template_veiculos.xlsx` (Placa, Tipo, Renavam, Última Manutenção)
- `template_cotacoes_historico.xlsx` (Cliente, Origem, Destino, Valor, Status)

#### Script de Importação (criar)
```python
# logiflow_import.py
# Lê Excel, valida, importa via API SuiteCRM
# Gera relatório de erros
# Suporta dry-run (simulação)
```

---

### 2.2 Plano de Treinamento/Capacitação

#### Estrutura de Onboarding (7 dias)

| Dia | Atividade | Duração | Responsável |
|-----|-----------|---------|-------------|
| 1 | Kickoff + Acesso ao sistema | 30min | CS |
| 2 | Migração de dados | 2h | Técnico |
| 3 | Treinamento: Cadastros básicos | 1h | CS (vídeo) |
| 4 | Treinamento: Cotações e Pedidos | 1h | CS (vídeo) |
| 5 | Treinamento: Operação (entregas, status) | 1h | CS (vídeo) |
| 6 | Configuração de usuários e permissões | 30min | Cliente + CS |
| 7 | Go-live assistido + Dúvidas | 1h | CS |

#### Materiais de Treinamento a Criar

**Vídeos (Loom/YouTube privado):**
1. Visão geral do sistema (5 min)
2. Cadastro de clientes (8 min)
3. Criando cotações (10 min)
4. Convertendo cotação em pedido (5 min)
5. Acompanhando entregas (8 min)
6. Usando o dashboard (5 min)
7. App do motorista (8 min)
8. Emitindo CT-e (quando disponível) (10 min)

**Documentos PDF:**
- Guia de início rápido (2 páginas)
- Manual completo do usuário (30 páginas)
- FAQ - Perguntas frequentes
- Glossário de termos

#### Certificação (opcional futuro)
- Quiz online após treinamento
- Certificado de "Usuário LogiFlow"
- Gamification: badges por uso

---

### 2.3 Documentação de Usuário Final

#### Estrutura da Base de Conhecimento

```
docs.logiflow.com.br/
├── inicio-rapido/
│   ├── primeiro-acesso.md
│   ├── navegacao-basica.md
│   └── configuracoes-iniciais.md
├── modulos/
│   ├── clientes/
│   ├── cotacoes/
│   ├── pedidos/
│   ├── entregas/
│   ├── motoristas/
│   └── veiculos/
├── operacao/
│   ├── fluxo-cotacao-entrega.md
│   ├── atualizando-status.md
│   ├── app-motorista.md
│   └── portal-cliente.md
├── fiscal/
│   ├── emitindo-cte.md
│   ├── emitindo-mdfe.md
│   └── cancelamento-carta-correcao.md
├── relatorios/
│   ├── dashboard-operacional.md
│   ├── relatorio-entregas.md
│   └── exportando-dados.md
├── integracao/
│   ├── whatsapp.md
│   ├── api.md
│   └── webhooks.md
└── faq/
    ├── problemas-comuns.md
    └── contato-suporte.md
```

#### Ferramenta Sugerida
- **GitBook** (grátis até 5 usuários) ou **Notion** para documentação
- **Loom** para vídeos rápidos
- **Intercom/Crisp** para chat de suporte integrado

---

## LACUNA 3: Integrações Essenciais

### 3.1 CT-e / MDF-e (Documentos Fiscais)

#### Opções de Integração

| Provedor | Preço | Vantagens | Desvantagens |
|----------|-------|-----------|--------------|
| **Focus NFe** | ~R$ 0,15/doc | Mais popular, boa doc | Preço por documento |
| **Webmania** | R$ 49-199/mês | Preço fixo, ilimitado | Menos conhecido |
| **Tecnospeed** | Negociar | Enterprise, completo | Caro para PME |
| **Desenvolvimento próprio** | ~R$ 15k inicial | Sem custo recorrente | Manutenção SEFAZ |

#### Recomendação Inicial
**Focus NFe** - Melhor custo-benefício para MVP
- API REST simples
- Sandbox para testes
- Preço por documento (escala com cliente)

#### Implementação CT-e

```python
# Exemplo de integração Focus NFe
# backend/integrations/fiscal/cte.py

import requests
from typing import Dict

class FocusNFeClient:
    BASE_URL = "https://api.focusnfe.com.br/v2"
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def emitir_cte(self, dados: Dict) -> Dict:
        """Emite CT-e via Focus NFe"""
        payload = {
            "natureza_operacao": dados["natureza"],
            "cfop": dados["cfop"],
            "modal": dados["modal"],  # 01=Rodoviário
            "tomador": dados["tomador"],
            "remetente": dados["remetente"],
            "destinatario": dados["destinatario"],
            "valores": dados["valores"],
            # ... demais campos obrigatórios
        }
        response = requests.post(
            f"{self.BASE_URL}/cte",
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    def consultar_cte(self, ref: str) -> Dict:
        """Consulta status do CT-e"""
        response = requests.get(
            f"{self.BASE_URL}/cte/{ref}",
            headers=self.headers
        )
        return response.json()
```

#### Campos Necessários no Módulo PedidosFrete
```
- cte_numero (varchar) - Número do CT-e
- cte_chave (varchar 44) - Chave de acesso
- cte_status (enum: Pendente/Emitido/Cancelado)
- cte_data_emissao (datetime)
- cte_xml (text) - XML autorizado
- cte_pdf_url (varchar) - Link do DACTE
- mdfe_numero (varchar) - Número do MDF-e
- mdfe_chave (varchar 44)
```

---

### 3.2 Rastreamento GPS em Tempo Real

#### Opções de Integração

| Solução | Tipo | Custo | Complexidade |
|---------|------|-------|--------------|
| **App próprio (PWA)** | Celular motorista | Grátis | Média |
| **Sascar/Autotrac** | Rastreador veicular | R$ 50-100/veículo | Baixa (API) |
| **Onixsat** | Rastreador | R$ 40-80/veículo | Baixa |
| **Google Maps API** | Geocoding/rotas | ~R$ 200/mês | Média |

#### Recomendação: App PWA + Opção de integração

**Fase 1 (MVP):** App PWA do motorista
- Usa GPS do celular
- Atualiza posição a cada 5 minutos
- Funciona offline (sync quando conectar)
- Custo: ZERO

**Fase 2 (Escala):** Integração com rastreadores
- API para receber posições de Sascar/Autotrac
- Webhook para atualização em tempo real
- Mapa consolidado no dashboard

#### Estrutura do App Motorista (PWA)

```
/app-motorista (Vue 3 + PWA)
├── src/
│   ├── views/
│   │   ├── Login.vue
│   │   ├── MinhasCargas.vue
│   │   ├── DetalheEntrega.vue
│   │   ├── AtualizarStatus.vue
│   │   └── Configuracoes.vue
│   ├── services/
│   │   ├── api.js
│   │   ├── geolocation.js
│   │   └── offline-sync.js
│   └── sw.js (Service Worker)
├── manifest.json
└── package.json
```

---

### 3.3 Integrações com ERPs

#### Priorização por Demanda de Mercado

| ERP | Market Share PME | Prioridade | Complexidade |
|-----|------------------|------------|--------------|
| **Omie** | Alta (PME) | Alta | Baixa (API REST) |
| **Bling** | Alta (e-commerce) | Alta | Baixa |
| **Tiny** | Média | Média | Baixa |
| **TOTVS Protheus** | Média (maior porte) | Média | Alta |
| **Sankhya** | Média | Baixa | Média |
| **SAP B1** | Baixa (enterprise) | Baixa | Alta |

#### Integração Omie (Exemplo)

```python
# backend/integrations/erp/omie.py

class OmieClient:
    BASE_URL = "https://app.omie.com.br/api/v1"
    
    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
    
    def listar_clientes(self, pagina: int = 1):
        payload = {
            "call": "ListarClientes",
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [{"pagina": pagina, "registros_por_pagina": 50}]
        }
        response = requests.post(
            f"{self.BASE_URL}/geral/clientes/",
            json=payload
        )
        return response.json()
    
    def sincronizar_cliente(self, cliente_logiflow: dict):
        """Cria/atualiza cliente no Omie"""
        # Mapear campos LogiFlow -> Omie
        # POST para API Omie
        pass
```

#### Fluxos de Sincronização
```
LogiFlow → ERP:
- Novo cliente cadastrado → Criar no ERP
- Pedido concluído → Gerar fatura no ERP
- Valores de frete → Lançar receita

ERP → LogiFlow:
- Novo cliente no ERP → Criar no LogiFlow
- Pagamento recebido → Atualizar status financeiro
- Produtos/serviços → Sincronizar tabela de preços
```

---

### 3.4 APIs de Frete (Cotação Automática)

#### Integrações Úteis

| API | Uso | Custo |
|-----|-----|-------|
| **Melhor Envio** | Cotação multi-transportadoras | Grátis (comissão) |
| **Frenet** | Cotação + gestão envios | R$ 49-199/mês |
| **Correios (API)** | Cotação PAC/SEDEX | Contrato ECT |
| **Google Distance Matrix** | Cálculo de distância | ~R$ 5/1000 req |

#### Exemplo: Cotação Automática

```python
# backend/services/cotacao_automatica.py

async def calcular_frete_automatico(
    origem_cep: str,
    destino_cep: str,
    peso_kg: float,
    volumes: int
) -> list:
    """Retorna cotações de múltiplas transportadoras"""
    
    # 1. Buscar distância
    distancia = await google_distance_matrix(origem_cep, destino_cep)
    
    # 2. Aplicar tabela própria
    valor_proprio = calcular_tabela_propria(distancia, peso_kg)
    
    # 3. (Opcional) Consultar Melhor Envio
    cotacoes_terceiros = await melhor_envio_cotar(
        origem_cep, destino_cep, peso_kg, volumes
    )
    
    return [
        {"transportadora": "Frota Própria", "valor": valor_proprio, "prazo": 3},
        *cotacoes_terceiros
    ]
```

---

## LACUNA 4: Métricas de Sucesso do Cliente

### 4.1 KPIs de Retenção (Churn)

#### Métricas Essenciais

| Métrica | Fórmula | Meta |
|---------|---------|------|
| **Churn Mensal** | Cancelamentos / Total clientes | < 3% |
| **Churn Anual** | 1 - (1 - churn_mensal)^12 | < 30% |
| **MRR** | Soma das assinaturas ativas | Crescimento 10%/mês |
| **LTV** | Ticket médio × Tempo médio | > 12x CAC |
| **CAC** | Custo marketing+vendas / Novos clientes | < R$ 500 |

#### Alertas de Churn (implementar)

```python
# Sinais de risco de churn
SINAIS_RISCO = [
    {"sinal": "Sem login há 14 dias", "peso": 3},
    {"sinal": "Uso < 30% features", "peso": 2},
    {"sinal": "Ticket de suporte não resolvido", "peso": 2},
    {"sinal": "Pagamento atrasado", "peso": 3},
    {"sinal": "Reclamação NPS", "peso": 2},
]

def calcular_risco_churn(tenant_id: str) -> int:
    """Retorna score de risco 0-10"""
    score = 0
    # Verificar cada sinal
    # Somar pesos
    return min(score, 10)
```

---

### 4.2 NPS e Satisfação

#### Implementação NPS

**Pesquisa automática:**
- Enviar após 30 dias de uso
- Repetir a cada 90 dias
- Pergunta: "De 0 a 10, qual a probabilidade de recomendar o LogiFlow?"

**Classificação:**
- **Promotores (9-10):** Pedir review, indicação
- **Neutros (7-8):** Entender o que falta
- **Detratores (0-6):** Contato urgente do CS

**Cálculo:**
```
NPS = % Promotores - % Detratores
Meta: NPS > 50
```

#### Pesquisa CSAT (por interação)

Após cada ticket de suporte:
- "Como você avalia o atendimento?" (1-5 estrelas)
- Meta: > 4.5 estrelas

---

### 4.3 Health Score do Cliente

#### Composição do Health Score (0-100)

| Componente | Peso | Como Medir |
|------------|------|------------|
| **Uso do sistema** | 30% | Logins, ações, features usadas |
| **Adoção de features** | 20% | % de módulos ativos |
| **Engajamento** | 15% | Frequência de uso |
| **Suporte** | 15% | Tickets abertos, tempo resolução |
| **Financeiro** | 20% | Pagamentos em dia, upsells |

#### Cálculo

```python
def calcular_health_score(tenant_id: str) -> dict:
    """Calcula health score do cliente"""
    
    # Uso (30 pontos max)
    logins_30d = contar_logins(tenant_id, dias=30)
    uso_score = min(30, logins_30d * 2)
    
    # Adoção (20 pontos max)
    features_ativas = contar_features_usadas(tenant_id)
    adocao_score = (features_ativas / TOTAL_FEATURES) * 20
    
    # Engajamento (15 pontos max)
    dias_ativos = contar_dias_ativos(tenant_id, dias=30)
    engajamento_score = (dias_ativos / 30) * 15
    
    # Suporte (15 pontos max)
    tickets_abertos = contar_tickets_abertos(tenant_id)
    suporte_score = max(0, 15 - tickets_abertos * 3)
    
    # Financeiro (20 pontos max)
    pagamentos_em_dia = verificar_pagamentos(tenant_id)
    financeiro_score = 20 if pagamentos_em_dia else 5
    
    total = uso_score + adocao_score + engajamento_score + suporte_score + financeiro_score
    
    return {
        "score": round(total),
        "classificacao": classificar_health(total),
        "detalhes": {
            "uso": uso_score,
            "adocao": adocao_score,
            "engajamento": engajamento_score,
            "suporte": suporte_score,
            "financeiro": financeiro_score
        }
    }

def classificar_health(score: int) -> str:
    if score >= 80: return "Saudável"
    if score >= 60: return "Atenção"
    if score >= 40: return "Risco"
    return "Crítico"
```

#### Dashboard de Customer Success

```
┌─────────────────────────────────────────────────────────┐
│ SAÚDE DOS CLIENTES                                      │
├─────────────────────────────────────────────────────────┤
│ 🟢 Saudável (80-100):  45 clientes (60%)               │
│ 🟡 Atenção (60-79):    20 clientes (27%)               │
│ 🟠 Risco (40-59):       8 clientes (10%)               │
│ 🔴 Crítico (0-39):      2 clientes (3%)                │
├─────────────────────────────────────────────────────────┤
│ CLIENTES QUE PRECISAM DE ATENÇÃO:                       │
│ • Transportes ABC (Score: 35) - Sem login há 20 dias   │
│ • Logística XYZ (Score: 42) - 3 tickets abertos        │
└─────────────────────────────────────────────────────────┘
```

---

## RESUMO: Prioridades de Implementação

### Antes do MVP (Semana 0)
- [x] Definir USP e posicionamento
- [x] Mapear concorrentes
- [x] Definir funcionalidades killer
- [x] Planejar integrações

### Durante o MVP (Semanas 1-6)
- [ ] Templates de migração Excel
- [ ] Script de importação básico
- [ ] Documentação inicial (5 páginas)
- [ ] 3 vídeos de treinamento

### Pós-MVP (Semanas 7-12)
- [ ] Integração CT-e (Focus NFe)
- [ ] App motorista PWA
- [ ] Health score básico
- [ ] Pesquisa NPS automática

### Escala (Mês 3+)
- [ ] Integração Omie/Bling
- [ ] Rastreamento GPS avançado
- [ ] Dashboard de CS completo
- [ ] Base de conhecimento completa

---

## ARQUIVOS A CRIAR

| Arquivo | Descrição | Prioridade |
|---------|-----------|------------|
| `templates/template_clientes.xlsx` | Migração de clientes | Alta |
| `templates/template_motoristas.xlsx` | Migração de motoristas | Alta |
| `scripts/importar_dados.py` | Script de migração | Alta |
| `docs/guia-inicio-rapido.md` | Documentação básica | Alta |
| `backend/integrations/fiscal/cte.py` | Integração CT-e | Média |
| `app-motorista/` | PWA do motorista | Média |
| `backend/services/health_score.py` | Cálculo de health score | Baixa |

---

*Documento gerado em Dezembro 2024 - LogiFlow CRM*
