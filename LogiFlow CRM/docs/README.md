# Documentação LogiFlow CRM

## 📚 Guia Completo de Uso

O guia completo do LogiFlow CRM está disponível em formato PDF e HTML.

### 🔗 Como Acessar

#### Opção 1: Via Frontend (Recomendado)
1. Acesse o sistema: http://localhost:3000
2. Vá em **FAQ** no menu
3. Clique no botão **"📄 Baixar Guia"**
4. O PDF será baixado automaticamente

#### Opção 2: Via API Backend
- **Endpoint:** http://localhost:8000/download/guia-completo
- **Método:** GET
- **Resposta:** Arquivo PDF para download

#### Opção 3: Arquivo Estático
- **Frontend:** `/frontend/public/guia-completo-logiflow.pdf`
- **Backend:** `/backend/static/guia-completo-logiflow.pdf`
- **Docs:** `/docs/guia-completo-logiflow.pdf`

#### Opção 4: HTML (Para Visualização)
- Abra o arquivo: `/docs/guia-completo-logiflow.html` no navegador
- Para gerar PDF: Ctrl+P > Salvar como PDF

---

## 📖 Conteúdo do Guia

O guia completo contém **14 capítulos** cobrindo:

1. **Introdução** - Visão geral do sistema
2. **Visão Geral** - Componentes e funcionalidades
3. **Fluxo de Funcionamento** - Ciclo completo de uma entrega
4. **Gestão de Pedidos** - Criar, atribuir e acompanhar
5. **Cotações de Frete** - Criar e converter cotações
6. **Gestão de Motoristas** - Cadastro e avaliação
7. **Gestão de Veículos** - Controle da frota
8. **Ocorrências e Incidentes** - Registro e resolução
9. **Rastreamento em Tempo Real** - GPS e localização
10. **App do Motorista** - Uso do aplicativo móvel
11. **Portal do Cliente** - Acesso para clientes
12. **Relatórios e Análises** - Dashboards e KPIs
13. **Configurações do Sistema** - Personalização
14. **Suporte e Contato** - Ajuda e contatos

---

## 🎯 Outros Recursos de Ajuda

### Tour Virtual
- Acesse o sistema pela primeira vez
- O tour inicia automaticamente
- Ou clique em "Iniciar Tour" no FAQ

### FAQ
- Acesse: http://localhost:3000/faq
- 15+ perguntas e respostas
- Sistema de busca
- Filtros por categoria

### Vídeos Tutoriais (Em breve)
- Visão geral do sistema
- Cadastro de clientes
- Criando cotações
- Acompanhando entregas

---

## 📞 Suporte

**Email:** suporte@logiflow.com  
**WhatsApp:** (21) 99999-9999  
**Documentação:** http://localhost:3000/faq

---

## 📝 Notas Técnicas

### Localização dos Arquivos

```
LogiFlow CRM/
├── docs/
│   ├── guia-completo-logiflow.html  # Versão HTML
│   ├── guia-completo-logiflow.pdf   # Versão PDF
│   └── README.md                     # Este arquivo
├── backend/
│   └── static/
│       └── guia-completo-logiflow.pdf  # Servido pela API
└── frontend/
    └── public/
        └── guia-completo-logiflow.pdf  # Servido pelo frontend
```

### Endpoints da API

```
GET /download/guia-completo
- Retorna: PDF do guia completo
- Content-Type: application/pdf
- Filename: LogiFlow-CRM-Guia-Completo.pdf
```

### Atualização do Guia

Para atualizar o guia:
1. Edite o arquivo HTML: `docs/guia-completo-logiflow.html`
2. Gere novo PDF (Ctrl+P > Salvar como PDF)
3. Substitua os PDFs nas 3 localizações
4. Commit e push para o repositório

---

**Última atualização:** 13/12/2024  
**Versão:** 1.0.0
