# Integração Melhor Envio - LogiFlow CRM

## Visão Geral

A integração com Melhor Envio permite cotação automática de frete com múltiplas transportadoras (Correios, Jadlog, Azul Cargo, etc.), comparação de preços e decisão inteligente entre frota própria ou terceirização.

## Configuração

### 1. Obter Token de Acesso

1. Crie uma conta em: https://melhorenvio.com.br
2. Acesse: Configurações > Tokens de acesso
3. Gere um novo token com permissões:
   - `shipping-calculate`
   - `shipping-tracking`
   - `agencies-read`

### 2. Configurar no .env

```env
MELHOR_ENVIO_TOKEN=seu_token_aqui
MELHOR_ENVIO_SANDBOX=True  # False para produção
```

## Funcionalidades

### ✅ Cotação de Frete

- Cálculo automático com múltiplas transportadoras
- Suporte a dimensões personalizadas ou automáticas
- Valor declarado para seguro
- Filtro por serviços específicos

### ✅ Comparação Inteligente

- Melhor preço vs. melhor prazo
- Comparação com tabela própria
- Recomendação automática (terceirizar ou frota própria)
- Cálculo de economia potencial

### ✅ Rastreamento

- Rastreamento por código
- Histórico de movimentações
- Status em tempo real

### ✅ Agências

- Busca de agências por CEP
- Filtro por transportadora
- Informações de endereço e horário

---

## Endpoints Disponíveis

### Cotação de Frete

#### POST /melhor-envio/calcular
Calcula frete com dimensões específicas

**Request:**
```json
{
  "origem_cep": "01310100",
  "destino_cep": "04101300",
  "peso_kg": 10.5,
  "altura_cm": 20,
  "largura_cm": 30,
  "comprimento_cm": 40,
  "valor_mercadoria": 1500.00,
  "servicos": [1, 2, 3]
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "transportadora": "Correios",
      "servico": "PAC",
      "valor": 45.80,
      "prazo_dias": 8,
      "disponivel": true,
      "detalhes": {
        "company_id": 1,
        "service_id": 1,
        "discount": 0,
        "currency": "BRL"
      }
    },
    {
      "transportadora": "Correios",
      "servico": "SEDEX",
      "valor": 78.50,
      "prazo_dias": 3,
      "disponivel": true
    }
  ],
  "total_opcoes": 5,
  "opcoes_disponiveis": 5
}
```

#### POST /melhor-envio/calcular-simples
Calcula frete com dimensões automáticas (ideal para cotações rápidas)

**Request:**
```json
{
  "origem_cep": "01310100",
  "destino_cep": "04101300",
  "peso_kg": 10.5,
  "valor_mercadoria": 1500.00
}
```

#### POST /melhor-envio/melhor-cotacao
Retorna a melhor cotação baseada em critério

**Request:**
```json
{
  "origem_cep": "01310100",
  "destino_cep": "04101300",
  "peso_kg": 10.5,
  "prioridade": "preco"  // ou "prazo"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transportadora": "Correios",
    "servico": "PAC",
    "valor": 45.80,
    "prazo_dias": 8
  },
  "criterio": "preco",
  "total_opcoes": 5
}
```

#### POST /melhor-envio/comparar-tabela
Compara cotações do mercado com tabela própria

**Request:**
```json
{
  "origem_cep": "01310100",
  "destino_cep": "04101300",
  "peso_kg": 10.5,
  "valor_tabela_propria": 120.00,
  "valor_mercadoria": 1500.00
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "valor_tabela_propria": 120.00,
    "menor_preco_mercado": 45.80,
    "economia_potencial": 74.20,
    "percentual_economia": 61.83,
    "recomendacao": "terceirizar",
    "cotacoes_disponiveis": [...]
  }
}
```

---

### Rastreamento

#### GET /melhor-envio/rastrear/{tracking_code}
Rastreia envio pelo código

**Response:**
```json
{
  "success": true,
  "data": {
    "tracking_code": "BR123456789BR",
    "status": "em_transito",
    "events": [
      {
        "date": "2024-12-14T10:30:00",
        "description": "Objeto em trânsito",
        "location": "São Paulo - SP"
      }
    ]
  }
}
```

---

### Agências

#### GET /melhor-envio/agencias?cep=01310100
Busca agências próximas

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "name": "Agência Correios - Centro",
      "address": "Av. Paulista, 1000",
      "phone": "(11) 3000-0000",
      "distance_km": 2.5
    }
  ]
}
```

---

### Informações

#### GET /melhor-envio/servicos
Lista serviços disponíveis

**Response:**
```json
{
  "success": true,
  "data": [
    {"id": 1, "nome": "Correios PAC", "tipo": "econômico"},
    {"id": 2, "nome": "Correios SEDEX", "tipo": "expresso"},
    {"id": 3, "nome": "Jadlog Package", "tipo": "econômico"},
    {"id": 4, "nome": "Azul Cargo Express", "tipo": "expresso"}
  ]
}
```

#### GET /melhor-envio/status
Verifica status da integração

**Response:**
```json
{
  "success": true,
  "data": {
    "configurado": true,
    "ambiente": "sandbox",
    "ativo": true
  }
}
```

---

## Casos de Uso

### 1. Cotação Automática no Pedido

Quando o cliente solicita uma cotação, o sistema automaticamente:
1. Calcula frete com Melhor Envio
2. Calcula frete com tabela própria
3. Compara os valores
4. Recomenda a melhor opção
5. Apresenta todas as opções ao cliente

```python
# Exemplo de integração no fluxo de cotação
async def criar_cotacao_com_frete_automatico(cotacao_data):
    # 1. Calcular frete com Melhor Envio
    frete_mercado = await melhor_envio.calcular_frete_simples(
        origem_cep=cotacao_data["origem_cep"],
        destino_cep=cotacao_data["destino_cep"],
        peso_kg=cotacao_data["peso_kg"]
    )
    
    # 2. Calcular frete com tabela própria
    frete_proprio = calcular_tabela_propria(
        distancia=cotacao_data["distancia_km"],
        peso=cotacao_data["peso_kg"]
    )
    
    # 3. Comparar e recomendar
    comparacao = await melhor_envio.comparar_com_tabela_propria(
        origem_cep=cotacao_data["origem_cep"],
        destino_cep=cotacao_data["destino_cep"],
        peso_kg=cotacao_data["peso_kg"],
        valor_tabela_propria=frete_proprio
    )
    
    # 4. Retornar opções
    return {
        "opcoes": [
            {"tipo": "frota_propria", "valor": frete_proprio},
            *comparacao["data"]["cotacoes_disponiveis"]
        ],
        "recomendacao": comparacao["data"]["recomendacao"]
    }
```

### 2. Dashboard de Economia

Monitorar quanto a empresa economiza usando o Melhor Envio:

```sql
SELECT 
    COUNT(*) as total_fretes_terceirizados,
    SUM(valor_tabela_propria - valor_terceiro) as economia_total,
    AVG(valor_tabela_propria - valor_terceiro) as economia_media
FROM pedidos
WHERE tipo_frete = 'terceirizado'
    AND data >= DATE_SUB(NOW(), INTERVAL 30 DAY)
```

### 3. Sugestão Inteligente

Ao criar pedido, sugerir automaticamente se vale a pena terceirizar:

```python
if comparacao["economia_potencial"] > 50:  # R$ 50 de economia
    sugestao = "Recomendamos terceirizar este frete"
elif comparacao["percentual_economia"] > 30:  # 30% de economia
    sugestao = "Terceirização pode ser vantajosa"
else:
    sugestao = "Frota própria é mais econômica"
```

---

## Dimensões Automáticas

Quando não se conhece as dimensões exatas, o sistema calcula automaticamente baseado no peso:

| Peso (kg) | Altura (cm) | Largura (cm) | Comprimento (cm) |
|-----------|-------------|--------------|------------------|
| 0-30 | 20 | 30 | 40 |
| 31-100 | 30 | 40 | 60 |
| 101-300 | 40 | 60 | 80 |
| 301+ | 60 | 80 | 120 |

---

## Limites e Restrições

### Melhor Envio API

- **Rate Limit:** 120 requisições/minuto
- **Peso máximo:** 300kg (varia por transportadora)
- **Dimensões máximas:** 200cm (soma das dimensões)
- **Valor máximo declarado:** R$ 10.000,00

### Transportadoras

| Transportadora | Peso Max | Dimensão Max | Prazo Médio |
|----------------|----------|--------------|-------------|
| Correios PAC | 30kg | 200cm | 8-12 dias |
| Correios SEDEX | 30kg | 200cm | 2-4 dias |
| Jadlog | 150kg | 300cm | 3-7 dias |
| Azul Cargo | 300kg | 400cm | 2-5 dias |

---

## Tratamento de Erros

### Erros Comuns

**1. CEP inválido**
```json
{
  "success": false,
  "error": "CEP deve conter 8 dígitos"
}
```

**2. Peso excede limite**
```json
{
  "success": false,
  "message": "Peso excede o limite de 300kg"
}
```

**3. Nenhuma cotação disponível**
```json
{
  "success": false,
  "message": "Nenhuma cotação disponível para esta rota"
}
```

---

## Custos

### Melhor Envio

- **Plano Gratuito:** Até 100 cotações/mês
- **Plano Básico:** R$ 49/mês - 1.000 cotações
- **Plano Pro:** R$ 199/mês - 10.000 cotações
- **Plano Enterprise:** Negociar

### Comissão

O Melhor Envio cobra comissão sobre fretes contratados:
- Correios: 5-10%
- Transportadoras privadas: 10-15%

---

## Monitoramento

### Logs

Todos os eventos são registrados:
```
2024-12-14 14:30:15 | INFO | Cotação Melhor Envio: SP → RJ, 10kg, 5 opções
2024-12-14 14:30:20 | INFO | Economia potencial: R$ 74,20 (61.83%)
```

### Métricas

Acompanhe no dashboard:
- Total de cotações realizadas
- Taxa de conversão (cotação → contratação)
- Economia total gerada
- Transportadora mais utilizada

---

## Suporte

- Email: suporte@logiflow.com.br
- Documentação Melhor Envio: https://docs.melhorenvio.com.br
- API Reference: https://api.logiflow.com.br/docs
