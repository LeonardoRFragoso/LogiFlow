# 📘 Manual Completo do Usuário - LogiFlow CRM

**Versão**: 1.0 | **Data**: Dezembro 2024

---

## 📑 Índice

1. [Introdução](#1-introdução)
2. [Primeiros Passos](#2-primeiros-passos)
3. [Módulo Comercial](#3-módulo-comercial)
4. [Módulo Operacional](#4-módulo-operacional)
5. [Módulo Fiscal](#5-módulo-fiscal)
6. [Gestão de Frota](#6-gestão-de-frota)
7. [Relatórios e Dashboards](#7-relatórios-e-dashboards)
8. [Integrações](#8-integrações)
9. [Configurações](#9-configurações)
10. [App do Motorista](#10-app-do-motorista)
11. [Portal do Cliente](#11-portal-do-cliente)
12. [Solução de Problemas](#12-solução-de-problemas)

---

## 1. Introdução

### 1.1 O que é o LogiFlow CRM?

O LogiFlow CRM é uma plataforma completa de gestão para transportadoras que integra:

- **CRM Comercial**: Gestão de clientes, cotações e oportunidades
- **TMS Operacional**: Controle de pedidos, entregas e rastreamento
- **Emissão Fiscal**: CT-e e MDF-e integrados
- **Gestão de Frota**: Veículos, motoristas e manutenções
- **Portal do Cliente**: Rastreamento em tempo real
- **App do Motorista**: Atualização de status mobile

### 1.2 Requisitos do Sistema

**Navegadores Suportados**:
- Google Chrome 90+ (recomendado)
- Mozilla Firefox 88+
- Microsoft Edge 90+
- Safari 14+

**Conexão de Internet**:
- Mínimo: 2 Mbps
- Recomendado: 10 Mbps

**Resolução de Tela**:
- Mínimo: 1366x768
- Recomendado: 1920x1080

### 1.3 Estrutura do Sistema

```
LogiFlow CRM
├── Dashboard (Visão Geral)
├── Comercial
│   ├── Clientes
│   ├── Cotações
│   └── Oportunidades
├── Operacional
│   ├── Pedidos
│   ├── Entregas
│   └── Ocorrências
├── Fiscal
│   ├── CT-e
│   ├── MDF-e
│   └── Relatórios Fiscais
├── Frota
│   ├── Veículos
│   ├── Motoristas
│   └── Manutenções
└── Configurações
    ├── Usuários
    ├── Permissões
    └── Integrações
```

---

## 2. Primeiros Passos

### 2.1 Primeiro Acesso

1. **Receba suas credenciais** por e-mail
2. **Acesse** a URL fornecida (ex: `https://suaempresa.logiflow.com.br`)
3. **Digite** seu e-mail e senha temporária
4. **Crie** uma nova senha segura
5. **Complete** seu perfil

### 2.2 Navegação Básica

**Menu Lateral**:
- Clique nos ícones para acessar módulos
- Use o campo de busca para encontrar rapidamente
- Favoritos: Clique na estrela para marcar páginas frequentes

**Barra Superior**:
- 🔔 **Notificações**: Alertas e avisos importantes
- 👤 **Perfil**: Suas informações e configurações
- ❓ **Ajuda**: Acesso rápido à documentação
- 🌙 **Tema**: Alterne entre claro/escuro

**Atalhos de Teclado**:
- `Ctrl + K`: Busca rápida
- `Ctrl + N`: Novo registro (contexto atual)
- `Ctrl + S`: Salvar
- `Esc`: Fechar modal

### 2.3 Dashboard Principal

O dashboard mostra em tempo real:

**Métricas Principais**:
- 📦 Entregas do Dia
- 🚚 Em Trânsito
- ⚠️ Atrasadas
- ✅ Concluídas no Mês
- 💰 Faturamento

**Gráficos**:
- Evolução de entregas (últimos 30 dias)
- Performance por motorista
- Principais clientes
- Tipos de ocorrências

**Ações Rápidas**:
- Nova Cotação
- Novo Pedido
- Registrar Ocorrência
- Emitir CT-e

---

## 3. Módulo Comercial

### 3.1 Gestão de Clientes

#### 3.1.1 Cadastrar Cliente

1. **Menu** → **Comercial** → **Clientes** → **Novo Cliente**

2. **Aba Dados Principais**:
   - Nome/Razão Social *
   - Nome Fantasia
   - CNPJ/CPF *
   - Inscrição Estadual
   - Email *
   - Telefone *
   - Site

3. **Aba Endereço**:
   - CEP (busca automática)
   - Logradouro
   - Número
   - Complemento
   - Bairro
   - Cidade/UF

4. **Aba Comercial**:
   - Condição de Pagamento
   - Limite de Crédito
   - Desconto Padrão
   - Tabela de Preços
   - Vendedor Responsável

5. **Aba Contatos**:
   - Adicione múltiplos contatos
   - Nome, cargo, telefone, email
   - Marque contato principal

6. **Clique em Salvar**

**Dica**: Use o botão "Buscar CNPJ" para preencher dados automaticamente da Receita Federal.

#### 3.1.2 Importar Clientes em Massa

1. **Baixe** o template: `templates/template_clientes.csv`
2. **Preencha** com seus dados
3. **Valide**: 
   ```bash
   python scripts/validar_importacao.py --arquivo clientes.csv --tipo clientes
   ```
4. **Importe**:
   ```bash
   python scripts/importar_dados.py --arquivo clientes.csv --tipo clientes
   ```

#### 3.1.3 Segmentação de Clientes

Crie segmentos para melhor gestão:

1. **Menu** → **Comercial** → **Segmentos**
2. **Novo Segmento**
3. Defina critérios:
   - Faturamento mensal
   - Frequência de pedidos
   - Região
   - Tipo de carga

**Segmentos Sugeridos**:
- 🌟 VIP (> R$ 50k/mês)
- 💼 Corporativo (R$ 10k-50k/mês)
- 🏢 PME (R$ 2k-10k/mês)
- 🆕 Novos Clientes (< 3 meses)

### 3.2 Cotações

#### 3.2.1 Criar Cotação

1. **Menu** → **Comercial** → **Nova Cotação**

2. **Selecione o Cliente**
   - Busque por nome ou CNPJ
   - Ou crie um novo cliente

3. **Dados da Carga**:
   - Tipo de Carga (Geral, Perecível, Perigosa, etc)
   - Peso (kg) *
   - Volumes *
   - Valor da Mercadoria
   - Observações

4. **Origem e Destino**:
   - CEP ou Cidade/UF
   - Sistema calcula distância automaticamente
   - Visualize rota no mapa

5. **Cálculo do Frete**:
   - Sistema sugere valor baseado em:
     - Distância
     - Peso e volume
     - Tabela de preços
     - Pedágios
   - Ajuste manualmente se necessário

6. **Prazo de Entrega**:
   - Defina data/hora de coleta
   - Defina data/hora de entrega
   - Sistema calcula prazo automaticamente

7. **Enviar Cotação**:
   - Por email (automático)
   - Por WhatsApp (link)
   - Imprimir PDF

#### 3.2.2 Acompanhar Cotações

**Status Possíveis**:
- 📝 Rascunho
- 📤 Enviada
- 👀 Visualizada
- ✅ Aprovada
- ❌ Recusada
- ⏰ Expirada

**Ações**:
- Editar cotação
- Reenviar
- Converter em pedido
- Duplicar
- Cancelar

#### 3.2.3 Converter Cotação em Pedido

1. **Abra a cotação aprovada**
2. **Clique em "Converter em Pedido"**
3. **Confirme os dados**:
   - Cliente
   - Valores
   - Prazos
4. **Pedido criado automaticamente**
5. **Programe a coleta**

### 3.3 Pipeline de Vendas

Visualize suas oportunidades em funil:

1. **Menu** → **Comercial** → **Pipeline**

**Etapas**:
1. 🎯 Prospecção
2. 📞 Contato Inicial
3. 💬 Negociação
4. 📄 Proposta Enviada
5. ✅ Fechado-Ganho
6. ❌ Fechado-Perdido

**Arraste e solte** oportunidades entre etapas.

---

## 4. Módulo Operacional

### 4.1 Gestão de Pedidos

#### 4.1.1 Criar Pedido Manual

1. **Menu** → **Operacional** → **Novo Pedido**

2. **Dados Básicos**:
   - Cliente *
   - Número do Pedido (auto)
   - Data de Criação
   - Vendedor

3. **Coleta**:
   - Endereço de coleta
   - Data/hora programada
   - Contato no local
   - Observações

4. **Entrega**:
   - Endereço de entrega
   - Data/hora programada
   - Contato no local
   - Observações

5. **Carga**:
   - Descrição
   - Peso e volumes
   - Valor da mercadoria
   - Tipo de embalagem

6. **Valores**:
   - Valor do frete
   - Pedágio
   - Seguro
   - Outros custos
   - **Total**

7. **Atribuir Recursos**:
   - Motorista
   - Veículo
   - Ajudantes (se necessário)

8. **Salvar**

#### 4.1.2 Programar Coleta

1. **Abra o pedido**
2. **Aba "Coleta"**
3. **Clique em "Programar"**
4. **Selecione**:
   - Data e hora
   - Motorista
   - Veículo
5. **Motorista recebe notificação** no app

#### 4.1.3 Acompanhar Status

**Fluxo de Status**:
```
Novo → Programado → Coletado → Em Trânsito → Entregue → Finalizado
```

**Ações por Status**:
- **Novo**: Programar coleta, Cancelar
- **Programado**: Editar programação, Cancelar
- **Coletado**: Emitir CT-e, Registrar ocorrência
- **Em Trânsito**: Rastrear, Registrar ocorrência
- **Entregue**: Confirmar entrega, Ver comprovante
- **Finalizado**: Faturar, Gerar relatório

### 4.2 Rastreamento

#### 4.2.1 Rastrear Entrega

1. **Menu** → **Operacional** → **Entregas**
2. **Clique na entrega**
3. **Visualize**:
   - 🗺️ Localização atual no mapa
   - 📍 Histórico de posições
   - ⏱️ Tempo estimado de chegada
   - 📊 Progresso da rota

#### 4.2.2 Compartilhar Rastreamento

1. **Abra a entrega**
2. **Clique em "Compartilhar"**
3. **Escolha**:
   - Copiar link
   - Enviar por email
   - Enviar por WhatsApp
4. **Cliente acessa sem login**

### 4.3 Ocorrências

#### 4.3.1 Registrar Ocorrência

1. **Abra a entrega**
2. **Clique em "Nova Ocorrência"**
3. **Selecione o tipo**:
   - ⏰ Atraso
   - 📦 Avaria
   - ❌ Recusa
   - 🚫 Endereço não encontrado
   - 🔧 Problema mecânico
   - 🚨 Acidente
   - 📝 Outros

4. **Descreva o problema**
5. **Anexe fotos** (opcional)
6. **Defina ação**:
   - Reagendar entrega
   - Retornar mercadoria
   - Aguardar instruções

7. **Salvar**

**Sistema notifica automaticamente**:
- Cliente (email + WhatsApp)
- Gestor responsável
- Vendedor

#### 4.3.2 Acompanhar Ocorrências

**Dashboard de Ocorrências**:
- Total de ocorrências no mês
- Por tipo
- Por motorista
- Por cliente
- Tempo médio de resolução

---

## 5. Módulo Fiscal

### 5.1 Configuração Inicial

#### 5.1.1 Certificado Digital

1. **Menu** → **Configurações** → **Fiscal**
2. **Upload do Certificado**:
   - Tipo A1: Arquivo .pfx
   - Tipo A3: Configurar token/cartão
3. **Digite a senha**
4. **Teste a conexão**

#### 5.1.2 Dados da Empresa

Configure:
- CNPJ
- Inscrição Estadual
- Regime Tributário
- Endereço fiscal
- Responsável técnico

### 5.2 Emissão de CT-e

#### 5.2.1 Emitir CT-e

1. **Abra o pedido**
2. **Clique em "Emitir CT-e"**

3. **Confira os dados**:
   - **Remetente**: Quem envia a mercadoria
   - **Destinatário**: Quem recebe
   - **Tomador**: Quem paga o frete
   - **Expedidor**: (se houver)
   - **Recebedor**: (se houver)

4. **Dados da Carga**:
   - Natureza da operação
   - Tipo de serviço
   - Produto predominante
   - Peso e volumes

5. **Valores**:
   - Valor da mercadoria
   - Valor do frete
   - Pedágio
   - Seguro
   - Outros

6. **Impostos** (calculados automaticamente):
   - ICMS
   - PIS
   - COFINS

7. **Clique em "Transmitir"**

8. **Aguarde autorização** (1-2 minutos)

9. **CT-e Autorizado!**
   - Baixe XML
   - Baixe DACTE (PDF)
   - Envie por email

#### 5.2.2 Consultar CT-e

1. **Menu** → **Fiscal** → **CT-e Emitidos**
2. **Filtros**:
   - Período
   - Cliente
   - Status
   - Número

3. **Ações**:
   - Ver detalhes
   - Baixar XML/PDF
   - Reenviar email
   - Cancelar
   - Carta de correção

#### 5.2.3 Cancelar CT-e

**Requisitos**:
- Até 24h após emissão
- Antes da entrega
- Motivo com mínimo 15 caracteres

**Procedimento**:
1. Abra o CT-e
2. Clique em "Cancelar"
3. Informe o motivo
4. Confirme
5. Aguarde processamento

### 5.3 Emissão de MDF-e

#### 5.3.1 Quando Emitir MDF-e

**Obrigatório para**:
- Transporte interestadual
- Mais de 1 CT-e no mesmo veículo
- Transporte de carga própria

#### 5.3.2 Emitir MDF-e

1. **Menu** → **Fiscal** → **MDF-e** → **Novo**

2. **Dados do Veículo**:
   - Placa
   - UF
   - RNTRC

3. **Motorista**:
   - CPF
   - Nome

4. **Percurso**:
   - UF de início
   - UFs de percurso
   - UF de fim

5. **Documentos Fiscais**:
   - Adicione os CT-e
   - Ou NF-e (carga própria)

6. **Transmitir**

7. **MDF-e Autorizado!**
   - Imprima o DAMDFE
   - Mantenha no veículo

#### 5.3.3 Encerrar MDF-e

Ao finalizar o transporte:
1. Abra o MDF-e
2. Clique em "Encerrar"
3. Informe UF de encerramento
4. Confirme

---

## 6. Gestão de Frota

### 6.1 Veículos

#### 6.1.1 Cadastrar Veículo

1. **Menu** → **Frota** → **Veículos** → **Novo**

2. **Dados Básicos**:
   - Placa *
   - Tipo * (Caminhão, Van, Carreta, etc)
   - Marca *
   - Modelo *
   - Ano Fabricação
   - Ano Modelo

3. **Documentação**:
   - Renavam
   - Chassi
   - RNTRC
   - Validade RNTRC

4. **Especificações**:
   - Capacidade (kg)
   - Capacidade (m³)
   - Tipo de carroceria
   - Tipo de propriedade

5. **Rastreamento**:
   - Possui rastreador?
   - Provedor (Sascar, Autotrac, etc)
   - ID do dispositivo

6. **Salvar**

#### 6.1.2 Manutenções

**Programar Manutenção**:
1. Abra o veículo
2. Aba "Manutenções"
3. Clique em "Nova Manutenção"
4. Preencha:
   - Tipo (Preventiva/Corretiva)
   - Data programada
   - Km atual
   - Serviços a realizar
   - Oficina
5. Salvar

**Registrar Manutenção Realizada**:
1. Abra a manutenção
2. Clique em "Finalizar"
3. Informe:
   - Data realização
   - Km final
   - Serviços realizados
   - Valor
   - Próxima manutenção
4. Anexe nota fiscal
5. Salvar

**Alertas Automáticos**:
- 🔔 Manutenção vencida
- ⚠️ Próxima manutenção (7 dias)
- 📄 Documento vencendo

### 6.2 Motoristas

#### 6.2.1 Cadastrar Motorista

1. **Menu** → **Frota** → **Motoristas** → **Novo**

2. **Dados Pessoais**:
   - Nome Completo *
   - CPF *
   - RG
   - Data de Nascimento
   - Telefone *
   - Email

3. **Endereço**:
   - CEP
   - Logradouro
   - Número
   - Cidade/UF

4. **CNH**:
   - Número *
   - Categoria *
   - Data de Emissão
   - Data de Validade *
   - Primeira Habilitação

5. **Dados Profissionais**:
   - Data de Admissão
   - Tipo de Contrato
   - Salário
   - Veículo Padrão

6. **Acesso ao Sistema**:
   - Criar usuário?
   - Login (CPF)
   - Senha temporária

7. **Salvar**

#### 6.2.2 Performance do Motorista

**Métricas Acompanhadas**:
- 📦 Entregas realizadas
- ⏱️ Tempo médio de entrega
- ⚠️ Ocorrências
- ⭐ Avaliação dos clientes
- 🚗 Km rodados
- ⛽ Consumo médio

**Relatório Mensal**:
1. Menu → Frota → Motoristas
2. Selecione o motorista
3. Aba "Performance"
4. Escolha o período
5. Visualize gráficos e métricas

---

## 7. Relatórios e Dashboards

### 7.1 Relatórios Disponíveis

#### 7.1.1 Relatórios Operacionais

**Entregas**:
- Entregas por período
- Entregas por cliente
- Entregas por motorista
- Entregas por região
- Taxa de sucesso

**Ocorrências**:
- Ocorrências por tipo
- Ocorrências por motorista
- Tempo médio de resolução
- Custo de ocorrências

**Performance**:
- SLA de entregas
- Tempo médio de entrega
- Km rodados
- Utilização da frota

#### 7.1.2 Relatórios Comerciais

**Vendas**:
- Faturamento por período
- Faturamento por cliente
- Faturamento por vendedor
- Ticket médio

**Cotações**:
- Taxa de conversão
- Tempo médio de resposta
- Motivos de recusa
- Valor médio de cotação

#### 7.1.3 Relatórios Fiscais

**CT-e**:
- CT-e emitidos por período
- Valor total de serviços
- Impostos por tipo
- CT-e cancelados

**MDF-e**:
- MDF-e emitidos
- Percursos mais frequentes
- Tempo médio de viagem

### 7.2 Criar Relatório Personalizado

1. **Menu** → **Relatórios** → **Novo Relatório**
2. **Selecione a fonte de dados**
3. **Escolha os campos**
4. **Defina filtros**
5. **Configure agrupamentos**
6. **Escolha visualização** (tabela/gráfico)
7. **Salvar e nomear**

### 7.3 Agendar Relatórios

**Envio Automático por Email**:
1. Abra o relatório
2. Clique em "Agendar"
3. Defina:
   - Frequência (Diária/Semanal/Mensal)
   - Dia e hora
   - Destinatários
4. Salvar

---

## 8. Integrações

### 8.1 WhatsApp (Evolution API)

#### 8.1.1 Configurar

1. **Menu** → **Integrações** → **WhatsApp**
2. **Conectar Conta**:
   - Escaneie QR Code
   - Aguarde confirmação
3. **Configurar Mensagens**:
   - Template de cotação
   - Template de confirmação
   - Template de rastreamento
   - Template de entrega

#### 8.1.2 Usar

**Envio Automático**:
- Cotação enviada → WhatsApp
- Pedido confirmado → WhatsApp
- Coleta programada → WhatsApp
- Entrega realizada → WhatsApp

**Envio Manual**:
1. Abra o registro (cotação/pedido)
2. Clique em "Enviar WhatsApp"
3. Confirme

### 8.2 Google Maps

**Funcionalidades**:
- Cálculo de distância
- Cálculo de rota
- Tempo estimado
- Visualização de mapa
- Geocoding (CEP → Coordenadas)

**Configuração**:
1. Menu → Integrações → Google Maps
2. Insira API Key
3. Teste conexão

### 8.3 ERPs (Omie, Bling, Tiny)

**Sincronização**:
- Clientes
- Produtos/Serviços
- Pedidos
- Notas Fiscais
- Pagamentos

**Configurar**:
1. Menu → Integrações → ERP
2. Selecione o ERP
3. Insira credenciais (App Key/Secret)
4. Configure mapeamento de campos
5. Teste sincronização
6. Ative sincronização automática

---

## 9. Configurações

### 9.1 Usuários e Permissões

#### 9.1.1 Criar Usuário

1. **Menu** → **Configurações** → **Usuários** → **Novo**
2. **Dados**:
   - Nome
   - Email
   - Telefone
   - Cargo
3. **Perfil de Acesso**:
   - Administrador
   - Gerente
   - Comercial
   - Operacional
   - Motorista
4. **Permissões Específicas** (opcional)
5. **Enviar convite**

#### 9.1.2 Perfis de Acesso

| Perfil | Permissões |
|--------|------------|
| **Administrador** | Acesso total |
| **Gerente** | Visualiza tudo, edita operação |
| **Comercial** | Clientes, cotações, pedidos |
| **Operacional** | Pedidos, entregas, ocorrências |
| **Financeiro** | Relatórios, faturamento |
| **Motorista** | Apenas app do motorista |

### 9.2 Empresa

**Configurar**:
1. Menu → Configurações → Empresa
2. **Dados Cadastrais**:
   - Razão Social
   - CNPJ
   - Inscrição Estadual
   - Endereço
3. **Dados Fiscais**:
   - Regime Tributário
   - Certificado Digital
   - Série CT-e/MDF-e
4. **Contatos**:
   - Telefone
   - Email
   - Site
5. **Logo**:
   - Upload da logo (PNG/JPG)
   - Aparece em relatórios e documentos

### 9.3 Tabelas de Preços

**Criar Tabela**:
1. Menu → Configurações → Tabelas de Preços
2. Novo
3. Nome da tabela
4. Tipo:
   - Por distância (R$/km)
   - Por peso (R$/kg)
   - Por rota fixa
5. Configure valores
6. Associe a clientes

---

## 10. App do Motorista

### 10.1 Acesso

**URL**: `app.logiflow.com.br`

**Login**:
- Usuário: CPF
- Senha: Fornecida pelo gestor

### 10.2 Funcionalidades

**Minhas Cargas**:
- Ver entregas do dia
- Detalhes de cada entrega
- Endereços e contatos
- Observações

**Atualizar Status**:
- Saí para coleta
- Coletado
- Em trânsito
- Chegou no destino
- Entregue

**Registrar Ocorrência**:
- Selecionar tipo
- Descrever problema
- Tirar foto
- Enviar

**Comprovante de Entrega**:
- Tirar foto do comprovante
- Coletar assinatura digital
- Enviar

**Offline**:
- App funciona sem internet
- Sincroniza quando conectar

---

## 11. Portal do Cliente

### 11.1 Acesso

Cada cliente recebe:
- URL personalizada
- Login e senha

### 11.2 Funcionalidades

**Rastrear Entregas**:
- Ver entregas em andamento
- Localização em tempo real
- Histórico de status
- Previsão de chegada

**Histórico**:
- Todas as entregas realizadas
- Filtrar por período
- Baixar comprovantes

**Solicitar Cotação**:
- Formulário online
- Resposta automática
- Acompanhar status

**Documentos**:
- Baixar CT-e (XML/PDF)
- Baixar comprovantes
- Notas fiscais

---

## 12. Solução de Problemas

### 12.1 Problemas Comuns

**Não consigo fazer login**:
- Verifique email e senha
- Use "Esqueci minha senha"
- Limpe cache do navegador
- Tente outro navegador

**Sistema está lento**:
- Verifique sua internet
- Feche abas desnecessárias
- Limpe cache (Ctrl+Shift+Del)
- Atualize o navegador

**Erro ao emitir CT-e**:
- Verifique certificado digital
- Confira dados obrigatórios
- Teste conexão com SEFAZ
- Veja log de erros

**App do motorista não sincroniza**:
- Verifique conexão de internet
- Force sincronização manual
- Atualize o app (F5)
- Limpe dados do app

### 12.2 Logs e Diagnóstico

**Acessar Logs**:
1. Menu → Configurações → Logs
2. Filtre por:
   - Data
   - Tipo (Erro/Aviso/Info)
   - Módulo
3. Visualize detalhes
4. Exporte se necessário

### 12.3 Suporte

**Canais de Atendimento**:
- 📧 Email: suporte@logiflow.com.br
- 💬 WhatsApp: (11) 99999-9999
- 📞 Telefone: (11) 3333-3333
- 🌐 Chat: Disponível no sistema

**Horário**:
- Segunda a Sexta: 8h às 18h
- Sábado: 8h às 12h
- Emergências: 24/7 (clientes Enterprise)

**SLA de Atendimento**:
- Crítico: 1 hora
- Alto: 4 horas
- Médio: 8 horas
- Baixo: 24 horas

---

## 📚 Recursos Adicionais

**Documentação Online**: docs.logiflow.com.br
**Vídeos Tutoriais**: youtube.com/logiflowcrm
**Blog**: blog.logiflow.com.br
**Comunidade**: community.logiflow.com.br

---

**© 2024 LogiFlow CRM - Todos os direitos reservados**

*Este manual é atualizado regularmente. Versão atual: 1.0 (Dezembro 2024)*
