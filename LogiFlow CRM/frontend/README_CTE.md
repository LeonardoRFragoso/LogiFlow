# 📄 Tela de Emissão CT-e - Frontend

## Visão Geral

A tela de emissão de CT-e foi implementada no frontend Vue.js, permitindo a emissão de Conhecimento de Transporte Eletrônico diretamente da interface do LogiFlow CRM.

---

## 📁 Arquivo Criado

**Localização:** `frontend/src/views/fiscal/EmitirCTeView.vue`

**Linhas de Código:** ~700 linhas

---

## 🎯 Funcionalidades

### ✅ Formulário Completo
- **Dados do Tomador** (quem paga o frete)
- **Dados do Remetente** (quem envia)
- **Dados do Destinatário** (quem recebe)
- **Valores e Carga** (valor do serviço, peso, etc)
- **Dados do Veículo** (placa, RENAVAM, tipo)
- **Dados Fiscais** (natureza da operação, ICMS, etc)

### ✅ Validações
- Campos obrigatórios marcados com *
- Validação em tempo real
- Botão de emissão desabilitado se formulário inválido
- Mensagens de erro claras

### ✅ Integração com Backend
- Carrega dados do pedido automaticamente
- Preenche campos com informações do pedido
- Envia dados para API `/fiscal/cte/emitir`
- Recebe resposta com chave, número e protocolo

### ✅ Modal de Sucesso
- Exibe informações do CT-e emitido
- Botão para download do PDF (DACTE)
- Botão para download do XML
- Redirecionamento automático após fechar

### ✅ UX/UI Moderna
- Design responsivo
- Loading states
- Estados de erro
- Feedback visual
- Ícones intuitivos

---

## 🚀 Como Usar

### 1. Acessar a Tela

**Opção 1: Via Lista de Pedidos**
```
1. Ir para Pedidos
2. Clicar em um pedido
3. Clicar em "Emitir CT-e"
```

**Opção 2: Via URL Direta**
```
/pedidos/{id}/emitir-cte
```

**Exemplo:**
```
http://localhost:5173/pedidos/123/emitir-cte
```

---

### 2. Preencher Formulário

#### Dados Pré-preenchidos (do pedido):
- ✅ Valor total do serviço
- ✅ Peso da carga
- ✅ Placa do veículo
- ✅ Endereços de origem e destino

#### Dados a Preencher:

**Tomador do Serviço:**
- Tipo (Remetente/Destinatário/Outros)
- CNPJ/CPF
- Razão Social
- Inscrição Estadual
- Endereço completo
- Contato

**Remetente:**
- CNPJ/CPF
- Razão Social
- Endereço completo

**Destinatário:**
- CNPJ/CPF
- Razão Social
- Endereço completo

**Veículo:**
- Placa
- UF
- RENAVAM (opcional)
- Tipo de veículo

**Fiscal:**
- Natureza da operação
- Série
- Modal (Rodoviário/Aéreo/etc)
- ICMS

---

### 3. Emitir CT-e

```
1. Preencher todos os campos obrigatórios
2. Revisar informações
3. Clicar em "📄 Emitir CT-e"
4. Aguardar processamento (15-30 segundos)
5. Modal de sucesso aparece
```

---

### 4. Download de Documentos

**Após Emissão:**
- ✅ Download PDF (DACTE)
- ✅ Download XML
- ✅ Informações salvas no pedido

---

## 🔧 Integração com Backend

### Endpoint Utilizado

**POST** `/fiscal/cte/emitir`

**Payload:**
```json
{
  "pedido_id": "123",
  "tomador": {
    "tipo": "3",
    "documento": "12.345.678/0001-90",
    "nome": "Empresa XYZ Ltda",
    "ie": "123.456.789.000",
    "endereco": "Rua ABC",
    "numero": "100",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "uf": "SP",
    "cep": "01310-100",
    "telefone": "(11) 3333-4444",
    "email": "contato@xyz.com.br"
  },
  "remetente": { ... },
  "destinatario": { ... },
  "valores": {
    "valor_total": 500.00,
    "valor_receber": 500.00,
    "valor_carga": 5000.00,
    "peso_kg": 500,
    "produto_predominante": "MERCADORIA"
  },
  "veiculo": {
    "placa": "ABC-1234",
    "uf": "SP",
    "renavam": "12345678901",
    "tipo": "02"
  },
  "natureza_operacao": "PRESTACAO DE SERVICO DE TRANSPORTE",
  "serie": "1",
  "modal": "01",
  "icms_situacao": "00",
  "icms_aliquota": "12.00",
  "icms_valor": "60.00"
}
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "numero": "000123",
  "chave": "35240512345678000190570010001230001234567890",
  "protocolo": "135240000123456",
  "data_emissao": "2024-12-14T15:30:00",
  "url_danfe": "https://api.focusnfe.com.br/...",
  "xml": "https://api.focusnfe.com.br/..."
}
```

---

## 📋 Campos do Formulário

### Obrigatórios (*)

**Tomador:**
- Tipo
- CNPJ/CPF
- Nome
- Endereço
- Número
- Bairro
- Cidade
- UF
- CEP

**Remetente:**
- CNPJ/CPF
- Nome
- Endereço
- Número
- Bairro
- Cidade
- UF
- CEP

**Destinatário:**
- CNPJ/CPF
- Nome
- Endereço
- Número
- Bairro
- Cidade
- UF
- CEP

**Valores:**
- Valor Total
- Valor a Receber
- Peso (kg)

**Veículo:**
- Placa
- UF

**Fiscal:**
- Natureza da Operação
- Série

### Opcionais

- Inscrição Estadual (todos)
- Complemento (endereços)
- Telefone e Email (tomador)
- RENAVAM (veículo)
- RNTRC, CIOT
- Valor da Carga
- Produto Predominante
- Dados de ICMS

---

## 🎨 Componentes Visuais

### Seções do Formulário
1. 📦 Informações do Pedido (readonly)
2. 👤 Tomador do Serviço
3. 📤 Remetente
4. 📥 Destinatário
5. 💰 Valores e Carga
6. 🚚 Veículo
7. 📋 Dados Fiscais

### Estados Visuais
- **Loading:** Spinner + mensagem
- **Erro:** Ícone de alerta + mensagem
- **Emitindo:** Botão com spinner
- **Sucesso:** Modal com informações do CT-e

---

## 🔄 Fluxo Completo

```
1. Usuário acessa /pedidos/:id/emitir-cte
   ↓
2. Sistema carrega dados do pedido
   ↓
3. Preenche campos automaticamente
   ↓
4. Usuário completa dados faltantes
   ↓
5. Usuário clica em "Emitir CT-e"
   ↓
6. Sistema valida formulário
   ↓
7. Envia para API Focus NFe
   ↓
8. Aguarda autorização SEFAZ (15-30s)
   ↓
9. Recebe chave e protocolo
   ↓
10. Exibe modal de sucesso
    ↓
11. Usuário baixa PDF/XML
    ↓
12. Retorna para lista de pedidos
```

---

## 🛠️ Tecnologias Utilizadas

- **Vue 3** (Composition API)
- **Vue Router** (navegação)
- **Axios** (requisições HTTP)
- **CSS3** (estilização)

---

## 📱 Responsividade

A tela é totalmente responsiva:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px)
- ✅ Tablet (768px)
- ✅ Mobile (375px)

---

## ⚠️ Validações Implementadas

### Frontend
- Campos obrigatórios
- Formato de CNPJ/CPF (visual)
- Formato de CEP (visual)
- Valores numéricos positivos
- Seleção de UF válida

### Backend (API)
- Validação completa de CNPJ/CPF
- Validação de CEP
- Validação de dados fiscais
- Comunicação com SEFAZ
- Tratamento de erros

---

## 🐛 Tratamento de Erros

### Erros Possíveis

**Pedido não encontrado:**
```
Erro ao carregar pedido
[Botão: Voltar]
```

**Campos obrigatórios vazios:**
```
Por favor, preencha todos os campos obrigatórios
```

**Erro na emissão:**
```
Erro ao emitir CT-e: [mensagem da API]
```

**Timeout SEFAZ:**
```
Timeout ao comunicar com SEFAZ. Tente novamente.
```

---

## 🚀 Próximas Melhorias

### Planejadas
- [ ] Busca de CEP automática (ViaCEP)
- [ ] Validação de CNPJ/CPF em tempo real
- [ ] Autocompletar dados de clientes cadastrados
- [ ] Salvar rascunho do formulário
- [ ] Histórico de CT-es emitidos
- [ ] Impressão direta do DACTE
- [ ] Cancelamento de CT-e
- [ ] Carta de correção

---

## 📞 Suporte

Dúvidas sobre a tela de emissão CT-e:
- Email: suporte@logiflow.com.br
- WhatsApp: (11) 99999-9999
- Documentação Backend: `backend/docs/INTEGRACOES_ERP.md`

---

**Desenvolvido por:** Leonardo Fragoso  
**Data:** 14 de Dezembro de 2024  
**Versão:** 1.0.0
