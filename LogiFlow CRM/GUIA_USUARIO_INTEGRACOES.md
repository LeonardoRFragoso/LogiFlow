# 🔌 Guia do Usuário - Configuração de Integrações

## 📋 Introdução

O LogiFlow CRM permite que você configure suas próprias integrações com sistemas externos como:
- 📄 **Focus NFe** - Emissão de CT-e e MDF-e
- 📦 **Melhor Envio** - Cotação de frete com múltiplas transportadoras
- 🚚 **Frenet** - Cálculo de frete inteligente

Cada empresa configura suas próprias credenciais de forma segura e independente.

---

## 🚀 Como Acessar

1. Faça login no LogiFlow CRM
2. No menu lateral, clique em **⚙️ Configurações**
3. Clique em **🔌 Integrações**

Você verá 3 abas:
- **ERP** - Integrações com sistemas de gestão (futuro)
- **GPS** - Rastreamento de frotas (futuro)
- **Frete** - Cotação e emissão de documentos fiscais ✅

---

## 📄 Focus NFe - Emissão de CT-e/MDF-e

### O que é?

Focus NFe é um serviço para emitir documentos fiscais eletrônicos como:
- **CT-e** - Conhecimento de Transporte Eletrônico
- **MDF-e** - Manifesto de Documentos Fiscais Eletrônicos

### Como Configurar

#### Passo 1: Criar conta no Focus NFe

1. Acesse: https://focusnfe.com.br
2. Clique em **"Teste Grátis"**
3. Preencha o cadastro da sua empresa
4. Confirme o email

#### Passo 2: Obter Token de API

**Para Testes (Homologação):**
1. Acesse: https://homologacao.focusnfe.com.br
2. Faça login
3. Vá em **Configurações** → **Tokens**
4. Copie o token (começa com `homologacao_`)

**Para Produção:**
1. Acesse: https://app.focusnfe.com.br
2. Vá em **Configurações** → **Tokens**
3. Copie o token (começa com `producao_`)
4. ⚠️ Certifique-se de ter enviado seu certificado digital A1

#### Passo 3: Configurar no LogiFlow

1. Na aba **Frete**, encontre o card **Focus NFe**
2. Clique em **Configurar**
3. Preencha:
   - **Token de API**: Cole o token copiado
   - **Ambiente**: 
     - Escolha **Homologação (Testes)** para testar
     - Escolha **Produção** quando estiver pronto
4. Marque **"Ativar integração imediatamente"**
5. Clique em **Salvar Credenciais**

#### Passo 4: Testar

1. Clique no botão **🔍 Testar**
2. Aguarde a validação
3. Você verá ✅ ou ❌ indicando se funcionou

### Como Usar

Após configurar, você pode emitir CT-e diretamente no LogiFlow:

1. Vá em **Pedidos** → selecione um pedido
2. Clique em **Emitir CT-e**
3. Preencha os dados fiscais
4. Clique em **Emitir**

O sistema usará automaticamente suas credenciais Focus NFe!

### Preços Focus NFe

- **Teste Grátis**: 10 documentos/mês (homologação)
- **Plano Básico**: R$ 49,90/mês - 100 documentos
- **Documentos adicionais**: R$ 0,45 cada

---

## 📦 Melhor Envio - Cotação de Frete

### O que é?

Melhor Envio integra múltiplas transportadoras:
- Correios (PAC, SEDEX)
- Jadlog
- Azul Cargo
- Latam Cargo
- Total Express

### Como Configurar

#### Passo 1: Criar conta no Melhor Envio

1. Acesse: https://melhorenvio.com.br
2. Clique em **"Cadastre-se grátis"**
3. Preencha os dados da empresa
4. Confirme o email

#### Passo 2: Obter Token

**Para Testes (Sandbox):**
1. Acesse: https://sandbox.melhorenvio.com.br
2. Faça login
3. Vá em **Configurações** → **API**
4. Clique em **Gerar Token**
5. Copie o token (começa com `eyJ...`)

**Para Produção:**
1. Acesse: https://melhorenvio.com.br
2. Complete o cadastro da empresa
3. **IMPORTANTE**: Adicione saldo na conta (via PIX ou boleto)
4. Vá em **Configurações** → **API**
5. Gere o token de produção

#### Passo 3: Configurar no LogiFlow

1. Na aba **Frete**, encontre o card **Melhor Envio**
2. Clique em **Configurar**
3. Preencha:
   - **Token de API**: Cole o token
   - **Ambiente**:
     - **Sandbox (Testes)** para testar
     - **Produção** quando tiver saldo
4. Marque **"Ativar integração"**
5. Clique em **Salvar**

### Como Usar

Após configurar, o sistema usará Melhor Envio automaticamente:

1. Ao criar uma **Cotação de Frete**:
   - O sistema consultará automaticamente o Melhor Envio
   - Você verá opções de Correios, Jadlog, etc
   - Escolha a melhor opção

2. O cliente pode visualizar as opções e escolher

### Custos

- **Sem mensalidade!**
- Você paga apenas o frete de cada envio
- Preços com desconto negociado pelo Melhor Envio
- Pagamento via saldo na plataforma

**Exemplo:**
- PAC SP → RJ: R$ 25,00
- SEDEX SP → RJ: R$ 45,00

---

## 🚚 Frenet (Opcional)

### O que é?

Frenet é similar ao Melhor Envio, focado em e-commerce.

### Como Configurar

1. Crie conta em: https://painel.frenet.com.br/cadastro
2. Aguarde aprovação (1-2 dias)
3. Obtenha o token em **Configurações** → **Token de Integração**
4. Configure no LogiFlow (aba **Frete**)

---

## 🔒 Segurança

### Suas credenciais estão seguras!

- ✅ **Criptografadas**: Tokens são criptografados no banco de dados
- ✅ **Isoladas**: Cada empresa tem suas próprias credenciais
- ✅ **Privadas**: Nenhuma outra empresa pode ver suas chaves
- ✅ **Auditadas**: Registramos quando foram usadas

### Boas Práticas

1. **Nunca compartilhe** seus tokens com terceiros
2. **Use ambiente de testes** antes de produção
3. **Valide** após configurar (botão Testar)
4. **Monitore** o uso no painel de cada serviço
5. **Revogue tokens** antigos quando trocar

---

## ❓ Perguntas Frequentes

### Posso trocar minhas credenciais depois?

Sim! Basta clicar em **Editar** no card da integração e atualizar.

### E se eu quiser desativar temporariamente?

Clique em **Editar** e desmarque **"Ativar integração"**.

### O que acontece se meu token expirar?

1. Você receberá erro ao tentar usar
2. Gere um novo token no painel do serviço
3. Atualize no LogiFlow

### Posso usar o mesmo token em diferentes sistemas?

**Não é recomendado!** Cada sistema deve ter seu próprio token por segurança.

### Quanto custa configurar?

**É gratuito** no LogiFlow! Você paga apenas:
- Plano do Focus NFe (se usar)
- Saldo do Melhor Envio (por envio)
- Plano do Frenet (se usar)

---

## 📞 Suporte

### Problemas com Focus NFe?

- Suporte Focus NFe: suporte@acras.com.br
- Telefone: (11) 3522-1555
- Documentação: https://doc.focusnfe.com.br

### Problemas com Melhor Envio?

- Suporte ME: https://melhorenvio.com.br/suporte
- WhatsApp: (11) 3230-2023

### Problemas no LogiFlow?

- Email: suporte@logiflow.com.br
- WhatsApp: (11) 99999-9999
- Chat: Dentro do sistema

---

## ✅ Checklist de Configuração

Antes de usar em produção, verifique:

### Focus NFe
- [ ] Conta criada
- [ ] Certificado Digital enviado
- [ ] Token obtido
- [ ] Configurado no LogiFlow
- [ ] Testado e validado ✅
- [ ] CT-e de teste emitido em homologação
- [ ] Plano Focus NFe contratado

### Melhor Envio
- [ ] Conta criada
- [ ] Cadastro completo
- [ ] Saldo adicionado (produção)
- [ ] Token obtido
- [ ] Configurado no LogiFlow
- [ ] Testado e validado ✅
- [ ] Cotação de teste funcionando

---

## 🎯 Próximos Passos

Após configurar suas integrações:

1. ✅ Teste em **ambiente de homologação/sandbox**
2. ✅ Emita um documento de teste
3. ✅ Faça uma cotação de teste
4. ✅ Valide que os dados estão corretos
5. ✅ Mude para **produção**
6. ✅ Comece a usar normalmente!

---

**Última atualização:** 23 de Janeiro de 2026

**Precisa de ajuda?** Entre em contato com nosso suporte! 💬
