# LogiFlow CRM - Documentation Index

> Central de documentação técnica do projeto

## 📁 Estrutura da Documentação

### 🏗️ Arquitetura
- [C4 Context Diagram](architecture/c4-context.md) - Visão geral do sistema
- [C4 Container Diagram](architecture/c4-container.md) - Containers e tecnologias
- [C4 Component Diagram](architecture/c4-component.md) - Componentes internos
- [Data Flow Diagram](architecture/data-flow.md) - Fluxos de dados
- [Clean Architecture Layers](architecture/layers.md) - Camadas da arquitetura

### 📋 ADRs (Architecture Decision Records)
- [ADR-001](adr/ADR-001-integracao-suitecrm.md) - Integração SuiteCRM (Obsoleta)
- [ADR-002](adr/ADR-002-fastapi-backend.md) - Escolha do FastAPI
- [ADR-003](adr/ADR-003-postgresql-database.md) - Escolha do PostgreSQL
- [ADR-004](adr/ADR-004-jwt-authentication.md) - Autenticação JWT
- [ADR-005](adr/ADR-005-clean-architecture.md) - Clean Architecture
- [ADR-006](adr/ADR-006-project-structure.md) - Estrutura do Projeto

### 🎨 Design Patterns
- [Repository Pattern](patterns/repository.md)
- [Dependency Injection](patterns/dependency-injection.md)
- [DTO Pattern](patterns/dto.md)
- [Factory Pattern](patterns/factory.md)
- [Strategy Pattern](patterns/strategy.md)

### 🔌 API
- [Getting Started](api/getting-started.md) - Quick start da API
- [Endpoints Reference](api/endpoints.md) - Todos os endpoints

### 📊 Análise
- [Current State](analysis/current-state.md) - Análise do estado atual

### 🚀 Deployment
- [Local Development](deployment/local.md) - Setup local
- [Production](deployment/production.md) - Deploy em produção
- [Docker Guide](deployment/docker.md) - Guia de Docker

### 🔒 Segurança
- [OWASP Checklist](security/owasp-checklist.md) - Checklist de segurança
- [Secrets Management](security/secrets.md) - Gerenciamento de secrets

### 💻 Desenvolvimento
- [Code Standards](development/code-standards.md) - Padrões de código

### 📈 Observabilidade
- [Monitoring Guide](observability/monitoring.md) - Logs, métricas e alertas

### ⚙️ CI/CD
- [CI/CD Pipeline](guides/ci-cd.md) - GitHub Actions e deploy

---

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

**Última atualização:** 26/01/2026  
**Versão:** 2.0.0
