# Módulo Pedidos - LogiFlow CRM

## Visão Geral

O módulo de Pedidos gerencia todo o ciclo de vida de um pedido de frete, desde a conversão da cotação até a entrega final, incluindo emissão de documentos fiscais e rastreamento.

---

## Funcionalidades

### ✅ Gestão de Pedidos
- Criação manual ou conversão de cotação
- Acompanhamento de status em tempo real
- Designação de motorista e veículo
- Emissão de CT-e/MDF-e
- Rastreamento GPS

### ✅ Controle Operacional
- Planejamento de rotas
- Gestão de entregas
- Registro de ocorrências
- Comprovantes de entrega
- Histórico completo

---

## Como Usar

### 1. Criar Novo Pedido

**Opção 1: Converter Cotação Aprovada**
```
1. Acesse a cotação aprovada
2. Clique em "Converter em Pedido"
3. Sistema cria pedido automaticamente
4. Todos os dados são transferidos
```

**Opção 2: Criar Manualmente**
```
Caminho: Menu > Pedidos > Novo Pedido

Preencher:
- Cliente
- Origem e Destino
- Dados da carga
- Valores
- Data de coleta
```

---

### 2. Designar Motorista e Veículo

**Passo a Passo:**
```
1. Abrir pedido
2. Aba "Operacional"
3. Selecionar Motorista
4. Selecionar Veículo
5. Definir Data/Hora de Coleta
6. Salvar
```

**Sistema verifica:**
- ✅ Motorista disponível
- ✅ CNH válida
- ✅ Veículo disponível
- ✅ Capacidade adequada
- ✅ Documentação em dia

---

### 3. Emitir CT-e

**Pré-requisitos:**
- Pedido confirmado
- Motorista e veículo designados
- Dados fiscais completos

**Processo:**
```
1. Abrir pedido
2. Aba "Fiscal"
3. Clicar em "Emitir CT-e"
4. Revisar dados
5. Confirmar emissão
6. Aguardar autorização SEFAZ
7. Download do XML/PDF
```

**Dados Necessários:**
- CNPJ/CPF do tomador
- Inscrição Estadual
- Endereço completo
- Valor da carga
- CFOP
- Natureza da operação

---

### 4. Acompanhar Entrega

**Status do Pedido:**

| Status | Descrição | Ações |
|--------|-----------|-------|
| 🟡 Pendente | Aguardando designação | Designar motorista |
| 🔵 Confirmado | Motorista designado | Iniciar coleta |
| 🟣 Em Coleta | Coletando mercadoria | Confirmar coleta |
| 🟢 Em Trânsito | Mercadoria em transporte | Rastrear |
| 🟠 Em Entrega | Chegou ao destino | Confirmar entrega |
| ✅ Entregue | Entrega concluída | Registrar comprovante |
| 🔴 Cancelado | Pedido cancelado | - |

**Rastreamento:**
- Localização em tempo real (GPS)
- Histórico de movimentações
- Previsão de chegada
- Alertas de atraso

---

### 5. Registrar Ocorrências

**Tipos de Ocorrências:**
- Atraso
- Avaria
- Destinatário ausente
- Endereço incorreto
- Recusa de recebimento
- Outros

**Como Registrar:**
```
1. Abrir pedido
2. Aba "Ocorrências"
3. Clicar em "Nova Ocorrência"
4. Preencher:
   - Tipo
   - Descrição
   - Data/Hora
   - Fotos (opcional)
5. Salvar
```

---

### 6. Confirmar Entrega

**Processo:**
```
1. Motorista chega ao destino
2. Entrega a mercadoria
3. Coleta assinatura/foto
4. Registra no app
5. Sistema atualiza status
6. Cliente recebe notificação
```

**Comprovante de Entrega:**
- Assinatura digital
- Foto do comprovante
- Nome do recebedor
- Data/Hora
- Observações

---

## Campos do Pedido

### Identificação

| Campo | Tipo | Descrição |
|-------|------|-----------|
| Número | Texto | Gerado automaticamente (PED-2024-00001) |
| Data | Data | Data de criação |
| Status | Seleção | Status atual |
| Cotação Origem | Referência | Cotação que originou (se aplicável) |

### Cliente e Rota

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Cliente | Seleção | ✅ Sim | Cliente solicitante |
| Origem | Endereço | ✅ Sim | Local de coleta |
| Destino | Endereço | ✅ Sim | Local de entrega |
| Distância | Número | Não | Calculado automaticamente (km) |

### Carga

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Tipo Carga | Seleção | ✅ Sim | Fracionada/Lotação/Container |
| Peso (kg) | Número | ✅ Sim | Peso total |
| Volume (m³) | Número | Não | Volume total |
| Valor Mercadoria | Moeda | Não | Para seguro |
| Descrição | Texto | Não | Descrição dos itens |
| Número NF | Texto | Não | Número da nota fiscal |

### Operacional

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Motorista | Seleção | Não | Motorista designado |
| Veículo | Seleção | Não | Veículo designado |
| Data Coleta | Data/Hora | Não | Agendamento de coleta |
| Data Entrega Prevista | Data | Não | Previsão de entrega |
| Data Entrega Real | Data/Hora | Não | Entrega efetiva |

### Fiscal

| Campo | Tipo | Descrição |
|-------|------|-----------|
| CT-e Número | Texto | Número do CT-e |
| CT-e Chave | Texto | Chave de acesso (44 dígitos) |
| CT-e Status | Seleção | Pendente/Emitido/Cancelado |
| CT-e Data Emissão | Data/Hora | Data de autorização |
| CT-e XML | Arquivo | XML autorizado |
| CT-e PDF | Arquivo | DACTE em PDF |

### Valores

| Campo | Tipo | Descrição |
|-------|------|-----------|
| Tipo Frete | Seleção | CIF ou FOB |
| Valor Frete | Moeda | Valor do transporte |
| Valor Pedágio | Moeda | Custo de pedágios |
| Valor Seguro | Moeda | Custo do seguro |
| Valor Outros | Moeda | Outros custos |
| Desconto | Moeda | Desconto aplicado |
| Valor Total | Moeda | Valor final |

---

## Fluxo Completo do Pedido

```
1. CRIAÇÃO
   └── Cotação aprovada ou criação manual
   └── Dados básicos preenchidos
   └── Status: Pendente

2. PLANEJAMENTO
   └── Designar motorista e veículo
   └── Agendar coleta
   └── Status: Confirmado

3. COLETA
   └── Motorista vai ao local
   └── Coleta mercadoria
   └── Confirma no app
   └── Status: Em Coleta → Em Trânsito

4. EMISSÃO FISCAL
   └── Emitir CT-e
   └── Aguardar autorização SEFAZ
   └── Download XML/PDF
   └── CT-e Status: Emitido

5. TRANSPORTE
   └── Rastreamento GPS ativo
   └── Atualizações de localização
   └── Status: Em Trânsito

6. ENTREGA
   └── Chegada ao destino
   └── Entrega da mercadoria
   └── Coleta de assinatura/foto
   └── Status: Em Entrega → Entregue

7. FINALIZAÇÃO
   └── Comprovante registrado
   └── Cliente notificado
   └── Pedido arquivado
   └── Status: Entregue ✅
```

---

## Integrações

### WhatsApp
- Notificação de confirmação
- Atualizações de status
- Link de rastreamento
- Comprovante de entrega

### Google Maps
- Cálculo de distância
- Sugestão de rota
- Tempo estimado
- Rastreamento em mapa

### Focus NFe
- Emissão de CT-e
- Consulta de status
- Cancelamento
- Download de documentos

---

## Relatórios

### Relatórios Disponíveis

#### 📊 Pedidos por Status
- Distribuição atual
- Pedidos atrasados
- Pedidos do dia

#### 💰 Faturamento
- Valor total por período
- Ticket médio
- Margem de lucro

#### 🚚 Performance de Entregas
- Taxa de entrega no prazo
- Tempo médio de entrega
- Ocorrências por tipo

#### 👤 Performance de Motoristas
- Entregas por motorista
- Taxa de sucesso
- Avaliações

---

## Boas Práticas

### ✅ Fazer

1. **Designar rapidamente**
   - Não deixar pedidos pendentes
   - Planejar com antecedência
   - Otimizar rotas

2. **Emitir CT-e antes do transporte**
   - Obrigatório por lei
   - Evita multas
   - Facilita fiscalização

3. **Manter cliente informado**
   - Enviar atualizações
   - Responder dúvidas
   - Ser proativo

4. **Registrar tudo**
   - Ocorrências
   - Comunicações
   - Comprovantes

### ❌ Evitar

1. **Transportar sem CT-e**
   - Ilegal
   - Multa pesada
   - Apreensão de carga

2. **Não rastrear**
   - Cliente fica no escuro
   - Dificulta gestão
   - Perde controle

3. **Ignorar ocorrências**
   - Problemas se agravam
   - Cliente insatisfeito
   - Prejuízos maiores

---

## Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl + N` | Novo Pedido |
| `Ctrl + S` | Salvar |
| `Ctrl + E` | Emitir CT-e |
| `Ctrl + R` | Rastrear |
| `Esc` | Cancelar |

---

## Perguntas Frequentes

### Como cancelar um pedido?
1. Abrir pedido
2. Clicar em "Cancelar"
3. Informar motivo
4. Confirmar
5. Se CT-e emitido, cancelar também

### Como reagendar coleta?
1. Abrir pedido
2. Aba "Operacional"
3. Alterar data/hora de coleta
4. Notificar motorista
5. Salvar

### Como adicionar parada intermediária?
1. Abrir pedido
2. Aba "Rota"
3. Clicar em "Adicionar Parada"
4. Informar endereço
5. Salvar

### O que fazer se houver avaria?
1. Registrar ocorrência
2. Fotografar dano
3. Notificar cliente
4. Acionar seguro
5. Documentar tudo

---

## Suporte

Dúvidas sobre o módulo de Pedidos:
- Email: suporte@logiflow.com.br
- WhatsApp: (11) 99999-9999
- Documentação: https://docs.logiflow.com.br/pedidos

---

**Última atualização:** 14 de Dezembro de 2024  
**Versão:** 1.0.0
