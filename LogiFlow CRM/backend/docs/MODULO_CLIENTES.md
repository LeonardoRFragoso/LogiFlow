# Módulo Clientes - LogiFlow CRM

## Visão Geral

O módulo de Clientes é o coração do LogiFlow CRM, permitindo o cadastro e gestão completa de todos os clientes da transportadora.

---

## Funcionalidades

### ✅ Cadastro de Clientes
- Pessoa Física (CPF) ou Jurídica (CNPJ)
- Dados cadastrais completos
- Múltiplos endereços
- Múltiplos contatos
- Histórico de interações

### ✅ Gestão de Relacionamento
- Histórico de cotações
- Histórico de pedidos
- Histórico de entregas
- Notas e observações
- Anexos de documentos

### ✅ Segmentação
- Por tipo (PF/PJ)
- Por região
- Por volume de negócios
- Por status (ativo/inativo)

---

## Como Usar

### 1. Cadastrar Novo Cliente

**Caminho:** Menu > Clientes > Novo Cliente

**Dados Obrigatórios:**
- Nome/Razão Social
- CPF ou CNPJ
- Telefone ou Email

**Dados Opcionais:**
- Nome Fantasia
- Inscrição Estadual
- Endereço completo
- Contato principal
- Observações

**Exemplo:**
```
Nome: Transportadora ABC Ltda
CNPJ: 12.345.678/0001-90
IE: 123.456.789
Telefone: (11) 3333-4444
Email: contato@abc.com.br
Endereço: Rua das Flores, 100
Bairro: Centro
Cidade: São Paulo - SP
CEP: 01310-100
```

---

### 2. Buscar Cliente

**Opções de Busca:**
- Por nome
- Por CNPJ/CPF
- Por cidade
- Por status

**Filtros Avançados:**
- Data de cadastro
- Última compra
- Valor total de negócios
- Região

---

### 3. Editar Cliente

**Caminho:** Clientes > Selecionar Cliente > Editar

**Campos Editáveis:**
- Todos os dados cadastrais
- Status (ativo/inativo)
- Observações
- Contatos

**Atenção:** Alterações em CNPJ/CPF devem ser feitas com cuidado, pois podem afetar integrações com ERPs.

---

### 4. Visualizar Histórico

**Abas Disponíveis:**

#### 📊 Resumo
- Dados cadastrais
- Status
- Última interação
- Total de negócios

#### 💰 Cotações
- Lista de todas as cotações
- Status de cada cotação
- Valores totais
- Filtros por período

#### 📦 Pedidos
- Lista de todos os pedidos
- Status de entrega
- Valores faturados
- Filtros por período

#### 🚚 Entregas
- Histórico de entregas
- Status de cada entrega
- Ocorrências registradas
- Avaliações

#### 📝 Notas
- Observações internas
- Histórico de comunicações
- Anexos de documentos

---

## Campos do Cadastro

### Dados Básicos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Nome | Texto | ✅ Sim | Razão Social ou Nome Completo |
| Nome Fantasia | Texto | Não | Nome comercial |
| Tipo Pessoa | Seleção | ✅ Sim | Física ou Jurídica |
| CPF | Número | Sim* | 11 dígitos (se PF) |
| CNPJ | Número | Sim* | 14 dígitos (se PJ) |
| IE | Texto | Não | Inscrição Estadual |
| Status | Seleção | ✅ Sim | Ativo/Inativo |

*CPF ou CNPJ obrigatório

### Contato

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Telefone | Texto | Não | Telefone fixo |
| Celular | Texto | Não | Celular/WhatsApp |
| Email | Email | Não | Email principal |
| Contato Principal | Texto | Não | Nome do responsável |

### Endereço

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| CEP | Número | Não | 8 dígitos |
| Logradouro | Texto | Não | Rua, Avenida, etc |
| Número | Texto | Não | Número do imóvel |
| Complemento | Texto | Não | Apto, Sala, etc |
| Bairro | Texto | Não | Bairro |
| Cidade | Texto | Não | Cidade |
| UF | Seleção | Não | Estado (2 letras) |

### Comercial

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| Condição Pagamento | Seleção | Não | À vista, 30 dias, etc |
| Limite Crédito | Moeda | Não | Valor máximo de crédito |
| Desconto Padrão | Percentual | Não | Desconto aplicado |
| Vendedor Responsável | Seleção | Não | Usuário responsável |

---

## Integrações

### Sincronização com ERP

O módulo de Clientes pode sincronizar automaticamente com:

#### Omie ERP
- Sincronização bidirecional
- Atualização automática de dados
- Mapeamento de campos

#### Bling ERP
- Sincronização de contatos
- Atualização de pedidos
- Integração financeira

**Como Ativar:**
1. Configurar credenciais do ERP no `.env`
2. Acessar: Configurações > Integrações > ERP
3. Ativar sincronização automática
4. Definir frequência (tempo real, diária, manual)

---

## Relatórios

### Relatórios Disponíveis

#### 📊 Clientes por Região
- Distribuição geográfica
- Concentração por estado/cidade
- Gráfico de mapa

#### 💰 Top Clientes
- Maiores faturamentos
- Maior volume de pedidos
- Clientes mais frequentes

#### 📈 Crescimento
- Novos clientes por período
- Taxa de retenção
- Churn rate

#### 🎯 Segmentação
- Por tipo de carga
- Por modal de transporte
- Por frequência de uso

---

## Boas Práticas

### ✅ Fazer

1. **Manter dados atualizados**
   - Revisar cadastros periodicamente
   - Atualizar contatos
   - Verificar endereços

2. **Registrar interações**
   - Anotar conversas importantes
   - Anexar documentos relevantes
   - Registrar acordos comerciais

3. **Segmentar clientes**
   - Criar tags personalizadas
   - Agrupar por características
   - Facilitar campanhas direcionadas

4. **Monitorar histórico**
   - Acompanhar padrões de compra
   - Identificar oportunidades
   - Prevenir problemas

### ❌ Evitar

1. **Cadastros duplicados**
   - Sempre buscar antes de criar
   - Verificar CNPJ/CPF
   - Mesclar duplicatas quando encontrar

2. **Dados incompletos**
   - Preencher o máximo de informações
   - Validar dados críticos
   - Solicitar documentos necessários

3. **Falta de atualização**
   - Não deixar dados desatualizados
   - Revisar periodicamente
   - Confirmar informações em cada contato

---

## Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl + N` | Novo Cliente |
| `Ctrl + F` | Buscar Cliente |
| `Ctrl + S` | Salvar |
| `Ctrl + E` | Editar |
| `Esc` | Cancelar |

---

## Perguntas Frequentes

### Como importar clientes de planilha?
Use o sistema de migração de dados:
```bash
python scripts/importar_dados.py --tipo clientes --arquivo clientes.csv
```

### Como mesclar clientes duplicados?
1. Acesse o cliente principal
2. Clique em "Mesclar"
3. Selecione o cliente duplicado
4. Confirme a mesclagem

### Como inativar um cliente?
1. Acesse o cadastro do cliente
2. Altere o status para "Inativo"
3. Salve as alterações

### Como exportar lista de clientes?
1. Acesse: Clientes > Listar
2. Clique em "Exportar"
3. Escolha o formato (CSV, Excel, PDF)
4. Baixe o arquivo

---

## Suporte

Dúvidas sobre o módulo de Clientes:
- Email: suporte@logiflow.com.br
- WhatsApp: (11) 99999-9999
- Documentação: https://docs.logiflow.com.br/clientes

---

**Última atualização:** 14 de Dezembro de 2024  
**Versão:** 1.0.0
