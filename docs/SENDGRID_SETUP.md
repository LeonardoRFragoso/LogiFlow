# 📧 Configuração SendGrid para LogiFlow

## Passo 1: Criar Nova Chave API no SendGrid

1. Acesse: https://app.sendgrid.com/settings/api_keys
2. Clique em "Create API Key"
3. Configure:
   - **Name:** LogiFlow Production
   - **API Key Permissions:** 
     - Mail Send (Full Access)
     - Template Engine (Read)
4. Copie a chave gerada (será exibida apenas uma vez)

## Passo 2: Atualizar Variáveis de Ambiente no Railway

No painel do Railway, adicione/atualize:

```
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br
```

## Passo 3: Instalar Dependência

```bash
pip install sendgrid
```

Ou adicionar ao `requirements.txt`:
```
sendgrid>=6.10.0
```

## Passo 4: Testar Envio de Email

```bash
cd "LogiFlow CRM/backend"
python -c "
from services.sendgrid_email_service import sendgrid_email_service
result = sendgrid_email_service.send_welcome_email(
    tenant_id=1,
    company_name='Test Company',
    contact_name='Test User',
    contact_email='test@example.com',
    subdomain='test',
    plan='starter',
    admin_email='test@example.com',
    admin_password='TempPassword123!'
)
print('Email enviado com sucesso!' if result else 'Erro ao enviar email')
"
```

## Vantagens do SendGrid

✅ **Confiabilidade:** 99.9% uptime
✅ **Escalabilidade:** Suporta milhões de emails
✅ **Rastreamento:** Abrir, clicar, bounce, spam
✅ **Templates:** Editor visual de templates
✅ **Webhooks:** Eventos em tempo real
✅ **Suporte:** Excelente suporte técnico
✅ **Preço:** Grátis até 100 emails/dia

## Monitoramento

Acesse o dashboard SendGrid para:
- Ver status de entrega
- Rastrear bounces e spam
- Analisar taxas de abertura/clique
- Gerenciar listas de contatos

## Fallback

Se a chave API não estiver configurada, os emails serão simulados (apenas logados).

---

**Status:** Pronto para configurar
**Próximo Passo:** Criar chave API no SendGrid e atualizar variáveis de ambiente
