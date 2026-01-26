# 📧 Configuração de SMTP para Emails - LogiFlow CRM

## 📋 Visão Geral

O LogiFlow CRM envia emails transacionais para:
- ✅ Confirmação de pagamento
- ✅ Boas-vindas com credenciais de acesso
- ✅ Confirmação de solicitação de demo
- ✅ Notificações para equipe de vendas

---

## 🚀 Opções de Configuração SMTP

### Opção 1: Gmail (Recomendado para testes)

#### Passo 1: Habilitar "App Passwords"

1. Acesse: https://myaccount.google.com/security
2. Ative a **Verificação em duas etapas** (obrigatório)
3. Acesse: https://myaccount.google.com/apppasswords
4. Crie uma senha de app:
   - **Nome:** LogiFlow CRM
   - Copie a senha gerada (16 caracteres)

#### Passo 2: Configurar `.env`

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu.email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
FROM_EMAIL=seu.email@gmail.com
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@suaempresa.com.br
```

**Limites do Gmail:**
- 500 emails/dia (conta gratuita)
- 2.000 emails/dia (Google Workspace)

---

### Opção 2: SendGrid (Recomendado para produção)

SendGrid oferece **100 emails/dia GRÁTIS** e é super confiável.

#### Passo 1: Criar Conta

1. Acesse: https://signup.sendgrid.com
2. Crie uma conta gratuita
3. Verifique seu email

#### Passo 2: Criar API Key

1. Acesse: https://app.sendgrid.com/settings/api_keys
2. Clique em **"Create API Key"**
3. Configure:
   - **Nome:** LogiFlow CRM Production
   - **Permissões:** Full Access (Mail Send)
4. Copie a API Key (começa com `SG.`)

#### Passo 3: Verificar Domínio (Opcional mas recomendado)

1. Acesse: https://app.sendgrid.com/settings/sender_auth/senders
2. Clique em **"Verify a Single Sender"**
3. Preencha com seus dados
4. Confirme o email de verificação

#### Passo 4: Configurar `.env`

```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@seudominio.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@seudominio.com.br
```

**Vantagens SendGrid:**
- ✅ 100 emails/dia grátis
- ✅ Alta deliverability
- ✅ Analytics de emails
- ✅ Escalável (até 100k/dia)

---

### Opção 3: Mailgun

Mailgun oferece **5.000 emails/mês GRÁTIS** nos primeiros 3 meses.

#### Passo 1: Criar Conta

1. Acesse: https://signup.mailgun.com
2. Crie uma conta (requer cartão de crédito, mas não cobra nos primeiros 3 meses)
3. Verifique email e telefone

#### Passo 2: Obter Credenciais SMTP

1. Acesse: https://app.mailgun.com/app/sending/domains
2. Selecione seu domínio de sandbox (ou configure domínio próprio)
3. Vá em **"SMTP credentials"**
4. Copie:
   - **SMTP hostname:** `smtp.mailgun.org`
   - **Port:** `587`
   - **Username:** `postmaster@sandbox...`
   - **Password:** (crie uma senha)

#### Passo 3: Configurar `.env`

```bash
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@sandboxXXXXXXXXXXXXXXXX.mailgun.org
SMTP_PASSWORD=sua_senha_aqui
FROM_EMAIL=noreply@seudominio.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@seudominio.com.br
```

---

### Opção 4: Amazon SES (Para alto volume)

Recomendado apenas para produção com alto volume (>10k emails/dia).

**Custo:** $0.10 por 1.000 emails (muito barato!)

#### Configuração Rápida:

1. Acesse: https://console.aws.amazon.com/ses
2. Verifique seu domínio
3. Saia do modo sandbox (request production access)
4. Configure SMTP credentials

```bash
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=AKIAXXXXXXXXXXXXXXXX
SMTP_PASSWORD=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FROM_EMAIL=noreply@seudominio.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@seudominio.com.br
```

---

## ✅ Validação da Configuração

### Teste 1: Verificar variáveis

```bash
# No container do backend
docker-compose exec backend env | grep SMTP
```

Deve mostrar:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu@email.com
SMTP_PASSWORD=****
```

### Teste 2: Enviar email de teste

Crie um arquivo `test_email.py`:

```python
import sys
sys.path.append('/app')

from services.email_service import email_service

result = email_service.send_email(
    to_email="seu@email.com",
    subject="🧪 Teste LogiFlow CRM",
    html_content="<h1>Email funcionando!</h1><p>Se você recebeu este email, está tudo OK!</p>"
)

print(f"Resultado: {'✅ Sucesso' if result else '❌ Erro'}")
```

Execute:
```bash
docker-compose exec backend python test_email.py
```

### Teste 3: Fluxo completo de checkout

1. Faça um pagamento de teste
2. Verifique os logs:
```bash
docker-compose logs -f backend | grep "Email"
```

Deve mostrar:
```
✅ Email de confirmação de pagamento enviado
✅ Email de boas-vindas com credenciais enviado
```

---

## 🚨 Troubleshooting

### Erro: "Authentication failed"

**Gmail:**
- Verifique se está usando App Password (não a senha normal)
- Verifique se a verificação em 2 etapas está ativa

**SendGrid:**
- Verifique se copiou a API Key corretamente
- Username deve ser exatamente `apikey` (não seu email!)

**Mailgun:**
- Verifique se criou uma senha para o usuário SMTP
- Use o domínio completo no username

### Erro: "Connection refused" ou "Timeout"

1. **Verifique o SMTP_HOST:**
   ```bash
   docker-compose exec backend ping smtp.gmail.com
   ```

2. **Verifique a porta:**
   - Use porta `587` (TLS)
   - NÃO use porta `465` (SSL)
   - NÃO use porta `25` (bloqueada em muitos hosts)

3. **Firewall/Security Group:**
   - Libere saída na porta 587
   - Em AWS/GCP, verifique Security Groups

### Emails caindo em SPAM

1. **Configure SPF, DKIM e DMARC:**
   - SendGrid e Mailgun fazem isso automaticamente
   - Gmail não recomendado para produção por isso

2. **Use domínio próprio:**
   - `noreply@seudominio.com.br`
   - NÃO use: `noreply@gmail.com`

3. **Verifique domínio no provedor:**
   - SendGrid: Domain Authentication
   - Mailgun: Domain Verification

### Modo Simulação (SMTP não configurado)

Se SMTP não estiver configurado, o sistema funciona em **modo simulação**:

```
⚠️  SMTP não configurado - email não será enviado
📧 [SIMULADO] Email para usuario@exemplo.com: Bem-vindo ao LogiFlow!
```

Para **produção**, SMTP DEVE estar configurado.

---

## 📊 Monitoramento

### Logs em Produção

Sempre monitore os logs de email:

```bash
# Ver últimos 100 emails enviados
docker-compose logs backend | grep "Email" | tail -100

# Ver erros de email
docker-compose logs backend | grep "❌.*email" -i

# Ver emails bem-sucedidos
docker-compose logs backend | grep "✅ Email"
```

### Métricas Importantes

Acompanhe no dashboard do seu provedor SMTP:

- **Delivered:** % de emails entregues
- **Opened:** % de emails abertos
- **Clicked:** % de cliques nos links
- **Bounced:** % de emails rejeitados
- **Spam Reports:** Reclamações de spam

**Meta ideal:**
- Delivery rate: >95%
- Bounce rate: <5%
- Spam rate: <0.1%

---

## 🎯 Melhores Práticas

1. **Use domínio próprio**
   - `@suaempresa.com.br` > `@gmail.com`

2. **Configure autenticação**
   - SPF, DKIM, DMARC

3. **Monitore bounce rate**
   - Remove emails inválidos

4. **Teste antes de produção**
   - Envie para diferentes provedores
   - Gmail, Outlook, Yahoo

5. **Não faça spam**
   - Respeite opt-out
   - Envie apenas emails transacionais

6. **Templates responsivos**
   - Já implementados no código ✅
   - Testados em mobile

---

## ✅ Checklist de Produção

- [ ] Provedor SMTP escolhido (SendGrid recomendado)
- [ ] Credenciais configuradas no `.env`
- [ ] Domínio verificado no provedor
- [ ] SPF/DKIM configurados
- [ ] Email de teste enviado e recebido
- [ ] Fluxo completo testado (pagamento → emails)
- [ ] Emails NÃO caindo em spam
- [ ] Monitoramento de logs configurado
- [ ] Dashboard do provedor acessível
- [ ] Limites de envio adequados ao volume

---

## 📞 Suporte

**Dúvidas sobre SMTP:**
- SendGrid: https://sendgrid.com/support
- Mailgun: https://help.mailgun.com
- Gmail: https://support.google.com/mail

**Código do email service:**
- `backend/services/email_service.py`

---

**Última atualização:** 23 de Janeiro de 2026
