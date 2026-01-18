# Configuração Focus NFe - Emissão de CT-e e MDF-e

## 📄 Visão Geral

O LogiFlow CRM integra com a **Focus NFe** para emissão de documentos fiscais eletrônicos:
- 📦 **CT-e** (Conhecimento de Transporte Eletrônico)
- 🚛 **MDF-e** (Manifesto Eletrônico de Documentos Fiscais)
- 📋 **NF-e** (Nota Fiscal Eletrônica) - opcional

---

## 🚀 Configuração Passo a Passo

### ETAPA 1: Criar Conta na Focus NFe

#### 1.1 Cadastro

1. Acesse: https://focusnfe.com.br/
2. Clique em **"Criar conta gratuita"**
3. Preencha:
   - Nome da empresa
   - CNPJ
   - Email
   - Telefone
4. Confirme o email de ativação

#### 1.2 Plano

**Planos Disponíveis:**

| Plano | Custo | CT-e/MDF-e Inclusos | Adicional |
|-------|-------|---------------------|-----------|
| **Free** | Gratuito | 10/mês | R$ 0,30/doc |
| **Básico** | R$ 49/mês | 100/mês | R$ 0,25/doc |
| **Profissional** | R$ 99/mês | 500/mês | R$ 0,20/doc |
| **Empresarial** | R$ 199/mês | 2.000/mês | R$ 0,15/doc |

**Recomendação:** Comece com plano Free para testes.

---

### ETAPA 2: Configurar Certificado Digital

#### 2.1 Upload do Certificado

1. No painel Focus NFe, vá em **"Configurações" → "Certificados"**
2. Clique em **"Adicionar Certificado"**
3. Upload do arquivo **.pfx** ou **.p12**
4. Digite a senha do certificado
5. Salve

**⚠️ IMPORTANTE:** O certificado deve ser:
- e-CNPJ ou e-CPF válido
- Emitido por Autoridade Certificadora credenciada
- Não vencido

#### 2.2 Obter Certificado (se não tiver)

Opções de Autoridades Certificadoras:
- **Serasa Experian** - https://serasa.certificadodigital.com.br/
- **Certisign** - https://www.certisign.com.br/
- **Valid** - https://www.validcertificadora.com.br/
- **Soluti** - https://www.soluti.com.br/

**Custo:** R$ 150-300 por ano

---

### ETAPA 3: Obter Token de API

#### 3.1 Gerar Token

1. No painel Focus NFe, vá em **"API" → "Tokens"**
2. Clique em **"Gerar novo token"**
3. Dê um nome: `LogiFlow Production`
4. Copie o token gerado (começa com `homologacao_` ou `producao_`)

**Tipos de Token:**
- **Homologação:** `homologacao_XXXXXXXXXXXXXXXXX` (para testes)
- **Produção:** `producao_XXXXXXXXXXXXXXXXX` (após homologação)

---

### ETAPA 4: Configurar no LogiFlow

#### 4.1 Adicionar no `.env`

```bash
# backend/.env

# ========================================
# Focus NFe - HOMOLOGAÇÃO (Testes)
# ========================================
FOCUSNFE_TOKEN=homologacao_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FOCUSNFE_ENVIRONMENT=homologacao

# ========================================
# Focus NFe - PRODUÇÃO (Após Homologação)
# ========================================
# FOCUSNFE_TOKEN=producao_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# FOCUSNFE_ENVIRONMENT=producao
```

#### 4.2 Variáveis Disponíveis

```bash
# Token de API (obrigatório)
FOCUSNFE_TOKEN=homologacao_xxx

# Ambiente: homologacao ou producao
FOCUSNFE_ENVIRONMENT=homologacao

# Timeout da API em segundos (opcional)
FOCUSNFE_TIMEOUT=30

# Webhook para receber notificações (opcional)
FOCUSNFE_WEBHOOK_URL=https://api.logiflow.com.br/api/fiscal/webhooks/focusnfe
```

---

### ETAPA 5: Configurar Dados da Empresa

#### 5.1 Dados Obrigatórios

No LogiFlow, configure no perfil da empresa:

```json
{
  "razao_social": "TRANSPORTES EXEMPLO LTDA",
  "nome_fantasia": "Exemplo Transportes",
  "cnpj": "12.345.678/0001-90",
  "inscricao_estadual": "123.456.789.123",
  "regime_tributario": "1",  // 1=Simples, 2=S.Normal, 3=S.Normal-excesso
  "endereco": {
    "logradouro": "Rua Exemplo",
    "numero": "100",
    "complemento": "Sala 1",
    "bairro": "Centro",
    "municipio": "São Paulo",
    "uf": "SP",
    "cep": "01234-567"
  },
  "telefone": "(11) 3333-4444",
  "email": "contato@exemplo.com.br"
}
```

---

## ✅ Testar Integração

### Teste 1: Verificar Token

```bash
cd backend
python scripts/test_focusnfe.py
```

### Teste 2: Emitir CT-e de Teste

Criar script: `backend/scripts/test_cte.py`

```python
from integrations.fiscal.focusnfe import FocusNFeClient
import json

client = FocusNFeClient()

# Dados mínimos para CT-e
cte_data = {
    "natureza_operacao": "PRESTACAO DE SERVICO DE TRANSPORTE",
    "tipo_documento": "0",  # 0=Saída
    "municipio_envio": "São Paulo",
    "municipio_inicio": "São Paulo",
    "municipio_fim": "Rio de Janeiro",
    "modelo": "57",  # CT-e
    
    "valores": {
        "valor_total": 100.00,
        "valor_receber": 100.00
    },
    
    "impostos": {
        "icms": {
            "situacao_tributaria": "00",
            "aliquota": 12.00,
            "valor": 12.00
        }
    },
    
    # Dados do remetente (quem está enviando a carga)
    "remetente": {
        "cpf_cnpj": "12345678000190",
        "nome": "Cliente Exemplo LTDA",
        "inscricao_estadual": "ISENTO",
        "endereco": "Rua A",
        "numero": "10",
        "bairro": "Centro",
        "municipio": "São Paulo",
        "uf": "SP",
        "cep": "01000-000"
    },
    
    # Dados do destinatário (quem vai receber a carga)
    "destinatario": {
        "cpf_cnpj": "98765432000111",
        "nome": "Destinatário Exemplo LTDA",
        "inscricao_estadual": "123456789",
        "endereco": "Rua B",
        "numero": "20",
        "bairro": "Centro",
        "municipio": "Rio de Janeiro",
        "uf": "RJ",
        "cep": "20000-000"
    },
    
    # Produtos/Serviços
    "produtos": [
        {
            "nome": "TRANSPORTE DE MERCADORIAS",
            "codigo": "001",
            "quantidade": 1,
            "valor_unitario": 100.00,
            "valor_total": 100.00
        }
    ]
}

# Emitir CT-e
response = client.emit_cte(cte_data)

print("Resposta:", json.dumps(response, indent=2))
```

Execute:
```bash
python scripts/test_cte.py
```

---

## 🔍 Fluxo de Emissão de CT-e

```
1. Usuário cria pedido de frete no LogiFlow
   ↓
2. Sistema valida dados obrigatórios
   ↓
3. Backend chama Focus NFe API para emitir CT-e
   ↓
4. Focus NFe valida e envia para SEFAZ
   ↓
5. SEFAZ autoriza ou rejeita
   ↓
6. Focus NFe retorna resposta
   ↓
7. LogiFlow salva chave de acesso e XML
   ↓
8. Sistema gera DACTE (PDF) para impressão
   ↓
9. Cliente recebe CT-e por email automaticamente
```

---

## 📊 Campos Obrigatórios por Documento

### CT-e (Conhecimento de Transporte)

**Mínimos Obrigatórios:**
- Natureza da operação
- Tipo de serviço (Normal, Subcontratação, etc)
- Dados do emitente (sua empresa)
- Dados do remetente (quem envia)
- Dados do destinatário (quem recebe)
- Dados da carga (valor, peso, quantidade)
- Valores (total, frete, impostos)
- Impostos (ICMS)

### MDF-e (Manifesto)

**Mínimos Obrigatórios:**
- Tipo de emitente (Transportadora, etc)
- Dados do emitente
- Modal de transporte (Rodoviário, etc)
- Dados do veículo (placa, RNTRC)
- Dados do motorista (CPF, nome)
- CT-es vinculados
- Município de carregamento
- Município de descarregamento

---

## 🛠️ Troubleshooting

### Problema: "Token inválido"

**Causa:** Token incorreto ou expirado

**Solução:**
1. Verifique se copiou o token completo
2. Confirme se está usando ambiente correto (homologação vs produção)
3. Regenere o token no painel Focus NFe

---

### Problema: "Certificado não encontrado"

**Causa:** Certificado não configurado no Focus NFe

**Solução:**
1. Faça upload do certificado digital no painel
2. Verifique se o certificado não está vencido
3. Confirme que a senha está correta

---

### Problema: "Rejeição 539 - CNPJ não habilitado"

**Causa:** CNPJ não está autorizado para emitir CT-e

**Solução:**
1. Solicite credenciamento na SEFAZ do seu estado
2. Aguarde aprovação (pode levar 2-5 dias úteis)
3. Até lá, use ambiente de homologação

---

### Problema: "Erro 400 - Dados inválidos"

**Causa:** JSON malformado ou campos obrigatórios faltando

**Solução:**
1. Valide JSON enviado
2. Verifique logs do backend para detalhes
3. Consulte documentação Focus NFe para campos obrigatórios
4. Use ambiente de homologação para testar

---

### Problema: "Timeout na API"

**Causa:** SEFAZ lenta ou indisponível

**Solução:**
1. Aumente o timeout da API (variável `FOCUSNFE_TIMEOUT`)
2. Implemente retry automático
3. Verifique status da SEFAZ: http://www.nfe.fazenda.gov.br/

---

## 💰 Custos e Limites

### Custo por Documento (Plano Básico)

- **CT-e:** R$ 0,25/documento
- **MDF-e:** R$ 0,25/documento  
- **NF-e:** R$ 0,25/documento

### Limites de API

- **Rate limit:** 60 requisições/minuto
- **Timeout:** 30 segundos por request
- **Tamanho máximo:** 5MB por documento

### Exemplo de Cálculo

Para transportadora com 200 CT-es/mês:
- Plano Básico: R$ 49/mês (inclui 100)
- 100 adicionais × R$ 0,25 = R$ 25
- **Total:** R$ 74/mês

---

## 🔐 Segurança

### Boas Práticas

1. **Nunca commitar token**
   - Use `.env` (não versionado)
   - Use secrets manager em produção

2. **Proteger certificado digital**
   - Senha forte
   - Backup seguro
   - Renovar antes do vencimento

3. **Validar dados antes de enviar**
   - CPF/CNPJ válidos
   - CEPs existentes
   - Valores corretos

4. **Monitorar rejeições**
   - Log todas as tentativas
   - Alertar sobre taxas altas de rejeição
   - Corrigir dados sistematicamente

---

## 📝 Checklist de Implementação

### Homologação
- [ ] Criar conta Focus NFe
- [ ] Upload certificado digital (homologação)
- [ ] Obter token de homologação
- [ ] Configurar no `.env`
- [ ] Testar emissão de CT-e
- [ ] Validar XML gerado
- [ ] Testar cancelamento
- [ ] Testar carta de correção
- [ ] Documentar processo

### Produção
- [ ] Solicitar credenciamento na SEFAZ
- [ ] Aguardar aprovação
- [ ] Obter certificado de produção
- [ ] Gerar token de produção
- [ ] Configurar variáveis de produção
- [ ] Testar com valores reais
- [ ] Configurar webhook
- [ ] Treinar equipe
- [ ] Ir ao ar! 🚀

---

## 📚 Recursos

### Documentação Oficial
- **Focus NFe API:** https://focusnfe.com.br/doc/
- **Manual CT-e:** https://focusnfe.com.br/doc/#tag/CTe
- **Manual MDF-e:** https://focusnfe.com.br/doc/#tag/MDFe

### Suporte Focus NFe
- **Email:** contato@acras.com.br
- **WhatsApp:** (47) 3041-1850
- **Horário:** 8h-18h (seg-sex)

### SEFAZ
- **Portal Nacional:** http://www.nfe.fazenda.gov.br/
- **Status dos Serviços:** http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx

---

## 🎯 Próximos Passos

Após configurar Focus NFe:

1. Implementar emissão automática de CT-e ao confirmar pedido
2. Integrar geração de DACTE (PDF)
3. Envio automático de CT-e por email para cliente
4. Dashboard de documentos fiscais emitidos
5. Relatórios de impostos

---

**Última atualização:** Janeiro 2026  
**Versão:** 1.0
