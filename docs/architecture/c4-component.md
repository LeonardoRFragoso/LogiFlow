# C4 - Component Diagram (Nível 3)

## Backend API (FastAPI)

```mermaid
flowchart TB
  subgraph API["Backend API (FastAPI)"]
    main["main.py\nApp bootstrap + middleware + routers"]

    subgraph routers["Presentation: routers/*"]
      r_auth["auth router\n/login, refresh, users"]
      r_tenants["tenants router\n(tenant lifecycle)"]
      r_fiscal["fiscal router\n(CT-e/MDF-e endpoints)"]
      r_billing["billing router\n(planos/assinaturas)"]
      r_operacional["cotacoes/pedidos/entregas\n(operacional)"]
      r_gps["gps_tracking + gps_self_service"]
      r_whats["whatsapp router"]
      r_erp["erp router"]
      r_dashboard["dashboard router"]
    end

    subgraph middleware["Cross-cutting: middleware/*"]
      m_tenant["TenantMiddleware\nresolve tenant"]
      m_rate["RateLimitMiddleware"]
      m_corr["Correlation middleware"]
      m_rbac["RBAC helpers + audit"]
    end

    subgraph app_services["Application: services/*"]
      s_integration["integration_manager\nresolve credenciais por tenant"]
      s_fiscal["fiscal_service\nregras fiscais + integração"]
      s_mp["mercadopago_service\ncheckout/webhooks"]
      s_whats["whatsapp_service\nmensagens/notificações"]
      s_scheduler["scheduler\nagendamentos"]
      s_cache["cache_service"]
      s_crypto["encryption_service"]
      s_erp_sync["erp_sync"]
    end

    subgraph infra["Infrastructure"]
      db_layer["database.py\nengine + session"]
      orm["models.py / models/*\nSQLAlchemy Models"]
      integ_focus["integrations/fiscal/focusnfe.py"]
      integ_maps["integrations/maps/*"]
      integ_gps["integrations/gps/*"]
      integ_erp["integrations/erp/*"]
    end

    main --> middleware
    main --> routers

    routers --> app_services
    routers --> db_layer
    routers --> orm

    m_tenant --> routers

    r_fiscal --> s_integration
    r_fiscal --> s_fiscal
    s_fiscal --> integ_focus

    r_billing --> s_mp

    r_whats --> s_whats
    s_whats --> integ_erp

    r_erp --> s_erp_sync
    s_erp_sync --> integ_erp

    r_gps --> integ_gps

    s_cache --> redis_ext[("Redis")]
    db_layer --> db_ext[("Database")]
  end
```

## Observações

- Os componentes acima representam a **estrutura real atual** (módulos existentes no repositório).
- Alguns routers ainda possuem lógica e persistência “simulada” em memória; isso será alvo de refatoração nas próximas fases.
