# Integração Focus NFe - Guia para Clientes

## ⚠️ IMPORTANTE

**A Focus NFe é uma API PAGA e EXTERNA ao LogiFlow CRM.**

O LogiFlow CRM oferece apenas a **integração técnica**. Você (cliente) precisa:
1. ✅ Contratar o serviço Focus NFe diretamente
2. ✅ Pagar pelos documentos emitidos à Focus NFe
3. ✅ Configurar seu Token de API no LogiFlow

---

## 📋 O Que é a Focus NFe?

A Focus NFe é uma plataforma de emissão de documentos fiscais eletrônicos que facilita a integração com a SEFAZ. Eles oferecem:

- ✅ Emissão de CT-e (Conhecimento de Transporte Eletrônico)
- ✅ Emissão de MDF-e (Manifesto de Documentos Fiscais Eletrônico)
- ✅ Consulta de status
- ✅ Cancelamento
- ✅ Download de PDF e XML
- ✅ Infraestrutura de conexão com SEFAZ
- ✅ Suporte técnico

**Site oficial**: https://focusnfe.com.br

---

## 💰 Custos

Os custos da Focus NFe são de responsabilidade do cliente:

- **Planos mensais** ou **pré-pago por documento**
- Valores variam conforme volume de documentos
- Ambiente de homologação é **gratuito** para testes
- Consulte preços no site: https://focusnfe.com.br/planos

> 💡 **Dica**: Comece com plano básico e aumente conforme necessidade.

---

## 🚀 Como Contratar e Configurar

### Passo 1: Contratar a Focus NFe

1. Acesse https://focusnfe.com.br
2. Clique em **Criar Conta** ou **Experimente Grátis**
3. Preencha seus dados cadastrais
4. Escolha um plano (ou comece com teste gratuito)
5. Confirme seu email

### Passo 2: Obter Token de API

1. Faça login no painel Focus NFe
2. Vá em **Minha Conta** → **Token de API**
3. Copie o Token (uma string longa como `abc123def456...`)
4. Guarde o Token em local seguro

### Passo 3: Configurar Certificado Digital (se necessário)

Para ambiente de **Produção**, você precisa:

1. Ter um **Certificado Digital A1** válido (e-CNPJ)
2. Fazer upload no painel Focus NFe
3. Associar ao seu CNPJ

> ℹ️ Para **Homologação**, não é necessário certificado.

### Passo 4: Configurar no LogiFlow CRM

1. Acesse o LogiFlow CRM
2. Vá em **Configurações > Configurações Fiscais**
3. Preencha os dados do emitente:
   - CNPJ
   - Razão Social
   - Inscrição Estadual
   - Endereço completo
4. **Cole o Token Focus NFe** obtido no Passo 2
5. Selecione o **Ambiente**:
   - **Homologação**: Para testes (gratuito)
   - **Produção**: Para documentos reais (pago por documento)
6. Configure RNTRC e ANTT (se aplicável)
7. Clique em **Salvar Configurações**

### Passo 5: Testar a Integração

1. Comece no ambiente de **Homologação**
2. Emita um CT-e de teste
3. Verifique se foi autorizado
4. Confira o documento no painel Focus NFe
5. Só vá para **Produção** após testes bem-sucedidos

---

## 🔒 Segurança

### Token de API

- ✅ Token é armazenado **criptografado** no banco de dados
- ✅ Cada tenant tem seu próprio token (multi-tenancy)
- ✅ Token não é compartilhado entre clientes
- ✅ Nunca compartilhe seu token com terceiros

### Certificado Digital

- ✅ Armazene com segurança
- ✅ Renove antes do vencimento
- ✅ Use senha forte
- ✅ Faça backup do certificado

---

## 📊 Ambientes

### Homologação
- **Uso**: Testes e desenvolvimento
- **Custo**: Gratuito
- **Documentos**: Sem valor fiscal
- **SEFAZ**: Ambiente de teste da SEFAZ
- **Certificado**: Não requer

### Produção
- **Uso**: Documentos reais
- **Custo**: Pago por documento
- **Documentos**: Valor fiscal pleno
- **SEFAZ**: Ambiente oficial da SEFAZ
- **Certificado**: Requer A1 válido

> ⚠️ **Importante**: Sempre teste em Homologação antes de ir para Produção!

---

## 🔧 Troubleshooting

### "Token inválido" ou "Erro 401"

**Causas possíveis:**
1. Token digitado incorretamente
2. Token expirado
3. Conta Focus NFe suspensa por falta de pagamento
4. Token revogado

**Solução:**
1. Copie o token novamente do painel Focus NFe
2. Verifique se sua conta Focus NFe está ativa
3. Confirme se tem créditos/saldo disponível
4. Entre em contato com suporte Focus NFe se persistir

### "Certificado digital não encontrado"

**Causa**: Produção sem certificado configurado

**Solução:**
1. Faça upload do certificado A1 no painel Focus NFe
2. Associe ao CNPJ correto
3. Aguarde alguns minutos para sincronização

### "Sem créditos para emissão"

**Causa**: Plano pré-pago sem saldo

**Solução:**
1. Acesse painel Focus NFe
2. Adicione créditos ou mude para plano mensal
3. Tente emitir novamente

### "CNPJ não autorizado a emitir CT-e"

**Causa**: CNPJ não está credenciado na SEFAZ

**Solução:**
1. Solicite credenciamento na SEFAZ do seu estado
2. Aguarde aprovação (pode levar dias)
3. Configure certificado digital
4. Tente novamente após credenciamento

---

## 📞 Suporte

### Suporte Focus NFe

Para questões sobre:
- Token de API
- Certificado digital
- Planos e pagamentos
- Credenciamento SEFAZ
- Erros da API Focus NFe

**Contato**: suporte@focusnfe.com.br  
**Site**: https://focusnfe.com.br/suporte

### Suporte LogiFlow

Para questões sobre:
- Configuração no LogiFlow
- Interface do sistema
- Fluxo de emissão
- Bugs do LogiFlow

**Contato**: suporte@logiflow.com.br

---

## 📚 Documentação Oficial

- **API Focus NFe**: https://focusnfe.com.br/doc/
- **CT-e SEFAZ**: http://www.cte.fazenda.gov.br/
- **MDF-e SEFAZ**: http://www.mdfe.fazenda.gov.br/

---

## 💡 Dicas e Boas Práticas

### Para Economizar

1. **Teste tudo em Homologação** (gratuito) antes de ir para Produção
2. **Revise dados** antes de emitir (cancelamento também custa)
3. **Configure numeração** correta desde o início
4. **Escolha plano adequado** ao seu volume mensal

### Para Evitar Problemas

1. ✅ Mantenha certificado digital válido
2. ✅ Monitore data de vencimento
3. ✅ Guarde XMLs autorizados
4. ✅ Faça backup regular
5. ✅ Teste após cada atualização
6. ✅ Mantenha dados do emitente atualizados

### Para Produtividade

1. ✅ Configure notificações automáticas
2. ✅ Use emissão automática após aprovar pedido
3. ✅ Agrupe CT-es em MDF-e automaticamente
4. ✅ Configure observações padrão

---

## ❓ FAQ

**P: O LogiFlow fornece conta Focus NFe?**  
R: Não. Cada cliente deve contratar diretamente com a Focus NFe.

**P: Posso usar o mesmo token em múltiplos tenants?**  
R: Não recomendado. Cada empresa (tenant) deve ter sua própria conta Focus NFe.

**P: Quanto custa emitir um CT-e?**  
R: Consulte os planos no site da Focus NFe. O custo é pago à Focus NFe, não ao LogiFlow.

**P: Preciso de certificado digital?**  
R: Apenas para ambiente de Produção. Homologação não requer.

**P: Posso emitir sem internet?**  
R: Não. A emissão requer conexão com a Focus NFe e SEFAZ.

**P: Os documentos ficam salvos no LogiFlow?**  
R: Sim. Salvamos todos os dados, XMLs e links para PDFs.

**P: Posso mudar de Focus NFe para outro provedor?**  
R: Sim, mas requer adaptação na integração (não suportado atualmente).

**P: A Focus NFe tem suporte 24/7?**  
R: Verifique os horários no site da Focus NFe.

---

**Última atualização**: Janeiro 2026  
**Versão**: 1.0.0
