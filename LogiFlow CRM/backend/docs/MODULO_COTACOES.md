# Módulo Cotações - LogiFlow CRM

## Visão Geral

O módulo de Cotações permite criar, gerenciar e acompanhar propostas de frete de forma rápida e eficiente, com cálculo automático de valores e integração com APIs de cotação.

---

## Funcionalidades

### ✅ Criação de Cotações
- Cálculo automático de frete
- Integração com Melhor Envio
- Múltiplas opções de transportadoras
- Comparação com tabela própria

### ✅ Gestão de Propostas
- Status da cotação (rascunho, enviada, aprovada, rejeitada)
- Histórico de alterações
- Envio automático por email/WhatsApp
- Validade configurável

### ✅ Conversão em Pedido
- Conversão automática ao aprovar
- Transferência de todos os dados
- Geração de número de pedido

---

## Como Usar

### 1. Criar Nova Cotação

**Caminho:** Menu > Cotações > Nova Cotação

**Passo a Passo:**

#### 1.1 Dados do Cliente
```
Cliente: [Selecionar ou criar novo]
Contato: [Nome do solicitante]
Email: [Para envio da cotação]
Telefone: [Para contato]
```

#### 1.2 Origem e Destino
```
Origem:
  CEP: 01310-100
  Cidade: São Paulo - SP
  Endereço: [Opcional]

Destino:
  CEP: 04101-300
  Cidade: São Paulo - SP
  Endereço: [Opcional]
```

#### 1.3 Dados da Carga
```
Tipo de Carga: [Fracionada/Lotação/Container/Granel]
Peso Total: 500 kg
Volume: 2 m³
Valor da Mercadoria: R$ 5.000,00
Descrição: [Descrição dos itens]
```

#### 1.4 Tipo de Frete
```
☐ CIF (Remetente paga)
☐ FOB (Destinatário paga)
```

#### 1.5 Informações Adicionais
```
Data Coleta Desejada: [Data]
☐ Urgente
Observações: [Instruções especiais]
```

---

### 2. Calcular Frete Automaticamente

**Opção 1: Melhor Envio**
- Clique em "Cotar com Melhor Envio"
- Sistema busca opções de múltiplas transportadoras
- Exibe preços e prazos
- Selecione a melhor opção

**Opção 2: Tabela Própria**
- Sistema calcula baseado na distância e peso
- Aplica tabela de preços configurada
- Adiciona pedágio e seguro automaticamente

**Opção 3: Comparação**
- Clique em "Comparar Opções"
- Sistema mostra tabela própria vs Melhor Envio
- Indica economia potencial
- Sugere melhor opção

---

### 3. Definir Valores

**Composição do Valor Total:**
```
Valor do Frete:     R$ 450,00
+ Pedágio:          R$  80,00
+ Seguro:           R$  50,00
+ Outros:           R$  20,00
- Desconto:         R$   0,00
─────────────────────────────
= Valor Total:      R$ 600,00
```

**Prazo de Entrega:** 3 dias úteis

---

### 4. Enviar Cotação

**Opções de Envio:**

#### 📧 Email
- Assunto personalizado
- PDF anexado
- Link para acompanhamento

#### 📱 WhatsApp
- Mensagem automática
- PDF da cotação
- Link para aprovação

#### 🖨️ Imprimir
- Formato profissional
- Logo da empresa
- Todas as informações

---

### 5. Acompanhar Status

**Status Disponíveis:**

| Status | Descrição | Ações Disponíveis |
|--------|-----------|-------------------|
| 🟡 Rascunho | Cotação em elaboração | Editar, Enviar, Excluir |
| 🔵 Enviada | Aguardando resposta | Editar, Cancelar |
| 🟢 Aprovada | Cliente aprovou | Converter em Pedido |
| 🔴 Rejeitada | Cliente recusou | Revisar, Duplicar |
| ⚫ Expirada | Validade vencida | Renovar |
| ✅ Convertida | Virou pedido | Visualizar Pedido |

---

## Campos da Cotação

### Identificação

| Campo | Tipo | Descrição |
|-------|------|-----------|
| Número | Texto | Gerado automaticamente (COT-2024-00001) |
| Data | Data | Data de criação |
| Validade | Data | Data de expiração (padrão: 15 dias) |
| Status | Seleção | Status atual |

### Cliente

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Cliente | Seleção | ✅ Sim | Cliente solicitante |
| Contato | Texto | Não | Nome do solicitante |
| Email | Email | Não | Para envio |
| Telefone | Texto | Não | Para contato |

### Rota

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Origem CEP | Número | ✅ Sim | CEP de coleta |
| Origem Cidade | Texto | Não | Preenchido automaticamente |
| Origem UF | Texto | Não | Preenchido automaticamente |
| Destino CEP | Número | ✅ Sim | CEP de entrega |
| Destino Cidade | Texto | Não | Preenchido automaticamente |
| Destino UF | Texto | Não | Preenchido automaticamente |

### Carga

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Tipo Carga | Seleção | ✅ Sim | Fracionada/Lotação/Container/Granel |
| Peso (kg) | Número | ✅ Sim | Peso total em kg |
| Volume (m³) | Número | Não | Volume em metros cúbicos |
| Valor Mercadoria | Moeda | Não | Para cálculo de seguro |
| Descrição | Texto | Não | Descrição dos itens |

### Valores

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Tipo Frete | Seleção | ✅ Sim | CIF ou FOB |
| Valor Frete | Moeda | ✅ Sim | Valor do transporte |
| Valor Pedágio | Moeda | Não | Custo de pedágios |
| Valor Seguro | Moeda | Não | Custo do seguro |
| Valor Outros | Moeda | Não | Outros custos |
| Desconto | Moeda | Não | Desconto aplicado |
| Valor Total | Moeda | ✅ Sim | Valor final |

---

## Integração com Melhor Envio

### Como Funciona

1. **Preencher dados da cotação**
2. **Clicar em "Cotar com Melhor Envio"**
3. **Sistema consulta API**
4. **Retorna opções de transportadoras:**
   - Correios PAC
   - Correios SEDEX
   - Jadlog
   - Azul Cargo
   - Outras

5. **Comparar preços e prazos**
6. **Selecionar melhor opção**
7. **Aplicar à cotação**

### Exemplo de Resultado

```
┌─────────────────────────────────────────────────────┐
│ OPÇÕES DE FRETE - São Paulo → Rio de Janeiro       │
├─────────────────────────────────────────────────────┤
│ Correios PAC                                        │
│ Prazo: 8 dias | Valor: R$ 45,80                   │
│ ✅ Mais econômico                                   │
├─────────────────────────────────────────────────────┤
│ Correios SEDEX                                      │
│ Prazo: 3 dias | Valor: R$ 78,50                   │
│ ⚡ Mais rápido                                      │
├─────────────────────────────────────────────────────┤
│ Jadlog Package                                      │
│ Prazo: 5 dias | Valor: R$ 52,30                   │
├─────────────────────────────────────────────────────┤
│ Frota Própria (Tabela)                             │
│ Prazo: 4 dias | Valor: R$ 120,00                  │
│ 💰 Economia de R$ 74,20 (61%) com Melhor Envio    │
└─────────────────────────────────────────────────────┘
```

---

## Relatórios

### Relatórios Disponíveis

#### 📊 Cotações por Status
- Distribuição por status
- Taxa de conversão
- Tempo médio de resposta

#### 💰 Análise de Valores
- Ticket médio
- Valor total cotado
- Valor convertido em pedidos

#### 📈 Performance
- Taxa de aprovação
- Taxa de rejeição
- Motivos de rejeição

#### 🎯 Por Vendedor
- Cotações por usuário
- Taxa de conversão
- Valor médio

---

## Boas Práticas

### ✅ Fazer

1. **Preencher todos os dados**
   - Quanto mais completo, melhor
   - Facilita cálculo automático
   - Evita retrabalho

2. **Usar cotação automática**
   - Economiza tempo
   - Preços competitivos
   - Comparação facilitada

3. **Definir validade adequada**
   - Padrão: 15 dias
   - Ajustar conforme necessário
   - Renovar se expirar

4. **Acompanhar status**
   - Fazer follow-up
   - Registrar feedback
   - Atualizar conforme necessário

### ❌ Evitar

1. **Cotações incompletas**
   - Dificulta aprovação
   - Gera dúvidas
   - Atrasa processo

2. **Valores irreais**
   - Prejudica credibilidade
   - Causa rejeição
   - Perde cliente

3. **Falta de follow-up**
   - Cotação esquecida
   - Oportunidade perdida
   - Cliente insatisfeito

---

## Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl + N` | Nova Cotação |
| `Ctrl + S` | Salvar |
| `Ctrl + E` | Enviar |
| `Ctrl + D` | Duplicar |
| `Esc` | Cancelar |

---

## Perguntas Frequentes

### Como duplicar uma cotação?
1. Abra a cotação original
2. Clique em "Duplicar"
3. Sistema cria cópia com novo número
4. Edite conforme necessário

### Como renovar cotação expirada?
1. Abra a cotação expirada
2. Clique em "Renovar"
3. Sistema atualiza validade
4. Revise valores se necessário

### Como converter em pedido?
1. Cotação deve estar "Aprovada"
2. Clique em "Converter em Pedido"
3. Sistema cria pedido automaticamente
4. Redireciona para tela do pedido

### Como calcular frete manualmente?
Use a fórmula:
```
Frete = (Distância × Peso × Fator) + Pedágio + Seguro
```

---

## Suporte

Dúvidas sobre o módulo de Cotações:
- Email: suporte@logiflow.com.br
- WhatsApp: (11) 99999-9999
- Documentação: https://docs.logiflow.com.br/cotacoes

---

**Última atualização:** 14 de Dezembro de 2024  
**Versão:** 1.0.0
