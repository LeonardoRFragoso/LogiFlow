# 🚀 Configuração SendGrid no Railway

## Variáveis de Ambiente para Adicionar

Acesse o painel do Railway e adicione as seguintes variáveis de ambiente no serviço `logiflow-api`:

### 1. SendGrid API Key
```
SENDGRID_API_KEY=[Cole aqui a chave API que você criou no SendGrid]
```

### 2. Email Configuration
```
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

## Passos para Configurar no Railway

1. Acesse: https://railway.app
2. Selecione o projeto: **luminous-heart**
3. Selecione o serviço: **logiflow-api**
4. Vá para a aba: **Variables**
5. Clique em **Add Variable** para cada variável acima
6. Cole os valores correspondentes
7. Clique em **Deploy** para aplicar as mudanças

## Verificar Configuração

Após configurar, você pode verificar se as variáveis foram aplicadas:

```bash
cd "LogiFlow CRM/backend"
railway variables | grep SENDGRID
```

## Testar Envio de Email

Após configurar, teste o envio:

```bash
python -c "
from services.sendgrid_email_service import sendgrid_email_service
result = sendgrid_email_service.send_welcome_email(
    tenant_id=1,
    company_name='Test Company',
    contact_name='Test User',
    contact_email='seu_email@example.com',
    subdomain='test',
    plan='starter',
    admin_email='seu_email@example.com',
    admin_password='TempPassword123!'
)
print('✅ Email enviado com sucesso!' if result else '❌ Erro ao enviar email')
"
```

## Status

- ✅ Chave API criada no SendGrid
- ⏳ Variáveis de ambiente a configurar no Railway
- ⏳ Testar envio de email

## Segurança

⚠️ **IMPORTANTE:** Nunca compartilhe sua chave API do SendGrid. Mantenha-a segura nas variáveis de ambiente do Railway.

---

**Próximo Passo:** Adicionar as variáveis de ambiente no painel do Railway
