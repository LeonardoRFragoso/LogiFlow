# 🚨 GUIA DE REMEDIAÇÃO - CREDENCIAIS SMTP EXPOSTAS

## ⚠️ SITUAÇÃO

O GitHub detectou credenciais SMTP expostas no repositório `LeonardoRFragoso/LogiFlow`.

**Data da detecção:** 18 de Janeiro de 2026, 03:55:53 UTC  
**Tipo:** SMTP credentials  
**Repositório:** LeonardoRFragoso/LogiFlow

---

## 🔴 AÇÕES IMEDIATAS (CRÍTICAS - EXECUTAR AGORA)

### 1. **REVOGAR CREDENCIAIS EXPOSTAS**

Se você está usando Gmail/Google Workspace:

1. Acesse: https://myaccount.google.com/security
2. Vá em **Senhas de app**
3. **REVOGUE IMEDIATAMENTE** a senha que estava no código
4. Gere uma **nova senha de app** exclusiva para o LogiFlow

Se for outro provedor SMTP:
- Acesse o painel do provedor
- Troque a senha imediatamente
- Gere novas credenciais

⚠️ **NÃO PULE ESTE PASSO** - As credenciais antigas estão públicas!

---

### 2. **REMOVER CREDENCIAIS DO HISTÓRICO DO GIT**

O arquivo `.env` está no `.gitignore` agora, mas pode estar no histórico. Execute:

```powershell
# Navegue até o diretório do repositório
cd "C:\Users\leona\OneDrive\Documentos\Projetos\LogiFlow"

# Verificar se .env está no histórico
git log --all --full-history -- "*/.env" "**/.env" ".env"

# Se aparecer algo, precisamos limpar o histórico
```

#### Opção A: Usar BFG Repo-Cleaner (RECOMENDADO)

```powershell
# 1. Baixar BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# 2. Criar backup
git clone --mirror https://github.com/LeonardoRFragoso/LogiFlow.git logiflow-backup.git

# 3. Limpar arquivos .env do histórico
java -jar bfg.jar --delete-files ".env" logiflow-backup.git

# 4. Limpar referências
cd logiflow-backup.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Force push (CUIDADO - isso reescreve o histórico!)
git push --force
```

#### Opção B: Usar git filter-branch

```powershell
# AVISO: Isso reescreve TODO o histórico do Git
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch '*.env' 'LogiFlow CRM/backend/.env' 'LogiFlow CRM/.env'" \
  --prune-empty --tag-name-filter cat -- --all

# Limpar referências
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (reescreve histórico remoto)
git push origin --force --all
git push origin --force --tags
```

---

### 3. **ATUALIZAR .gitignore (JÁ ESTÁ CORRETO)**

Seu `.gitignore` já contém:
```
.env
.env.local
.env.*.local
```

✅ Isso está correto e impede novos commits de arquivos `.env`.

---

### 4. **CRIAR TEMPLATE DE .env (SEM CREDENCIAIS)**

```powershell
cd "LogiFlow CRM\backend"

# Criar .env.example com valores de exemplo
```

Conteúdo do `.env.example`:

```env
# Banco de Dados
DATABASE_URL=sqlite:///./logiflow.db
SQLALCHEMY_DATABASE_URI=sqlite:///./logiflow.db

# Segurança
SECRET_KEY=sua-chave-secreta-aqui-gere-uma-nova
JWT_SECRET_KEY=sua-chave-jwt-aqui-gere-uma-nova

# Email SMTP - SUBSTITUIR COM VALORES REAIS
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=gere-uma-senha-de-app-no-google
FROM_EMAIL=noreply@logiflow.com.br
FROM_NAME=LogiFlow CRM
SALES_EMAIL=vendas@logiflow.com.br

# Aplicação
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

### 5. **RECRIAR SEU .env LOCAL COM NOVAS CREDENCIAIS**

```powershell
# Copiar o template
cd "LogiFlow CRM\backend"
Copy-Item .env.example .env

# Editar .env e adicionar as NOVAS credenciais
notepad .env
```

---

### 6. **NOTIFICAR O GITHUB (FECHAR O ALERTA)**

Depois de:
1. ✅ Revogar credenciais antigas
2. ✅ Limpar histórico do Git
3. ✅ Criar novas credenciais
4. ✅ Atualizar .env local

Clique no botão **"Fix This Secret Leak"** no email do GitHub.

---

## 📋 CHECKLIST DE SEGURANÇA

- [ ] Revogadas as credenciais SMTP antigas
- [ ] Geradas novas credenciais SMTP
- [ ] Verificado histórico do Git para arquivos .env
- [ ] Limpado histórico do Git (se necessário)
- [ ] Force push executado (se histórico foi limpo)
- [ ] Arquivo .env.example criado (sem credenciais)
- [ ] Arquivo .env local atualizado com novas credenciais
- [ ] Testado que a aplicação funciona com novas credenciais
- [ ] Alerta do GitHub fechado
- [ ] Equipe notificada sobre o incidente (se aplicável)

---

## 🔐 BOAS PRÁTICAS PARA O FUTURO

1. **NUNCA commitar arquivos .env**
   - Sempre verificar antes de fazer commit: `git status`
   - Usar `.env.example` com valores dummy

2. **Usar variáveis de ambiente em produção**
   - Render, Heroku, AWS: usar variáveis de ambiente do painel
   - Nunca armazenar credenciais em código

3. **Rotação regular de credenciais**
   - Trocar senhas a cada 90 dias
   - Usar senhas únicas por ambiente (dev/staging/prod)

4. **Monitoramento**
   - Habilitar GitHub Secret Scanning (já está ativo)
   - Considerar ferramentas como GitGuardian

5. **Usar git-secrets**
   ```powershell
   # Prevenir commits com credenciais
   git clone https://github.com/awslabs/git-secrets.git
   cd git-secrets
   # Seguir instruções de instalação
   ```

---

## 📞 SUPORTE

Se precisar de ajuda:
- GitHub Support: https://support.github.com
- Documentação Git: https://git-scm.com/docs

---

**IMPORTANTE:** Trate isso com **MÁXIMA PRIORIDADE**. Credenciais expostas podem ser usadas para:
- Envio de spam/phishing
- Custos inesperados
- Comprometimento de contas de clientes
- Danos à reputação

**Tempo estimado para remediar:** 30-60 minutos
