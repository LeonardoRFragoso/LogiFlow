# Módulo WhatsApp - Integração Evolution API

## 📋 Visão Geral

O Módulo WhatsApp do LogiFlow CRM oferece integração completa com WhatsApp Business através da Evolution API, incluindo chatbot inteligente, histórico completo de conversas e sincronização automática com o CRM.

## 🎯 Funcionalidades Implementadas

### ✅ Backend Completo

#### Models de Persistência
- **WhatsAppMessage**: Armazena todas as mensagens com metadados completos
- **WhatsAppConversation**: Agrupa mensagens por conversa com estatísticas
- **WhatsAppConfig**: Configurações por tenant (multi-tenancy)

#### Endpoints da API

**Envio de Mensagens**
- `POST /whatsapp/enviar/texto` - Enviar mensagem de texto
- `POST /whatsapp/enviar/imagem` - Enviar imagem
- `POST /whatsapp/enviar/documento` - Enviar documento (PDF, etc)
- `POST /whatsapp/enviar/localizacao` - Enviar localização

**Notificações Automáticas**
- `POST /whatsapp/notificar/pedido` - Notificações de status de pedido
- `POST /whatsapp/notificar/motorista` - Notificações para motoristas

**Conversas e Histórico**
- `GET /whatsapp/conversas` - Listar conversas com filtros
- `GET /whatsapp/conversas/{id}/mensagens` - Obter mensagens de uma conversa
- `GET /whatsapp/mensagens` - Listar mensagens com filtros avançados
- `POST /whatsapp/conversas/{id}/marcar-lida` - Marcar conversa como lida
- `PATCH /whatsapp/conversas/{id}/arquivar` - Arquivar conversa

**Configurações**
- `GET /whatsapp/config` - Obter configurações
- `PUT /whatsapp/config` - Atualizar configurações
- `GET /whatsapp/status-conexao` - Verificar status da conexão

**Dashboard e Métricas**
- `GET /whatsapp/dashboard` - Estatísticas completas
- `GET /whatsapp/qrcode` - Obter QR Code para conexão

**Webhook**
- `POST /whatsapp/webhook` - Webhook básico
- `POST /whatsapp/webhook/enhanced` - Webhook com chatbot e persistência

#### Serviços

1. **WhatsAppService** (`services/whatsapp_service.py`)
   - Cliente completo Evolution API
   - Gerenciamento de instâncias
   - Envio de mensagens
   - Templates de notificação

2. **ChatbotService** (`services/chatbot_service.py`)
   - Reconhecimento de intenções
   - Extração de dados estruturados
   - Respostas contextualizadas
   - Verificação de horário comercial
   - Geração de menu interativo

3. **WhatsAppCRMSync** (`services/whatsapp_crm_sync.py`)
   - Criar leads de conversas
   - Criar casos de atendimento
   - Vincular conversas a clientes/pedidos
   - Sincronizar mensagens com timeline do CRM
   - Buscar cliente por telefone

### ✅ Frontend Completo

#### Views Criadas

1. **DashboardWhatsAppView** - Dashboard com métricas
   - Total de mensagens (enviadas/recebidas)
   - Taxa de automação do bot
   - Conversas ativas e não lidas
   - Gráficos de mensagens por dia
   - Top intenções do chatbot
   - Conversas recentes
   - Ações rápidas

2. **ConversasWhatsAppView** - Interface de chat completa
   - Lista de conversas com busca e filtros
   - Chat em tempo real
   - Indicadores de mensagens não lidas
   - Visualização de intenções do bot
   - Painel de detalhes da conversa
   - Ações: marcar como lida, arquivar
   - Criar lead ou caso da conversa

3. **ConfiguracaoWhatsAppView** - Configurações
   - Status de conexão WhatsApp
   - Conectar via QR Code
   - Configurações do chatbot
   - Horário comercial
   - Notificações automáticas por tipo de evento

#### Rotas Configuradas

```javascript
{ path: 'whatsapp/dashboard', name: 'DashboardWhatsApp' }
{ path: 'whatsapp/conversas', name: 'ConversasWhatsApp' }
{ path: 'whatsapp/config', name: 'ConfiguracaoWhatsApp' }
```

---

## 🚀 Como Usar

### 1. Configuração da Evolution API

#### Instalar Evolution API

```bash
# Docker
docker run -d \
  --name evolution-api \
  -p 8080:8080 \
  -e API_KEY=sua_chave_api_aqui \
  atendai/evolution-api:latest
```

#### Configurar no Backend

Adicione ao `.env`:

```env
# Evolution API
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_chave_api_aqui
EVOLUTION_INSTANCE_NAME=logiflow
```

### 2. Criar Tabelas no Banco

As tabelas serão criadas automaticamente ao iniciar a aplicação:

```bash
# Reiniciar o backend
python main.py
```

### 3. Configurar WhatsApp

1. Acesse **WhatsApp > Configurações**
2. Clique em **Conectar WhatsApp**
3. Escaneie o QR Code com seu WhatsApp
4. Configure as preferências do chatbot
5. Habilite notificações automáticas desejadas

### 4. Usar o Sistema

#### Chat com Clientes
1. Acesse **WhatsApp > Conversas**
2. Clique em uma conversa para abrir
3. Digite mensagens na área de chat
4. Veja o histórico completo
5. Marque como lida ou arquive

#### Dashboard
1. Acesse **WhatsApp > Dashboard**
2. Visualize métricas em tempo real
3. Selecione período (hoje, semana, mês)
4. Veja gráficos e estatísticas

---

## 🤖 Chatbot Inteligente

### Intenções Reconhecidas

O chatbot reconhece automaticamente:

- **📦 Rastreamento**: "rastreio", "onde está", "localização"
- **📋 Status Pedido**: "status", "situação", "andamento"
- **📅 Prazo**: "prazo", "quanto tempo", "previsão"
- **❌ Cancelamento**: "cancelar", "desistir"
- **❓ Dúvidas**: "dúvida", "ajuda", "suporte"
- **🕐 Horário**: "horário", "atendimento"
- **💰 Preço**: "preço", "valor", "cotação"
- **👋 Saudação**: "oi", "olá", "bom dia"
- **🙏 Agradecimento**: "obrigado", "valeu"

### Extração de Dados

O chatbot extrai automaticamente:
- Códigos de rastreio
- Números de pedido
- Telefones
- CPF/CNPJ

### Respostas Contextualizadas

O bot gera respostas personalizadas baseadas:
- Na intenção detectada
- Nos dados extraídos
- No histórico da conversa
- No horário (comercial ou não)

---

## 📊 Notificações Automáticas

### Tipos de Notificação

Configure quais eventos enviarão notificações:

1. **✅ Pedido Confirmado**
   - Enviado quando pedido é confirmado
   - Inclui número do pedido e código de rastreio

2. **📦 Coleta Realizada**
   - Enviado quando carga é coletada
   - Inclui nome do motorista

3. **🚛 Em Trânsito**
   - Enviado durante o transporte
   - Inclui localização atual e previsão

4. **🎉 Saiu para Entrega**
   - Enviado quando sai para entrega final
   - Inclui dados do motorista e veículo

5. **✅ Entregue**
   - Enviado após entrega concluída
   - Solicita avaliação

6. **⚠️ Ocorrência**
   - Enviado em caso de problemas
   - Inclui descrição e ação tomada

### Templates Personalizados

Mensagens seguem templates profissionais com:
- Emojis para facilitar leitura
- Formatação em negrito
- Links para rastreamento
- Informações relevantes do pedido

---

## 🔗 Sincronização com CRM

### Automações Disponíveis

#### Criar Lead Automaticamente
Quando um novo cliente inicia conversa:
- Lead criado no CRM
- Telefone vinculado
- Observações com histórico

#### Criar Caso de Atendimento
Para dúvidas complexas:
- Caso aberto automaticamente
- Histórico da conversa anexado
- Categoria definida pela intenção

#### Vincular a Cliente/Pedido
- Busca automática por telefone
- Vinculação de conversas
- Timeline atualizada

#### Sincronizar Timeline
- Todas as mensagens no histórico do cliente
- Filtro por tipo (enviadas/recebidas)
- Marcação de origem WhatsApp

---

## ⚙️ Configurações Avançadas

### Chatbot

**Horário Comercial**
- Defina horários de funcionamento
- Dias da semana específicos
- Mensagem fora do horário personalizada

**Respostas Automáticas**
- Habilitar/desabilitar bot
- Mensagem de boas-vindas customizada
- Funcionamento apenas em horário comercial

### Notificações

Configure individualmente cada tipo de notificação:
- Pedido confirmado
- Coleta realizada
- Em trânsito
- Saiu para entrega
- Entregue
- Ocorrência

---

## 📈 Dashboard e Métricas

### KPIs Principais

- **Total de Mensagens**: Enviadas vs Recebidas
- **Taxa de Automação**: % de mensagens do bot
- **Conversas Ativas**: Conversas em andamento
- **Conversas Não Lidas**: Aguardando resposta
- **Tempo Médio de Resposta**: Performance do atendimento

### Gráficos

- **Mensagens por Dia**: Barras comparando enviadas/recebidas
- **Top Intenções**: Ranking das dúvidas mais comuns
- **Conversas Recentes**: Lista das últimas interações

---

## 🔧 Troubleshooting

### WhatsApp não conecta

1. Verifique se Evolution API está rodando
2. Confirme o `EVOLUTION_API_KEY` no `.env`
3. Verifique se a porta 8080 está acessível
4. Tente gerar novo QR Code

### Mensagens não são recebidas

1. Configure o webhook na Evolution API:
   ```
   POST para https://seu-dominio.com/api/v1/whatsapp/webhook/enhanced
   ```
2. Verifique logs do backend
3. Confirme que a instância está conectada

### Bot não responde

1. Verifique se chatbot está habilitado nas configurações
2. Confirme horário comercial (se habilitado)
3. Teste a intenção com palavras-chave exatas
4. Verifique logs para ver a confiança detectada

### Histórico não sincroniza

1. Confirme que há `cliente_id` vinculado
2. Verifique credenciais do CRM Enterprise
3. Teste endpoint do CRM manualmente
4. Veja logs de sincronização

---

## 🔐 Segurança

- ✅ Multi-tenancy: Cada tenant tem suas próprias conversas
- ✅ Autenticação: Todos os endpoints requerem token
- ✅ Criptografia: Comunicação segura com Evolution API
- ✅ Privacidade: Mensagens não são compartilhadas entre tenants
- ✅ Auditoria: Timestamps e tracking completos

---

## 📚 Integrações

### Evolution API
- Envio de mensagens
- Recebimento via webhook
- Status de entrega
- Download de mídias

### CRM Enterprise
- Criação de leads
- Criação de casos
- Timeline de interações
- Vinculação de registros

### Módulos LogiFlow
- **Pedidos**: Notificações automáticas de status
- **Motoristas**: Atribuição de entregas
- **Clientes**: Histórico unificado
- **Fiscal**: Envio de CT-e/MDF-e

---

## 🎯 Roadmap Futuro

Próximas implementações planejadas:

- ❌ Envio em massa com intervalo
- ❌ Templates de mensagem salvos
- ❌ Respostas rápidas configuráveis
- ❌ Transferência de conversas entre atendentes
- ❌ Tags e categorias customizadas
- ❌ Relatórios avançados (Excel/PDF)
- ❌ Integração com outras plataformas (Telegram, etc)
- ❌ Chatbot com IA (GPT-4, Claude)
- ❌ Áudio e vídeo chamadas

---

## 💡 Dicas de Uso

### Para Melhor Performance

1. **Horário Comercial**: Configure para evitar mensagens fora do expediente
2. **Respostas Rápidas**: Use o bot para perguntas frequentes
3. **Vinculação**: Sempre vincule conversas a clientes
4. **Tags**: Use tags para organizar conversas
5. **Arquivamento**: Arquive conversas antigas regularmente

### Para Melhor Experiência do Cliente

1. Use emojis nos templates de notificação
2. Mantenha mensagens curtas e objetivas
3. Inclua links para rastreamento
4. Responda rapidamente mensagens não lidas
5. Personalize a mensagem de boas-vindas

---

## 📝 Notas Importantes

1. **Limite de Mensagens**: Respeite limites do WhatsApp Business
2. **Spam**: Não envie mensagens não solicitadas
3. **LGPD**: Mantenha conformidade com dados pessoais
4. **Backup**: Exporte histórico periodicamente
5. **Testes**: Sempre teste em homologação primeiro

---

## 🤝 Suporte

Para dúvidas ou problemas:
1. Consulte esta documentação
2. Veja logs do sistema (`backend/logs`)
3. Teste webhook no Postman/Insomnia
4. Entre em contato com suporte técnico

---

**Versão**: 1.0.0  
**Data**: Janeiro 2026  
**Desenvolvido por**: LogiFlow CRM Team

**Evolution API**: https://doc.evolution-api.com/  
**WhatsApp Business**: https://business.whatsapp.com/
