#!/bin/bash

# =============================================
# LogiFlow CRM - Commit e Preparar Deploy
# =============================================

echo "🚀 LogiFlow CRM - Preparando Deploy para Render.com"
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Status do Git
echo -e "${BLUE}📊 Status atual do Git:${NC}"
git status
echo ""

# 2. Adicionar todos os arquivos
echo -e "${BLUE}📦 Adicionando arquivos ao Git...${NC}"
git add .
echo -e "${GREEN}✅ Arquivos adicionados!${NC}"
echo ""

# 3. Commit
echo -e "${BLUE}💾 Criando commit...${NC}"
read -p "Digite a mensagem do commit (ou pressione Enter para usar padrão): " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Deploy: LogiFlow CRM 100% Concluído - Ready for Production"
fi

git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✅ Commit criado!${NC}"
echo ""

# 4. Push para GitHub
echo -e "${BLUE}🌐 Enviando para GitHub...${NC}"
echo -e "${YELLOW}⚠️  Certifique-se de ter configurado o remote origin${NC}"
echo ""

read -p "Branch para push (padrão: main): " BRANCH
if [ -z "$BRANCH" ]; then
    BRANCH="main"
fi

git push origin $BRANCH

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Push realizado com sucesso!${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}🎉 CÓDIGO ATUALIZADO NO GITHUB!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${BLUE}📋 PRÓXIMOS PASSOS:${NC}"
    echo ""
    echo "1. Acesse: https://dashboard.render.com"
    echo "2. Clique em: New + → Blueprint"
    echo "3. Conecte seu repositório GitHub"
    echo "4. Selecione a branch: $BRANCH"
    echo "5. O Render detectará automaticamente o render.yaml"
    echo "6. Configure as variáveis de ambiente"
    echo "7. Clique em Apply"
    echo ""
    echo -e "${BLUE}📖 Documentação completa:${NC}"
    echo "   -> LogiFlow CRM/DEPLOY_RENDER.md"
    echo ""
    echo -e "${BLUE}🔗 URLs após deploy:${NC}"
    echo "   Frontend: https://logiflow-frontend.onrender.com"
    echo "   Backend:  https://logiflow-api.onrender.com"
    echo "   Docs:     https://logiflow-api.onrender.com/docs"
    echo ""
    echo -e "${GREEN}✅ Deploy automático iniciará após conectar no Render!${NC}"
    echo ""
else
    echo ""
    echo -e "${YELLOW}⚠️  Erro no push. Verifique:${NC}"
    echo "   1. Remote origin configurado?"
    echo "      git remote add origin <URL_DO_SEU_REPOSITORIO>"
    echo "   2. Credenciais do GitHub configuradas?"
    echo "   3. Branch existe no remoto?"
    echo ""
fi

