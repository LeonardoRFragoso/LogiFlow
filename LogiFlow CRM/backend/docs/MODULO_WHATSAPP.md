# Módulo WhatsApp - LogiFlow CRM

## Visão Geral

O módulo de WhatsApp integra o LogiFlow CRM com WhatsApp Business através da Evolution API, permitindo comunicação automática e eficiente com clientes.

---

## Funcionalidades

### ✅ Notificações Automáticas
- Confirmação de cotação
- Aprovação de pedido
- Atualizações de entrega
- Comprovante de entrega
- Alertas de atraso

### ✅ Comunicação Bidirecional
- Receber mensagens de clientes
- Responder pelo sistema
- Histórico completo no CRM
- Anexos (PDF, imagens)

### ✅ Templates Personalizáveis
- Mensagens pré-configuradas
- Variáveis dinâmicas
- Formatação rica (negrito, itálico)
- Emojis

---

## Configuração Inicial

### 1. Instalar Evolution API

**Docker Compose:**
```bash
cd docker/evolution-api
docker compose -f docker/docker-compose.yml up -d
```

**Verificar Status:**
```bash
docker ps | grep evolution
```

**Acessar Interface:**
```
http://localhost:8080
```

---

### 2. Criar Instância

**Via Interface Web:**
```
1. Acessar http://localhost:8080
2. Clicar em "Nova Instância"
3. Nome: logiflow
4. Gerar QR Code
5. Escanear com WhatsApp
6. Aguardar conexão
```

**Via API:**
```bash
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: logiflow-evolution-key-2025" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "logiflow",
    "qrcode": true
  }'
```

---

### 3. Conectar WhatsApp

**Passo a Passo:**
```
1. Abrir WhatsApp no celular
2. Ir em Configurações > Aparelhos Conectados
3. Clicar em "Conectar um aparelho"
4. Escanear QR Code da Evolution API
5. Aguardar confirmação
6. Pronto! WhatsApp conectado
```

**Verificar Conexão:**
```bash
curl http://localhost:8080/instance/connectionState/logiflow \
  -H "apikey: logiflow-evolution-key-2025"
```

---

### 4. Configurar no LogiFlow

**Arquivo `.env`:**
```env
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=logiflow-evolution-key-2025
EVOLUTION_INSTANCE_NAME=logiflow
```

**Testar Integração:**
```bash
curl http://localhost:8000/whatsapp/status
```

---

## Como Usar

### 1. Enviar Mensagem Manual

**Via Interface:**
```
1. Abrir cliente/pedido
2. Clicar em "Enviar WhatsApp"
3. Selecionar template ou escrever
4. Adicionar anexos (opcional)
5. Enviar
```

**Via API:**
```bash
curl -X POST http://localhost:8000/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "5511999998888",
    "mensagem": "Olá! Sua cotação está pronta.",
    "anexo_url": "https://..."
  }'
```

---

### 2. Notificações Automáticas

**Eventos que Disparam Notificações:**

| Evento | Template | Quando |
|--------|----------|--------|
| Cotação Criada | `cotacao_enviada` | Ao enviar cotação |
| Cotação Aprovada | `cotacao_aprovada` | Cliente aprova |
| Pedido Confirmado | `pedido_confirmado` | Pedido criado |
| Saiu para Entrega | `saiu_entrega` | Início da rota |
| Próximo ao Destino | `proximo_destino` | 5km do destino |
| Entrega Concluída | `entrega_concluida` | Confirmação |
| Atraso Detectado | `atraso_entrega` | Fora do prazo |

**Configurar Notificações:**
```
1. Acessar: Configurações > WhatsApp
2. Selecionar eventos ativos
3. Personalizar templates
4. Salvar
```

---

### 3. Templates de Mensagens

**Template: Cotação Enviada**
```
📋 *Nova Cotação - LogiFlow*

Olá {{cliente_nome}}!

Sua cotação está pronta:

*Número:* {{cotacao_numero}}
*Origem:* {{origem_cidade}}
*Destino:* {{destino_cidade}}
*Valor:* R$ {{valor_total}}
*Prazo:* {{prazo_dias}} dias

📄 Ver detalhes: {{link_cotacao}}

Dúvidas? Responda esta mensagem!
```

**Template: Pedido Confirmado**
```
✅ *Pedido Confirmado - LogiFlow*

Olá {{cliente_nome}}!

Seu pedido foi confirmado:

*Número:* {{pedido_numero}}
*Motorista:* {{motorista_nome}}
*Veículo:* {{veiculo_placa}}
*Coleta:* {{data_coleta}}
*Entrega prevista:* {{data_entrega}}

🔍 Rastrear: {{link_rastreamento}}
```

**Template: Entrega Concluída**
```
🎉 *Entrega Concluída - LogiFlow*

Olá {{cliente_nome}}!

Sua entrega foi concluída com sucesso!

*Pedido:* {{pedido_numero}}
*Entregue em:* {{data_entrega}}
*Recebido por:* {{nome_recebedor}}

📄 Comprovante: {{link_comprovante}}

Obrigado pela confiança! 🚚
```

---

### 4. Variáveis Disponíveis

**Cliente:**
- `{{cliente_nome}}`
- `{{cliente_telefone}}`
- `{{cliente_email}}`

**Cotação:**
- `{{cotacao_numero}}`
- `{{cotacao_data}}`
- `{{origem_cidade}}`
- `{{destino_cidade}}`
- `{{valor_total}}`
- `{{prazo_dias}}`
- `{{link_cotacao}}`

**Pedido:**
- `{{pedido_numero}}`
- `{{pedido_data}}`
- `{{motorista_nome}}`
- `{{motorista_telefone}}`
- `{{veiculo_placa}}`
- `{{data_coleta}}`
- `{{data_entrega}}`
- `{{link_rastreamento}}`

**Entrega:**
- `{{data_entrega}}`
- `{{hora_entrega}}`
- `{{nome_recebedor}}`
- `{{link_comprovante}}`

---

## Formatação de Mensagens

### Estilos de Texto

```
*Negrito*
_Itálico_
~Riscado~
```monospace```

### Emojis Úteis

```
📋 Cotação
📦 Pedido
🚚 Entrega
✅ Confirmado
⚠️ Atenção
🔔 Notificação
📍 Localização
📄 Documento
💰 Valor
⏰ Prazo
```

### Quebras de Linha

```
Linha 1

Linha 2 (duas quebras = espaço)

Linha 3
```

---

## Receber Mensagens

### Webhook Configurado

**Evolution API envia para:**
```
POST http://localhost:8000/whatsapp/webhook
```

**Sistema Processa:**
1. Recebe mensagem
2. Identifica cliente (por número)
3. Registra no histórico do CRM
4. Notifica usuário responsável
5. Pode responder automaticamente

**Respostas Automáticas:**
```
Cliente: "Qual o status do meu pedido?"
Bot: "Consultando... Seu pedido PED-2024-00123 está em trânsito. Previsão de entrega: hoje às 15h. Rastrear: https://..."
```

---

## Histórico de Conversas

**Visualizar no CRM:**
```
1. Abrir cadastro do cliente
2. Aba "WhatsApp"
3. Ver todas as mensagens
4. Enviadas e recebidas
5. Com timestamp
```

**Informações Registradas:**
- Data/Hora
- Direção (enviada/recebida)
- Conteúdo da mensagem
- Anexos
- Status de entrega (✓ ✓)
- Lido pelo cliente

---

## Anexos

### Tipos Suportados

| Tipo | Extensão | Tamanho Máx |
|------|----------|-------------|
| PDF | .pdf | 100 MB |
| Imagem | .jpg, .png | 16 MB |
| Vídeo | .mp4 | 16 MB |
| Áudio | .mp3, .ogg | 16 MB |
| Documento | .doc, .xls | 100 MB |

### Enviar Anexo

**Via API:**
```bash
curl -X POST http://localhost:8000/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "5511999998888",
    "mensagem": "Segue sua cotação em anexo",
    "anexo_url": "https://logiflow.com.br/cotacoes/123.pdf",
    "anexo_nome": "Cotacao-123.pdf"
  }'
```

---

## Relatórios

### Métricas Disponíveis

#### 📊 Volume de Mensagens
- Total enviadas
- Total recebidas
- Por período
- Por cliente

#### ⏱️ Tempo de Resposta
- Tempo médio
- Tempo mínimo/máximo
- Por usuário

#### ✅ Taxa de Entrega
- Mensagens entregues
- Mensagens lidas
- Mensagens falhadas

#### 💬 Engajamento
- Clientes que respondem
- Taxa de resposta
- Conversas ativas

---

## Boas Práticas

### ✅ Fazer

1. **Ser profissional**
   - Linguagem adequada
   - Respostas rápidas
   - Informações claras

2. **Usar templates**
   - Padronização
   - Agilidade
   - Menos erros

3. **Incluir links**
   - Facilita acesso
   - Melhora experiência
   - Reduz dúvidas

4. **Responder rápido**
   - Cliente satisfeito
   - Resolve problemas
   - Aumenta conversão

### ❌ Evitar

1. **Spam**
   - Muitas mensagens
   - Conteúdo irrelevante
   - Cliente bloqueia

2. **Mensagens genéricas**
   - Sem personalização
   - Parecem automáticas
   - Baixo engajamento

3. **Ignorar mensagens**
   - Cliente insatisfeito
   - Perde oportunidade
   - Má reputação

---

## Troubleshooting

### WhatsApp Desconectou

**Causas:**
- Celular sem internet
- WhatsApp desinstalado
- Sessão expirada

**Solução:**
1. Verificar celular
2. Reconectar via QR Code
3. Verificar Evolution API

### Mensagens Não Chegam

**Verificar:**
- Número correto (com DDI)
- WhatsApp ativo
- Não bloqueado
- Limite de mensagens

### Erro ao Enviar Anexo

**Verificar:**
- Tamanho do arquivo
- Formato suportado
- URL acessível
- Permissões

---

## Limites e Restrições

### WhatsApp Business API

| Limite | Valor |
|--------|-------|
| Mensagens/dia | Ilimitado* |
| Tamanho mensagem | 4.096 caracteres |
| Anexo imagem | 16 MB |
| Anexo documento | 100 MB |
| Contatos/lista | 256 |

*Sujeito a políticas do WhatsApp

### Evolution API

| Limite | Valor |
|--------|-------|
| Instâncias | Ilimitado |
| Mensagens/segundo | 10 |
| Webhooks | Ilimitado |
| Armazenamento | Depende do servidor |

---

## Perguntas Frequentes

### Preciso de WhatsApp Business?
Não. Funciona com WhatsApp normal também.

### Posso usar múltiplos números?
Sim. Crie uma instância para cada número.

### As mensagens ficam no meu WhatsApp?
Sim. Tudo fica sincronizado.

### Posso responder pelo celular?
Sim. Funciona normalmente.

### É seguro?
Sim. Usa criptografia end-to-end do WhatsApp.

---

## Suporte

Dúvidas sobre o módulo de WhatsApp:
- Email: suporte@logiflow.com.br
- WhatsApp: (11) 99999-9999
- Documentação: https://docs.logiflow.com.br/whatsapp
- Evolution API: https://doc.evolution-api.com

---

**Última atualização:** 14 de Dezembro de 2024  
**Versão:** 1.0.0
