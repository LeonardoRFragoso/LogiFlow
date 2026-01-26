# 📦 Configuração Cotações Automáticas - LogiFlow CRM

## 📋 Visão Geral

O sistema de cotações automáticas compara preços de frete de múltiplas fontes:
- 🗺️ **Google Maps Distance Matrix** - Cálculo de distância e tempo
- 📮 **Melhor Envio** - Correios, Jadlog, Azul Cargo, etc
- 🚚 **Frenet** - Agregador de transportadoras
- 💰 **Tabela Própria** - Preços customizados

---

## 🗺️ PARTE 1: Google Maps Distance Matrix API

### Por que Google Maps?

Calcula automaticamente:
- ✅ Distância real entre CEPs
- ✅ Tempo estimado de viagem
- ✅ Considera tráfego e rotas
- ✅ Base para cálculo de frete próprio

### 1. Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com
2. Clique em **"Criar Projeto"**
3. Nome: `LogiFlow CRM`
4. Clique em **"Criar"**

### 2. Habilitar Distance Matrix API

1. No menu, vá em **"APIs e Serviços"** → **"Biblioteca"**
2. Busque: `Distance Matrix API`
3. Clique em **"Distance Matrix API"**
4. Clique em **"Ativar"**

### 3. Criar API Key

1. Vá em **"APIs e Serviços"** → **"Credenciais"**
2. Clique em **"+ Criar Credenciais"** → **"Chave de API"**
3. Copie a API Key gerada
4. Clique em **"Restringir chave"** (IMPORTANTE!)

### 4. Restringir API Key (Segurança)

**Por IP (Produção):**
1. Em **"Restrições de aplicativo"**, selecione **"Endereços IP"**
2. Adicione o IP do seu servidor
3. Exemplo: `203.0.113.0/24` ou `203.0.113.10`

**Por API (Recomendado):**
1. Em **"Restrições de API"**, selecione **"Restringir chave"**
2. Escolha apenas: `Distance Matrix API`
3. Clique em **"Salvar"**

### 5. Configurar Cobrança

⚠️ **IMPORTANTE:** Google Maps cobra após limite gratuito!

**Limite Gratuito:**
- $200 de créditos/mês (≈ 40.000 requisições)
- Depois: $0.005 por requisição

**Para evitar custos altos:**
1. Vá em **"Faturamento"** → **"Orçamentos e alertas"**
2. Crie alerta para $50, $100, $150
3. Configure limite máximo de $200

### 6. Configurar no LogiFlow

Edite `.env`:

```bash
# Google Maps Distance Matrix
GOOGLE_MAPS_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvw
GOOGLE_MAPS_DISTANCE_MATRIX_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvw
```

### 7. Testar API

```bash
docker-compose exec backend python -c "
import os
import requests

api_key = os.getenv('GOOGLE_MAPS_API_KEY')
origins = '01310-100'  # Av Paulista, SP
destinations = '20040-020'  # Centro, RJ

url = f'https://maps.googleapis.com/maps/api/distancematrix/json'
params = {
    'origins': origins,
    'destinations': destinations,
    'key': api_key
}

response = requests.get(url, params=params)
data = response.json()

if data['status'] == 'OK':
    element = data['rows'][0]['elements'][0]
    print(f'✅ Distância: {element[\"distance\"][\"text\"]}')
    print(f'✅ Tempo: {element[\"duration\"][\"text\"]}')
else:
    print(f'❌ Erro: {data[\"error_message\"]}')
"
```

---

## 📮 PARTE 2: Melhor Envio

### O que é Melhor Envio?

Plataforma que integra múltiplas transportadoras:
- Correios (PAC, SEDEX)
- Jadlog
- Azul Cargo
- Latam Cargo
- Total Express
- E mais...

### 1. Criar Conta

1. Acesse: https://melhorenvio.com.br
2. Clique em **"Cadastre-se grátis"**
3. Preencha dados da empresa
4. Confirme email

### 2. Obter Token (Sandbox)

1. Faça login em: https://sandbox.melhorenvio.com.br
2. Vá em **"Configurações"** → **"API"**
3. Clique em **"Gerar Token"**
4. Copie o token de sandbox

**Formato:** `eyJ0eXAiOiJKV1QiLCJhbGc...`

### 3. Obter Token (Produção)

1. Faça login em: https://melhorenvio.com.br
2. Complete o cadastro da empresa
3. Adicione saldo (via boleto/PIX)
4. Vá em **"Configurações"** → **"API"**
5. Clique em **"Gerar Token"**

### 4. Configurar no LogiFlow

Edite `.env`:

**Sandbox (Testes):**
```bash
MELHOR_ENVIO_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGc...SANDBOX
MELHOR_ENVIO_SANDBOX=true
```

**Produção:**
```bash
MELHOR_ENVIO_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGc...PRODUCAO
MELHOR_ENVIO_SANDBOX=false
```

### 5. Testar Melhor Envio

```bash
docker-compose exec backend python -c "
import sys
sys.path.append('/app')

from integrations.frete.melhor_envio import MelhorEnvioClient
import os

token = os.getenv('MELHOR_ENVIO_TOKEN')
sandbox = os.getenv('MELHOR_ENVIO_SANDBOX', 'true') == 'true'

client = MelhorEnvioClient(token=token, sandbox=sandbox)

resultado = client.calcular_frete_simples(
    cep_origem='01310100',
    cep_destino='20040020',
    peso_kg=1.0,
    altura_cm=10,
    largura_cm=15,
    comprimento_cm=20,
    valor_mercadoria=100.00
)

if resultado['success']:
    print('✅ Cotações recebidas:')
    for cotacao in resultado['cotacoes'][:3]:
        print(f'  - {cotacao[\"nome\"]}: R$ {cotacao[\"preco\"]:.2f} ({cotacao[\"prazo\"]} dias)')
else:
    print(f'❌ Erro: {resultado.get(\"error\")}')
"
```

### 6. Custos Melhor Envio

**Modelo:**
- Você paga à Melhor Envio
- Melhor Envio paga a transportadora
- Sem mensalidade

**Vantagens:**
- ✅ Preços negociados (desconto)
- ✅ Rastreamento unificado
- ✅ Um único pagamento
- ✅ Suporte centralizado

---

## 🚚 PARTE 3: Frenet

### O que é Frenet?

Agregador similar ao Melhor Envio, focado em e-commerce.

### 1. Criar Conta

1. Acesse: https://painel.frenet.com.br/cadastro
2. Preencha dados
3. Aguarde aprovação (1-2 dias úteis)

### 2. Obter Token

1. Faça login em: https://painel.frenet.com.br
2. Vá em **"Configurações"** → **"Token de Integração"**
3. Copie o token

### 3. Configurar no LogiFlow

Edite `.env`:

```bash
FRENET_TOKEN=abc123def456ghi789jkl012mno345pqr678stu
```

### 4. Testar Frenet

```bash
docker-compose exec backend python -c "
import sys
sys.path.append('/app')

from integrations.frete.frenet import FrenetClient
import os

token = os.getenv('FRENET_TOKEN')
client = FrenetClient(token=token)

resultado = client.calcular_frete(
    cep_origem='01310100',
    cep_destino='20040020',
    peso_kg=1.0,
    altura_cm=10,
    largura_cm=15,
    comprimento_cm=20,
    valor_mercadoria=100.00
)

if resultado['success']:
    print('✅ Cotações Frenet:')
    for cotacao in resultado['cotacoes']:
        print(f'  - {cotacao[\"transportadora\"]}: R$ {cotacao[\"valor\"]:.2f}')
else:
    print(f'❌ Erro: {resultado.get(\"error\")}')
"
```

---

## 💰 PARTE 4: Tabela Própria

### Configurar Preços Customizados

O sistema calcula automaticamente baseado em:
- Distância (Google Maps)
- Peso e volume da carga
- Tabela de preços configurável

### 1. Criar Tabela de Preços

Crie arquivo `tabela_frete.json`:

```json
{
  "frete_por_km": 1.50,
  "taxa_base": 50.00,
  "taxa_por_kg": 0.80,
  "taxa_por_m3": 150.00,
  "pedagio_medio_por_km": 0.15,
  "markup_percentual": 30,
  "prazo_dias_por_100km": 1
}
```

### 2. Carregar Tabela no Sistema

```python
# backend/services/tabela_frete.py
import json
import os

def get_tabela_frete():
    """Carrega tabela de preços"""
    arquivo = os.path.join(os.path.dirname(__file__), 'tabela_frete.json')
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    
    # Valores padrão
    return {
        "frete_por_km": 1.50,
        "taxa_base": 50.00,
        "taxa_por_kg": 0.80,
        "taxa_por_m3": 150.00,
        "pedagio_medio_por_km": 0.15,
        "markup_percentual": 30,
        "prazo_dias_por_100km": 1
    }

def calcular_frete_proprio(distancia_km, peso_kg, volume_m3):
    """Calcula frete usando tabela própria"""
    tabela = get_tabela_frete()
    
    # Cálculo base
    custo_distancia = distancia_km * tabela["frete_por_km"]
    custo_peso = peso_kg * tabela["taxa_por_kg"]
    custo_volume = volume_m3 * tabela["taxa_por_m3"]
    pedagio = distancia_km * tabela["pedagio_medio_por_km"]
    
    # Custo total
    custo_total = (
        tabela["taxa_base"] +
        custo_distancia +
        max(custo_peso, custo_volume) +  # Usa o maior entre peso e volume
        pedagio
    )
    
    # Aplica markup
    markup = custo_total * (tabela["markup_percentual"] / 100)
    valor_final = custo_total + markup
    
    # Calcula prazo
    prazo_dias = int((distancia_km / 100) * tabela["prazo_dias_por_100km"]) + 1
    
    return {
        "valor": round(valor_final, 2),
        "prazo_dias": prazo_dias,
        "detalhes": {
            "taxa_base": tabela["taxa_base"],
            "custo_distancia": round(custo_distancia, 2),
            "custo_peso": round(custo_peso, 2),
            "custo_volume": round(custo_volume, 2),
            "pedagio": round(pedagio, 2),
            "subtotal": round(custo_total, 2),
            "markup": round(markup, 2)
        }
    }
```

---

## ✅ Teste Completo do Sistema

### Script de Teste End-to-End

```python
import sys
sys.path.append('/app')

from routers.cotacao_automatica import cotar_frete_consolidado

# Dados de teste
dados = {
    "origem_cep": "01310100",
    "destino_cep": "20040020",
    "peso_kg": 10.5,
    "altura_cm": 30,
    "largura_cm": 40,
    "comprimento_cm": 50,
    "valor_mercadoria": 1000.00,
    "incluir_melhor_envio": True,
    "incluir_frenet": True,
    "incluir_tabela_propria": True
}

print("🔍 Iniciando cotação consolidada...\n")

resultado = cotar_frete_consolidado(dados)

if resultado["success"]:
    print(f"✅ {len(resultado['cotacoes'])} cotações encontradas:\n")
    
    for cotacao in resultado["cotacoes"]:
        print(f"📦 {cotacao['transportadora']} ({cotacao['fonte']})")
        print(f"   Valor: R$ {cotacao['valor']:.2f}")
        print(f"   Prazo: {cotacao['prazo_dias']} dias úteis")
        print()
    
    if resultado.get("melhor_opcao"):
        melhor = resultado["melhor_opcao"]
        print(f"🏆 MELHOR OPÇÃO: {melhor['transportadora']}")
        print(f"   R$ {melhor['valor']:.2f} em {melhor['prazo_dias']} dias")
else:
    print(f"❌ Erro: {resultado.get('error')}")
```

Execute:
```bash
docker-compose exec backend python test_cotacao_completa.py
```

**Resultado esperado:**
```
✅ 8 cotações encontradas:

📦 Correios PAC (melhor_envio)
   Valor: R$ 45.80
   Prazo: 8 dias úteis

📦 Correios SEDEX (melhor_envio)
   Valor: R$ 78.50
   Prazo: 3 dias úteis

📦 Jadlog Package (melhor_envio)
   Valor: R$ 52.30
   Prazo: 5 dias úteis

📦 Frenet Correios (frenet)
   Valor: R$ 47.20
   Prazo: 7 dias úteis

📦 Tabela Própria (tabela_propria)
   Valor: R$ 185.50
   Prazo: 5 dias úteis

🏆 MELHOR OPÇÃO: Correios PAC
   R$ 45.80 em 8 dias
```

---

## 🚨 Troubleshooting

### Google Maps retorna "REQUEST_DENIED"

**Causa:** API Key inválida ou não autorizada

**Solução:**
1. Verifique se habilitou Distance Matrix API
2. Verifique se o IP está autorizado
3. Verifique se o billing está ativo

### Melhor Envio retorna "Unauthorized"

**Causa:** Token inválido ou expirado

**Solução:**
1. Regere o token no painel
2. Copie o token COMPLETO
3. Confirme se está usando sandbox/produção correto

### Frenet sem transportadoras

**Causa:** CEP fora da área de cobertura ou cadastro incompleto

**Solução:**
1. Verifique se a conta foi aprovada
2. Complete o cadastro da empresa
3. Teste com CEPs de capitais

### Tabela própria com valores irreais

**Causa:** Parâmetros da tabela desconfigurados

**Solução:**
1. Ajuste `frete_por_km` (típico: R$ 1,00-2,00)
2. Ajuste `taxa_base` (típico: R$ 30-80)
3. Ajuste `markup_percentual` (típico: 20-40%)

---

## 💡 Dicas de Otimização

### 1. Cache de Cotações

```python
# Evita requisições repetidas
from functools import lru_cache

@lru_cache(maxsize=100)
def cotar_com_cache(origem, destino, peso, altura, largura, comprimento):
    return cotar_frete_consolidado(...)
```

### 2. Timeout nas APIs

```python
# Evita travamentos
import requests

response = requests.get(url, timeout=5)  # 5 segundos max
```

### 3. Fallback

```python
# Se uma API falhar, usa outra
try:
    cotacoes_melhor_envio = melhor_envio.calcular()
except:
    cotacoes_melhor_envio = []

try:
    cotacoes_frenet = frenet.calcular()
except:
    cotacoes_frenet = []

# Sempre terá ao menos a tabela própria
cotacoes_proprias = calcular_frete_proprio()

todas = cotacoes_melhor_envio + cotacoes_frenet + cotacoes_proprias
```

---

## 🎯 Checklist de Produção

- [ ] Google Maps API criada e configurada
- [ ] Billing do Google Cloud ativo com alertas
- [ ] Melhor Envio conta criada e token obtido
- [ ] Saldo adicionado no Melhor Envio (produção)
- [ ] Frenet conta aprovada e token obtido
- [ ] Tabela de preços própria configurada
- [ ] Todas as variáveis no `.env`
- [ ] Testes de cotação funcionando
- [ ] Cache implementado
- [ ] Fallbacks configurados
- [ ] Monitoramento de custos ativo

---

## 📞 Suporte

**Google Maps:**
- Console: https://console.cloud.google.com
- Suporte: https://cloud.google.com/support

**Melhor Envio:**
- Painel: https://melhorenvio.com.br
- Suporte: https://melhorenvio.com.br/suporte
- WhatsApp: (11) 3230-2023

**Frenet:**
- Painel: https://painel.frenet.com.br
- Suporte: contato@frenet.com.br
- Telefone: (11) 4003-1194

**LogiFlow CRM:**
- Código: `backend/routers/cotacao_automatica.py`
- Integrações: `backend/integrations/frete/`

---

**Última atualização:** 23 de Janeiro de 2026
