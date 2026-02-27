# 🔄 ATUALIZAR GITHUB - render.yaml na Raiz

## ⚠️ **PROBLEMA**
O arquivo `render.yaml` estava dentro de `LogiFlow CRM/`, mas o Render precisa dele na **raiz do repositório**.

## ✅ **SOLUÇÃO**

Copiei o arquivo para a raiz. Agora você precisa commitar e fazer push!

---

## 📝 **COMANDOS PARA COPIAR E COLAR**

Abra o **PowerShell** e execute:

```powershell
# 1. Ir para o diretório
cd "C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM"

# 2. Adicionar o novo arquivo render.yaml (na raiz)
git add render.yaml

# 3. Commit
git commit -m "Fix: Mover render.yaml para raiz do repositório"

# 4. Push
git push origin main
```

---

## ⏱️ **DEPOIS DO PUSH**

1. Volte para o Render
2. Clique em **"Retry"** (botão na tela)
3. O Render encontrará o `render.yaml` agora!
4. Deploy iniciará automaticamente

---

## 🎯 **ALTERNATIVA: SCRIPT RÁPIDO**

Execute este comando único:

```powershell
cd "C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM"; git add render.yaml; git commit -m "Fix: Mover render.yaml para raiz"; git push origin main
```

---

**Após o push, clique em "Retry" no Render!** 🔄

