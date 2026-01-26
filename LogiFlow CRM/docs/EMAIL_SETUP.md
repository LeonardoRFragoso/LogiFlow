# Configuração do Sistema de Emails - LogiFlow CRM

## 📧 Visão Geral

O LogiFlow CRM usa SMTP para enviar emails transacionais como:
- ✅ Confirmação de solicitação de demo
- ✅ Credenciais de acesso após pagamento
- ✅ Confirmação de pagamento
- ✅ Notificações para equipe de vendas

---

## 🚀 Configuração Rápida

### 1. Escolher Provedor SMTP

Recomendamos uma das seguintes opções:

#### **Opção A: Gmail** (Mais Simples)
✅ Gratuito até 500 emails/dia  
✅ Configuração rápida  
❌ Limite de envios  

#### **Opção B: SendGrid** (Recomendado para Produção)
✅ 100 emails/dia gratuitos  
✅ 40.000 emails/mês no plano pago  
✅ Analytics e tracking  
✅ Alta deliverability  

#### **Opção C: AWS SES** (Escalável)
✅ $0.10 por 1.000 emails  
✅ Altamente escalável  
❌ Configuração mais complexa  

#### **Opção D: Mailgun**
✅ 5.000 emails/mês gratuitos  
✅ API simples  
✅ Boa deliverability  

---

## 📋 Configuração Passo a Passo

### **OPÇÃO A: Usar Gmail (Desenvolvimento)**

#### 1. Criar Senha de App no Gmail

1. Acesse sua conta Google: https://myaccount.google.com/
2. Vá em **Segurança**
3. Ative **Verificação em duas etapas** (se ainda não estiver)
4. Vá em **Senhas de app**
5. Selecione **Email** e **Windows/Mac/Linux**
6. Copie a senha gerada (16 caracteres)

#### 2. Configurar no `.env`

```bash
# Email (SMTP) - Gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=<YOUR_GMAIL_APP_PASSWORD_HERE>
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

**⚠️ IMPORTANTE:** Use a senha de app, NÃO sua senha normal do Gmail!

---

### **OPÇÃO B: Usar SendGrid (Produção Recomendada)**

#### 1. Criar Conta SendGrid

1. Acesse: https://signup.sendgrid.com/
2. Crie uma conta gratuita
3. Verifique seu email

#### 2. Obter API Key

1. Vá em **Settings → API Keys**
2. Clique em **Create API Key**
3. Nome: `LogiFlow Production`
4. Permissões: **Full Access** ou **Mail Send**
5. Copie a API Key (você só verá uma vez!)

#### 3. Configurar no `.env`

```bash
# Email (SMTP) - SendGrid
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey  # Sempre "apikey"
SMTP_PASSWORD=<YOUR_SENDGRID_API_KEY_HERE>
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

#### 4. Verificar Sender (Importante!)

1. Vá em **Settings → Sender Authentication**
2. Clique em **Verify a Single Sender**
3. Preencha com `noreply@logiflow.com.br`
4. Confirme o email de verificação

**Sem verificação, os emails NÃO serão enviados!**

---

### **OPÇÃO C: Usar AWS SES**

#### 1. Criar Conta AWS e Configurar SES

1. Acesse AWS Console: https://console.aws.amazon.com/
2. Vá para **SES (Simple Email Service)**
3. Selecione região (ex: `us-east-1`)
4. Clique em **Create Identity**
5. Verifique domínio ou email

#### 2. Obter Credenciais SMTP

1. Em SES, vá em **SMTP Settings**
2. Clique em **Create SMTP Credentials**
3. Copie:
   - SMTP Username
   - SMTP Password
   - Server Name
   - Port

#### 3. Configurar no `.env`

```bash
# Email (SMTP) - AWS SES
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=AKIA...  # SMTP Username
SMTP_PASSWORD=<YOUR_AWS_SMTP_PASSWORD_HERE>
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

#### 4. Sair do Sandbox (Produção)

Por padrão, SES está em **sandbox mode** (só envia para emails verificados).

Para produção:
1. Vá em **Account dashboard**
2. Clique em **Request production access**
3. Preencha formulário justificando uso
4. Aguarde aprovação (1-2 dias úteis)

---

### **OPÇÃO D: Usar Mailgun**

#### 1. Criar Conta Mailgun

1. Acesse: https://signup.mailgun.com/
2. Crie conta gratuita
3. Verifique domínio

#### 2. Obter Credenciais SMTP

1. Vá em **Sending → Domain Settings**
2. Clique em **SMTP**
3. Copie as credenciais

#### 3. Configurar no `.env`

```bash
# Email (SMTP) - Mailgun
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@mg.logiflow.com.br
SMTP_PASSWORD=<YOUR_MAILGUN_PASSWORD_HERE>
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

---

## ✅ Testar Configuração

### 1. Executar Testes Automatizados

```bash
cd backend
pytest tests/test_email_service.py -v
```

### 2. Testar Envio Manual

Crie um script de teste: `backend/scripts/test_email.py`

```python
from services.email_service import email_service

# Testar email de confirmação de demo
result = email_service.send_demo_confirmation(
    name="Seu Nome",
    email="seu-email@exemplo.com",  # Coloque seu email real
    company="Empresa Teste",
    vehicles="10"
)

print(f"Email enviado: {result}")
```

Execute:
```bash
python scripts/test_email.py
```

### 3. Verificar Logs

Se configurado corretamente, você verá:
```
✅ Email enviado para seu-email@exemplo.com: Recebemos sua solicitação de demonstração! 🚀
```

Se não configurado (modo simulação):
```
⚠️  SMTP não configurado - email não será enviado
📧 [SIMULADO] Email para seu-email@exemplo.com: ...
```

---

## 🔍 Troubleshooting

### Problema: "Authentication failed"

**Causa:** Credenciais incorretas

**Solução:**
- Gmail: Verifique se está usando senha de app (16 caracteres)
- SendGrid: Verifique se o username é exatamente `apikey`
- Verifique se não há espaços extras nas credenciais

---

### Problema: "Connection refused"

**Causa:** Firewall bloqueando porta 587

**Solução:**
- Verifique firewall do servidor
- Tente porta 465 (SSL) ou 25 (não recomendado)
- Verifique se o provider SMTP está acessível

---

### Problema: Emails vão para SPAM

**Causa:** Falta de autenticação de domínio

**Solução:**
1. Configure **SPF** no DNS:
   ```
   v=spf1 include:_spf.google.com ~all  (Gmail)
   v=spf1 include:sendgrid.net ~all  (SendGrid)
   ```

2. Configure **DKIM** (fornecido pelo provider)

3. Configure **DMARC**:
   ```
   v=DMARC1; p=none; rua=mailto:dmarc@logiflow.com.br
   ```

---

### Problema: "Sender not verified" (SendGrid)

**Causa:** Email remetente não verificado

**Solução:**
1. Vá em SendGrid → Sender Authentication
2. Verifique o email `FROM_EMAIL`
3. Confirme o email de verificação

---

### Problema: Emails não enviados (AWS SES Sandbox)

**Causa:** Conta em sandbox mode

**Solução:**
- Para testes: Verifique o email destinatário no SES
- Para produção: Solicite remoção do sandbox

---

## 📊 Monitoramento

### Logs de Email

Todos os envios são logados:

```python
# Sucesso
✅ Email enviado para usuario@empresa.com: Assunto do Email

# Erro
❌ Erro ao enviar email para usuario@empresa.com: Erro SMTP...

# Modo simulação
📧 [SIMULADO] Email para usuario@empresa.com: Assunto do Email
```

### Métricas Importantes

Monitore:
- Taxa de envio bem-sucedido
- Taxa de bounce (rejeição)
- Taxa de emails marcados como spam
- Tempo de entrega

---

## 🔐 Segurança

### Boas Práticas

1. **Nunca commitar credenciais**
   - Use `.env` (não versionado)
   - Use variáveis de ambiente em produção

2. **Rotacionar senhas regularmente**
   - Troque API keys a cada 90 dias
   - Use senhas de app diferentes por ambiente

3. **Limite de envios**
   - Implemente rate limiting
   - Monitore uso para evitar abuso

4. **Validação de emails**
   - Valide formato antes de enviar
   - Use confirmação de email para cadastros

---

## 📈 Limites por Provider

| Provider  | Gratuito/Mês | Pago/Mês | Preço Aprox |
|-----------|--------------|----------|-------------|
| Gmail     | 500/dia      | N/A      | Gratuito    |
| SendGrid  | 100/dia      | 40k-100k | $15-$90     |
| AWS SES   | 62k          | Ilimitado| $0.10/1k    |
| Mailgun   | 5.000        | 50k-100k | $35-$80     |

---

## 🎯 Recomendações

### Desenvolvimento/Staging
✅ **Gmail** - Simples e gratuito

### Produção (até 5k emails/mês)
✅ **SendGrid Free** - Confiável e gratuito

### Produção (5k-50k emails/mês)
✅ **SendGrid Essentials** ou **Mailgun**

### Produção (50k+ emails/mês)
✅ **AWS SES** - Mais econômico em escala

---

## 📝 Checklist de Implementação

- [ ] Escolher provider SMTP
- [ ] Criar conta e obter credenciais
- [ ] Configurar variáveis no `.env`
- [ ] Verificar sender/domínio
- [ ] Executar testes automatizados
- [ ] Enviar email de teste real
- [ ] Verificar deliverability (não vai para spam)
- [ ] Configurar SPF/DKIM/DMARC (produção)
- [ ] Implementar monitoramento
- [ ] Documentar credenciais (secrets manager)

---

## 🆘 Suporte

### Documentação Oficial

- **Gmail:** https://support.google.com/mail/answer/7126229
- **SendGrid:** https://docs.sendgrid.com/
- **AWS SES:** https://docs.aws.amazon.com/ses/
- **Mailgun:** https://documentation.mailgun.com/

### Contato

Dúvidas sobre a implementação? Entre em contato com a equipe de desenvolvimento.

---

**Última atualização:** Janeiro 2026  
**Versão:** 1.0
