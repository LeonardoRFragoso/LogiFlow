# 🔧 Limpar Campos de Configuração no Railway

## ❌ Campos que Precisam Ser Limpos

Você encontrou os três campos problemáticos. Todos eles tentam fazer `cd "LogiFlow CRM/backend"` o que não funciona no Railway.

### Campo 1: Custom Build Command
**Atual:**
```
cd "LogiFlow CRM/backend"pip install --upgrade pippip install -r requirements.txt
```

**Ação:** Delete completamente e deixe vazio

---

### Campo 2: Pre-deploy Command
**Atual:**
```
/bin/sh -c "exec cd "LogiFlow CRM/backend"alembic upgrade head || echo "Migration skipped or failed - will retry on next deploy""
```

**Ação:** Delete completamente e deixe vazio

---

### Campo 3: Custom Start Command
**Atual:**
```
cd "LogiFlow CRM/backend"uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Ação:** Delete completamente e deixe vazio

---

## ✅ Passo-a-Passo

Para cada um dos 3 campos acima:

1. **Clique no campo de texto**
2. **Selecione todo o conteúdo:**
   - Windows/Linux: `Ctrl+A`
   - Mac: `Cmd+A`
3. **Delete o conteúdo:**
   - Pressione `Delete` ou `Backspace`
4. **Verifique que o campo está vazio**
5. **Clique em Save** (se houver botão)

---

## 🚀 Depois de Limpar

Após limpar os três campos:

1. **Clique em Redeploy** para forçar um novo deploy
2. O Railway agora usará apenas o `Procfile` que está correto:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

---

## ✨ Resultado Esperado

O deploy agora deve:
- ✅ Instalar dependências Python corretamente
- ✅ **NÃO** tentar fazer `cd`
- ✅ **NÃO** tentar executar `alembic upgrade head`
- ✅ Iniciar o uvicorn corretamente
- ✅ Serviço ficar **Online**

---

**Status:** Aguardando você limpar os campos no Dashboard
