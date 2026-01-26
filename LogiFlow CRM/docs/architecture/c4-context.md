# LogiFlow CRM - C4 Model: Context Diagram (Nível 1)

> **Versão:** 1.0.0  
> **Atualizado:** Janeiro 2026

## Descrição

O Diagrama de Contexto mostra o sistema LogiFlow CRM e suas interações com usuários e sistemas externos. Este é o nível mais alto de abstração do C4 Model.

---

## Diagrama

```mermaid
C4Context
    title Sistema LogiFlow CRM - Diagrama de Contexto

    Person(admin, "Administrador", "Gerencia configurações, usuários e planos")
    Person(operador, "Operador", "Gerencia cotações, pedidos e entregas")
    Person(motorista, "Motorista", "Registra entregas e envia localização GPS")
    Person(cliente_final, "Cliente Final", "Acompanha entregas e solicita cotações")

    System(logiflow, "LogiFlow CRM", "Sistema de CRM especializado para transportadoras")

    System_Ext(whatsapp, "WhatsApp Business API", "Envio de notificações e chatbot")
    System_Ext(mercadopago, "MercadoPago", "Processamento de pagamentos e assinaturas")
    System_Ext(focusnfe, "Focus NFe", "Emissão de CT-e, MDF-e e NF-e")
    System_Ext(melhor_envio, "Melhor Envio", "Cotação de fretes com múltiplas transportadoras")
    System_Ext(google_maps, "Google Maps API", "Geocodificação e cálculo de rotas")
    System_Ext(smtp, "Servidor SMTP", "Envio de e-mails transacionais")

    Rel(admin, logiflow, "Configura e gerencia", "HTTPS")
    Rel(operador, logiflow, "Opera diariamente", "HTTPS")
    Rel(motorista, logiflow, "Atualiza entregas", "HTTPS/App")
    Rel(cliente_final, logiflow, "Acompanha pedidos", "HTTPS/Portal")

    Rel(logiflow, whatsapp, "Envia mensagens", "REST API")
    Rel(logiflow, mercadopago, "Processa pagamentos", "REST API")
    Rel(logiflow, focusnfe, "Emite documentos fiscais", "REST API")
    Rel(logiflow, melhor_envio, "Consulta cotações", "REST API")
    Rel(logiflow, google_maps, "Calcula rotas", "REST API")
    Rel(logiflow, smtp, "Envia e-mails", "SMTP/TLS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

---

## Visão Alternativa (Flowchart)

```mermaid
flowchart TB
    subgraph Usuarios["👥 Usuários"]
        ADMIN["🔧 Administrador<br/>Gerencia sistema"]
        OPERADOR["📋 Operador<br/>Operações diárias"]
        MOTORISTA["🚛 Motorista<br/>App mobile"]
        CLIENTE["👤 Cliente Final<br/>Portal web"]
    end

    subgraph LogiFlow["🏢 LogiFlow CRM"]
        SISTEMA["Sistema LogiFlow CRM<br/>━━━━━━━━━━━━━━━<br/>CRM especializado para<br/>transportadoras com<br/>multi-tenancy"]
    end

    subgraph Externos["🌐 Sistemas Externos"]
        WA["📱 WhatsApp<br/>Business API"]
        MP["💳 MercadoPago<br/>Pagamentos"]
        NFE["📄 Focus NFe<br/>Documentos Fiscais"]
        ME["📦 Melhor Envio<br/>Cotação Fretes"]
        MAPS["🗺️ Google Maps<br/>Rotas e Geo"]
        EMAIL["📧 SMTP<br/>E-mails"]
    end

    ADMIN -->|"Configura<br/>HTTPS"| SISTEMA
    OPERADOR -->|"Opera<br/>HTTPS"| SISTEMA
    MOTORISTA -->|"Atualiza<br/>App/HTTPS"| SISTEMA
    CLIENTE -->|"Acompanha<br/>Portal/HTTPS"| SISTEMA

    SISTEMA -->|"REST API"| WA
    SISTEMA -->|"REST API"| MP
    SISTEMA -->|"REST API"| NFE
    SISTEMA -->|"REST API"| ME
    SISTEMA -->|"REST API"| MAPS
    SISTEMA -->|"SMTP/TLS"| EMAIL

    style SISTEMA fill:#1168bd,stroke:#0b4884,color:#fff
    style Usuarios fill:#f5f5f5,stroke:#999
    style Externos fill:#f5f5f5,stroke:#999
```

---

## Descrição dos Elementos

### Usuários (Pessoas)

| Ator | Descrição | Interação Principal |
|------|-----------|---------------------|
| **Administrador** | Responsável por configurar o sistema, gerenciar usuários, planos e integrações | Painel administrativo via web |
| **Operador** | Usuário do dia-a-dia que gerencia cotações, pedidos, entregas e clientes | CRM Frontend via web |
| **Motorista** | Profissional que realiza as entregas e reporta localização GPS | App mobile dedicado |
| **Cliente Final** | Pessoa física ou jurídica que acompanha suas entregas | Portal do cliente via web |

### Sistema Principal

| Sistema | Descrição | Tecnologias |
|---------|-----------|-------------|
| **LogiFlow CRM** | Sistema de CRM SaaS multi-tenant especializado para transportadoras e empresas de logística | FastAPI, Vue.js 3, PostgreSQL, Redis |

### Sistemas Externos

| Sistema | Propósito | Tipo de Integração |
|---------|-----------|-------------------|
| **WhatsApp Business API** | Envio de notificações automáticas, chatbot para atendimento | REST API (Evolution API) |
| **MercadoPago** | Processamento de pagamentos de assinaturas e checkout | REST API + Webhooks |
| **Focus NFe** | Emissão de documentos fiscais (CT-e, MDF-e, NF-e) | REST API |
| **Melhor Envio** | Cotação automática com múltiplas transportadoras | REST API |
| **Google Maps API** | Geocodificação de endereços e cálculo de rotas | REST API |
| **Servidor SMTP** | Envio de e-mails transacionais e notificações | SMTP com TLS |

---

## Fluxos de Comunicação

### Entrada de Dados
```
Usuários → LogiFlow CRM (HTTPS/REST)
├── Administrador: Configurações, usuários, planos
├── Operador: Cotações, pedidos, clientes
├── Motorista: Status entregas, localização GPS
└── Cliente: Solicitações, aprovações
```

### Saída para Sistemas Externos
```
LogiFlow CRM → Sistemas Externos (REST/SMTP)
├── WhatsApp: Notificações em tempo real
├── MercadoPago: Cobrança de assinaturas
├── Focus NFe: Emissão fiscal
├── Melhor Envio: Cotações de frete
├── Google Maps: Geocodificação
└── SMTP: E-mails transacionais
```

---

## Requisitos de Segurança

| Comunicação | Protocolo | Autenticação |
|-------------|-----------|--------------|
| Usuários → LogiFlow | HTTPS (TLS 1.3) | JWT Tokens |
| LogiFlow → WhatsApp | HTTPS | API Key |
| LogiFlow → MercadoPago | HTTPS | OAuth + Access Token |
| LogiFlow → Focus NFe | HTTPS | API Token |
| LogiFlow → Melhor Envio | HTTPS | Bearer Token |
| LogiFlow → Google Maps | HTTPS | API Key |
| LogiFlow → SMTP | SMTP/TLS | Username/Password |

---

## Observações

1. **Multi-Tenancy**: Cada transportadora (tenant) tem seus dados isolados
2. **SaaS Model**: Sistema oferecido como serviço com diferentes planos
3. **APIs RESTful**: Todas as integrações utilizam REST com JSON
4. **Webhooks**: MercadoPago utiliza webhooks para notificações de pagamento

---

*Documento parte da documentação arquitetural do LogiFlow CRM - Modelo C4*
