# LogiFlow CRM

**CRM SaaS especializado para Transportadoras e Logística**

[![Python](https://img.shields.io/badge/Python-47.3%25-blue)](/)
[![Vue](https://img.shields.io/badge/Vue-29.3%25-green)](/)
[![PHP](https://img.shields.io/badge/PHP-17.3%25-purple)](/)

---

## Visão Geral

LogiFlow é um CRM brasileiro que une **gestão comercial, operacional e fiscal** para transportadoras em uma única plataforma, com emissão de CT-e/MDF-e integrada e rastreamento em tempo real.

### Proposta de Valor

- **Tudo em um só lugar** - Elimina 3-4 sistemas separados (CRM + TMS + Emissor fiscal + Rastreamento)
- **Preço acessível** - 60-70% mais barato que soluções enterprise
- **Setup em 48h** - Sem projetos de meses; cliente opera em 2 dias
- **Sem contrato de fidelidade** - Pagamento mensal

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Vue 3)                      │
│                 SPA - Single Page Application            │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────┐
│               BACKEND ORQUESTRADOR (FastAPI)             │
│     Autenticação │ Billing │ Regras de Negócio │ Cache  │
└───────────────────────────┬─────────────────────────────┘
                            │ API V8 (JSON:API)
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     SUITECRM 8.x                         │
│     Módulos Custom │ ACL │ Workflows │ Logic Hooks      │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   BANCO DE DADOS (MariaDB)               │
└─────────────────────────────────────────────────────────┘
```

---

## Estrutura do Projeto

```
LogiFlow CRM/
├── backend/           # FastAPI - Orquestrador Python
├── frontend/          # Vue 3 + Vite + TailwindCSS
├── suitecrm/          # SuiteCRM 8.x com módulos custom
├── docker/            # Configurações Docker
├── scripts/           # Scripts de provisioning e migração
├── templates/         # Templates de importação de dados
├── docs/              # Documentação
└── docker-compose.yml # Orquestração dos serviços
```

---

## Módulos Custom

| Módulo | Descrição |
|--------|-----------|
| **Cotações** | Cotações de frete com cálculo automático |
| **PedidosFrete** | Pedidos confirmados e gestão operacional |
| **Entregas** | Rastreamento e status de entregas |
| **Motoristas** | Cadastro com controle de CNH |
| **Veículos** | Gestão de frota e manutenção |
| **Ocorrências** | Registro de avarias, atrasos, etc. |

---

## Tecnologias

- **Frontend:** Vue 3, Vite, Pinia, Vue Router, TailwindCSS
- **Backend:** FastAPI, Python 3.11, Redis, Celery
- **CRM Base:** SuiteCRM 8.x (PHP 8.0, Symfony)
- **Banco de Dados:** MariaDB 10.6
- **Infraestrutura:** Docker, Nginx

---

## Quick Start

```bash
# Clone o repositório
git clone https://github.com/LeonardoRFragoso/LogiFlow.git
cd LogiFlow/LogiFlow\ CRM

# Copie o arquivo de ambiente
cp .env.example .env

# Suba os containers
docker-compose up -d

# Acesse
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# SuiteCRM: http://localhost:8080
```

---

## Integrações Planejadas

- **CT-e / MDF-e** - Emissão de documentos fiscais (Focus NFe)
- **WhatsApp** - Notificações via Evolution API
- **ERPs** - Omie, Bling, Tiny
- **Rastreamento GPS** - App PWA do motorista

---

## Documentação

- [Arquitetura](LogiFlow%20CRM/ARCHITECTURE.md)
- [Guia de Início Rápido](LogiFlow%20CRM/docs/GUIA_INICIO_RAPIDO.md)
- [Status Atual](LogiFlow%20CRM/STATUS_ATUAL.md)

---

## Licença

Projeto proprietário - Todos os direitos reservados.

---

**LogiFlow CRM** - *Sua transportadora no controle. Do comercial à entrega.*
