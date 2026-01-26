# 📄 Configuração Focus NFe - CT-e/MDF-e - LogiFlow CRM

## 📋 O que é Focus NFe?

Focus NFe é um serviço para emissão de documentos fiscais eletrônicos (CT-e, NF-e, MDF-e, etc) através de API.

**Funcionalidades no LogiFlow:**
- ✅ Emissão de CT-e (Conhecimento de Transporte Eletrônico)
- ✅ Emissão de MDF-e (Manifesto de Documentos Fiscais Eletrônicos)
- ✅ Consulta de status
- ✅ Cancelamento de documentos
- ✅ Download de PDF e XML

---

## 🚀 Passo a Passo

### 1. Criar Conta no Focus NFe

1. Acesse: https://focusnfe.com.br
2. Clique em **"Teste Grátis"** ou **"Criar Conta"**
3. Preencha o cadastro:
   - Email corporativo
   - Dados da empresa
   - CNPJ
4. Confirme o email

### 2. Obter Token de API

#### Ambiente de HOMOLOGAÇÃO (Testes):

1. Faça login em: https://homologacao.focusnfe.com.br
2. Acesse **"Configurações"** → **"Tokens"**
3. Copie o **Token de Homologação**
4. Formato: `homologacao_abcdef1234567890`

#### Ambiente de PRODUÇÃO:

1. Faça login em: https://app.focusnfe.com.br
2. Acesse **"Configurações"** → **"Tokens"**
3. Gere um novo token ou copie o existente
4. Formato: `producao_abcdef1234567890`

⚠️ **IMPORTANTE:** 
- Tokens de homologação **NÃO** funcionam em produção
- Documentos de homologação **NÃO** têm validade fiscal

### 3. Configurar Certificado Digital

Para emitir documentos fiscais, você precisa de um **Certificado Digital A1**.

#### 3.1. Upload do Certificado

1. No painel Focus NFe, vá em **"Certificado Digital"**
2. Faça upload do arquivo `.pfx` ou `.p12`
3. Digite a senha do certificado
4. Clique em **"Enviar"**

#### 3.2. Validação

O Focus NFe valida automaticamente:
- ✅ Certificado dentro da validade
- ✅ CNPJ do certificado = CNPJ da conta
- ✅ Cadeia de certificação válida

### 4. Configurar Variáveis de Ambiente

Edite o arquivo `.env`:

#### Para HOMOLOGAÇÃO (Testes):

```bash
# Focus NFe - CT-e/MDF-e
FOCUSNFE_TOKEN=homologacao_abcdef1234567890abcdef1234567890
FOCUSNFE_ENVIRONMENT=homologacao
```

#### Para PRODUÇÃO:

```bash
# Focus NFe - CT-e/MDF-e
FOCUSNFE_TOKEN=producao_abcdef1234567890abcdef1234567890
FOCUSNFE_ENVIRONMENT=producao
```

### 5. Configurar Dados da Empresa

No painel Focus NFe, configure:

1. **Dados Cadastrais:**
   - Razão Social
   - CNPJ
   - Inscrição Estadual
   - Endereço completo

2. **Configurações Fiscais:**
   - Regime Tributário
   - CSOSN/CST padrão
   - Alíquotas de ICMS

3. **Série de Documentos:**
   - CT-e: Série 1 (padrão)
   - MDF-e: Série 1 (padrão)

---

## ✅ Validação da Configuração

### Teste 1: Verificar Token

```bash
# No container do backend
docker-compose exec backend python -c "
import os
token = os.getenv('FOCUSNFE_TOKEN', '')
env = os.getenv('FOCUSNFE_ENVIRONMENT', '')
print(f'Token: {token[:20]}...')
print(f'Ambiente: {env}')
"
```

### Teste 2: Testar Conexão

Crie `test_focusnfe.py`:

```python
import sys
sys.path.append('/app')

from integrations.fiscal.focusnfe import FocusNFeClient
import os

token = os.getenv('FOCUSNFE_TOKEN')
ambiente = os.getenv('FOCUSNFE_ENVIRONMENT', 'homologacao')

if not token:
    print("❌ FOCUSNFE_TOKEN não configurado!")
    exit(1)

client = FocusNFeClient(token=token, ambiente=ambiente)
print(f"✅ Cliente Focus NFe criado")
print(f"   Ambiente: {ambiente}")
print(f"   URL: {client.base_url}")
```

Execute:
```bash
docker-compose exec backend python test_focusnfe.py
```

### Teste 3: Emitir CT-e de Teste (Homologação)

```python
import sys
sys.path.append('/app')

from integrations.fiscal.focusnfe import FocusNFeClient
import os

token = os.getenv('FOCUSNFE_TOKEN')
client = FocusNFeClient(token=token, ambiente='homologacao')

dados_teste = {
    "numero": "1",
    "serie": "1",
    "natureza_operacao": "PRESTACAO DE SERVICO DE TRANSPORTE",
    "modal": "01",  # Rodoviário
    "tomador": {
        "tipo": "3",  # Destinatário
        "documento": "12345678000100",
        "nome": "EMPRESA TESTE LTDA",
        "endereco": "RUA TESTE",
        "numero": "123",
        "bairro": "CENTRO",
        "cidade": "SAO PAULO",
        "uf": "SP",
        "cep": "01310100"
    },
    "remetente": {
        "documento": "12345678000100",
        "nome": "REMETENTE TESTE",
        "endereco": "RUA A",
        "numero": "100",
        "bairro": "CENTRO",
        "cidade": "SAO PAULO",
        "uf": "SP",
        "cep": "01310100"
    },
    "destinatario": {
        "documento": "98765432000100",
        "nome": "DESTINATARIO TESTE",
        "endereco": "RUA B",
        "numero": "200",
        "bairro": "CENTRO",
        "cidade": "RIO DE JANEIRO",
        "uf": "RJ",
        "cep": "20040020"
    },
    "valores": {
        "valor_total": 100.00,
        "valor_receber": 100.00,
        "valor_carga": 500.00,
        "peso_kg": 10.50,
        "produto_predominante": "MERCADORIA GERAL"
    },
    "veiculo": {
        "placa": "ABC1234",
        "uf": "SP",
        "tipo": "02"  # Caminhão
    },
    "rntrc": "12345678",
    "icms_aliquota": "12.00"
}

resultado = client.emitir_cte(dados_teste)

if resultado["success"]:
    print(f"✅ CT-e emitido com sucesso!")
    print(f"   Número: {resultado['numero']}")
    print(f"   Chave: {resultado['chave']}")
else:
    print(f"❌ Erro ao emitir CT-e:")
    print(f"   {resultado.get('error')}")
```

---

## 🚨 Troubleshooting

### Erro: "Token inválido"

**Causa:** Token incorreto ou ambiente errado

**Solução:**
1. Verifique se copiou o token completo
2. Confirme se está usando token de homologação no ambiente correto
3. Regere o token no painel Focus NFe

```bash
# Testar token manualmente
curl -X GET https://homologacao.focusnfe.com.br/v2/cte \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Erro: "Certificado não encontrado"

**Causa:** Certificado digital não configurado

**Solução:**
1. Acesse o painel Focus NFe
2. Faça upload do certificado A1 (.pfx)
3. Aguarde validação (pode levar alguns minutos)

### Erro: "CNPJ do certificado diferente do emissor"

**Causa:** Certificado de outro CNPJ

**Solução:**
- Use certificado do mesmo CNPJ da conta Focus NFe
- OU configure múltiplos emissores no Focus NFe

### Erro: "Série não autorizada"

**Causa:** Série não configurada na SEFAZ

**Solução:**
1. Configure a série no painel Focus NFe
2. Aguarde sincronização com SEFAZ (até 24h)
3. Use série 1 (geralmente já autorizada)

### Erro: "Rejeição 999: Erro não catalogado"

**Causa:** Dados inválidos ou faltantes

**Solução:**
1. Verifique logs detalhados
2. Confira todos os campos obrigatórios
3. Valide CNPJs, CEPs e códigos de município
4. Consulte documentação da SEFAZ

---

## 📊 Monitoramento

### Logs do Sistema

```bash
# Ver emissões de CT-e
docker-compose logs backend | grep "CT-e"

# Ver erros Focus NFe
docker-compose logs backend | grep "Focus" | grep "ERROR"
```

### Dashboard Focus NFe

Acompanhe no painel:
- **Documentos Emitidos:** Total por período
- **Taxa de Sucesso:** % de aprovação
- **Rejeições:** Motivos mais comuns
- **Consumo de API:** Requests por mês

### Limites e Custos

**Plano Gratuito (Trial):**
- 10 documentos/mês
- Apenas homologação

**Plano Básico:**
- R$ 49,90/mês
- 100 documentos/mês
- Produção + homologação

**Plano Professional:**
- R$ 199,90/mês
- 500 documentos/mês
- Suporte prioritário

**Documentos adicionais:**
- R$ 0,45 por documento

---

## 📚 Documentação Técnica

### Endpoints Implementados

```python
# backend/integrations/fiscal/focusnfe.py

client = FocusNFeClient(token="...", ambiente="producao")

# CT-e
client.emitir_cte(dados)           # Emitir CT-e
client.consultar_cte(ref)          # Consultar status
client.cancelar_cte(ref, justif)   # Cancelar CT-e
client.download_pdf(ref, "cte")    # Baixar DACTE
client.download_xml(ref, "cte")    # Baixar XML

# MDF-e
client.emitir_mdfe(dados)          # Emitir MDF-e
client.consultar_mdfe(ref)         # Consultar status
client.encerrar_mdfe(ref, uf, cod) # Encerrar MDF-e
client.cancelar_mdfe(ref, justif)  # Cancelar MDF-e
client.download_pdf(ref, "mdfe")   # Baixar DAMDFE
```

### Estrutura de Dados CT-e

Ver exemplos completos em:
- `backend/routers/fiscal.py` - Schemas Pydantic
- Documentação Focus NFe: https://doc.focusnfe.com.br

---

## 🎯 Checklist de Produção

- [ ] Conta Focus NFe criada
- [ ] Certificado Digital A1 válido
- [ ] Certificado enviado ao Focus NFe
- [ ] Token de produção obtido
- [ ] Token configurado no `.env`
- [ ] Dados da empresa configurados
- [ ] Série de documentos autorizada
- [ ] CT-e de teste emitido em homologação
- [ ] CT-e validado pela SEFAZ
- [ ] Plano Focus NFe adequado ao volume
- [ ] Monitoramento de logs ativo

---

## 📞 Suporte

**Focus NFe:**
- Site: https://focusnfe.com.br
- Suporte: https://suporte.focusnfe.com.br
- Documentação: https://doc.focusnfe.com.br
- Email: suporte@acras.com.br
- Telefone: (11) 3522-1555

**LogiFlow CRM:**
- Código: `backend/integrations/fiscal/focusnfe.py`
- Router: `backend/routers/fiscal.py`

---

**Última atualização:** 23 de Janeiro de 2026
