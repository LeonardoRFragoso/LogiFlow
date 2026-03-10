"""
LogiFlow CRM - FastAPI Backend
================================
API principal para orquestração do LogiFlow CRM
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import redis
import os
from loguru import logger
from pathlib import Path

from config import settings
from database import init_db
from middleware.correlation import correlation_middleware
from middleware.tenant import TenantMiddleware

# Importar novos routers v2 (Clean Architecture)
try:
    from presentation.api import clientes_router as clientes_v2
    from presentation.api import cotacoes_router as cotacoes_v2
    from presentation.api import pedidos_router as pedidos_v2
    V2_ROUTERS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Routers v2 não disponíveis: {e}")
    V2_ROUTERS_AVAILABLE = False
    clientes_v2 = cotacoes_v2 = pedidos_v2 = None

# Importar routers
try:
    from routers import (
        fiscal,
        rastreamento,
        cotacoes,
        pedidos,
        motoristas,
        veiculos,
        auth,
        whatsapp,
        maps,
        demo,
        ocorrencias,
        leads,
        billing,
        tenants,
        erp,
        melhor_envio,
        health_score,
        nps,
        cotacao_automatica,
        gps_tracking,
        gps_self_service,
        # integrations_self_service,  # Comentado temporariamente
        tenant_credentials,
        plan_info,
        clientes,
        entregas,
        dashboard,
        features,  # Feature Flags para BETA
        crm_enterprise,  # CRM Enterprise nativo - ÚNICO CRM
    )
    from routers.admin import quota_router
except ImportError as e:
    print(f"WARNING: Erro ao importar routers: {e}")
    fiscal = None
    rastreamento = None
    cotacoes = None
    pedidos = None
    motoristas = None
    veiculos = None
    auth = None
    whatsapp = None
    maps = None
    demo = None
    ocorrencias = None
    leads = None
    billing = None
    tenants = None
    erp = None
    melhor_envio = None
    health_score = None
    nps = None
    cotacao_automatica = None
    gps_tracking = None
    gps_self_service = None
    tenant_credentials = None
    plan_info = None
    clientes = None
    entregas = None
    dashboard = None
    features = None
    quota_router = None
    crm_enterprise = None

# Configurar logging
logger.add(
    "logs/api_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    # Startup
    logger.info("Iniciando LogiFlow API...")
    
    # Testar conexão Redis
    try:
        redis_config = settings.get_redis_config()
        redis_client = redis.Redis(**redis_config)
        redis_client.ping()
        logger.info("Redis conectado com sucesso")
        app.state.redis = redis_client
    except Exception as e:
        logger.warning(f"Redis não disponível: {e}. Continuando sem cache...")
        app.state.redis = None

    # Garantir que as tabelas do banco existam
    try:
        init_db()
        logger.info("Banco inicializado (init_db).")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco: {e}")
    
    # Criar usuário admin padrão se não existir
    try:
        from routers.auth import criar_usuario_admin_se_necessario
        criar_usuario_admin_se_necessario()
    except Exception as e:
        logger.warning(f"Não foi possível criar admin: {e}")
    
    # Inicializar monitoramento de quotas
    try:
        from utils.quota_monitor import init_quota_monitoring
        init_quota_monitoring()
        logger.info("Monitoramento de quotas inicializado")
    except Exception as e:
        logger.error(f"Erro ao inicializar quota monitoring: {e}")
    
    # Inicializar agendador de pesquisas automáticas (NPS/CSAT)
    try:
        from services.scheduler import start_scheduler, stop_scheduler
        start_scheduler()
        logger.info("Agendador de pesquisas automáticas inicializado")
        app.state.scheduler_active = True
    except Exception as e:
        logger.error(f"Erro ao inicializar scheduler: {e}")
        app.state.scheduler_active = False
    
    # CRM Enterprise é o único sistema de CRM nativo
    
    logger.info("LogiFlow API iniciada com sucesso!")
    
    yield
    
    # Shutdown
    # Parar agendador
    if hasattr(app.state, 'scheduler_active') and app.state.scheduler_active:
        try:
            from services.scheduler import stop_scheduler
            stop_scheduler()
            logger.info("Agendador parado")
        except Exception as e:
            logger.error(f"Erro ao parar scheduler: {e}")
    logger.info("Encerrando LogiFlow API...")
    if hasattr(app.state, 'redis'):
        app.state.redis.close()


# Criar aplicação FastAPI
docs_base = f"{settings.API_PREFIX.rstrip('/')}/{settings.API_VERSION}".rstrip("/")
app = FastAPI(
    title="LogiFlow CRM API",
    description="API de orquestração para o LogiFlow CRM - Sistema especializado para Transportadoras",
    version="1.0.0",
    docs_url=f"{docs_base}/docs" if settings.DEBUG else None,
    redoc_url=f"{docs_base}/redoc" if settings.DEBUG else None,
    openapi_url=f"{docs_base}/openapi.json",
    lifespan=lifespan
)

# Configurar CORS
from middleware.cors_security import setup_cors
setup_cors(app)

# Middleware de Tenant (Multi-Tenancy)
app.add_middleware(TenantMiddleware)

# Rate Limiting
from middleware.rate_limit import RateLimitMiddleware
from middleware.rate_limiter import limiter, setup_rate_limiter
app.add_middleware(RateLimitMiddleware)
setup_rate_limiter(app)
app.state.limiter = limiter

# Prometheus Metrics
from middleware.prometheus import PrometheusMiddleware, get_metrics

def setup_prometheus_metrics(app):
    """Setup Prometheus middleware"""
    app.add_middleware(PrometheusMiddleware, group_paths=True)

setup_prometheus_metrics(app)

# Correlation ID
app.middleware("http")(correlation_middleware)


# ===========================================
# Prefixos e Routers
# ===========================================
api_prefix = f"{settings.API_PREFIX.rstrip('/')}/{settings.API_VERSION}".rstrip("/")
api_router = APIRouter(prefix=api_prefix)


def include_router_with_version(router_module, prefix: str = "", tags=None):
    """Inclui router na rota legada e na rota versionada /api/{version}."""
    if not router_module:
        return
    router_obj = getattr(router_module, "router", None)
    if not router_obj:
        return
    app.include_router(router_obj, prefix=prefix, tags=tags)
    api_router.include_router(router_obj, prefix=prefix, tags=tags)


include_router_with_version(fiscal, prefix="/fiscal", tags=["Fiscal"])
include_router_with_version(rastreamento, prefix="/rastreamento", tags=["Rastreamento"])
include_router_with_version(cotacoes, prefix="/cotacoes", tags=["Cotações"])
include_router_with_version(pedidos, prefix="/pedidos", tags=["Pedidos"])
include_router_with_version(motoristas, prefix="/motoristas", tags=["Motoristas"])
include_router_with_version(veiculos, prefix="/veiculos", tags=["Veículos"])
include_router_with_version(auth, prefix="/auth", tags=["Autenticação"])
include_router_with_version(whatsapp, prefix="/whatsapp", tags=["WhatsApp"])
include_router_with_version(maps, prefix="/maps", tags=["Google Maps"])
include_router_with_version(cases)
include_router_with_version(demo)
include_router_with_version(ocorrencias, prefix="/ocorrencias", tags=["Ocorrências"])
include_router_with_version(leads)
include_router_with_version(billing)
include_router_with_version(tenants, prefix="/api/tenants", tags=["Tenants"])
include_router_with_version(erp, prefix="/erp", tags=["Integrações ERP"])
include_router_with_version(melhor_envio, prefix="/melhor-envio", tags=["Melhor Envio"])
include_router_with_version(health_score, prefix="/customer-success", tags=["Health Score & CS"])
include_router_with_version(nps, prefix="/satisfacao", tags=["NPS & CSAT"])
include_router_with_version(cotacao_automatica, prefix="/cotacao-automatica", tags=["Cotação Automática"])
include_router_with_version(gps_tracking, prefix="/gps", tags=["Rastreamento GPS"])
include_router_with_version(gps_self_service, prefix="/gps-config", tags=["Configuração GPS Self-Service"])
# Router temporariamente comentado para deploy (opcional, não crítico)
# include_router_with_version(integrations_self_service, prefix="/integrations-config", tags=["Configuração de Integrações Self-Service"])
include_router_with_version(tenant_credentials, prefix="/tenant-credentials", tags=["Tenant Credentials"])
# plan_info já define /plans internamente; manter prefixo vazio evita caminhos duplicados
include_router_with_version(plan_info, prefix="", tags=["Planos"])
include_router_with_version(clientes, prefix="/clientes", tags=["Clientes"])
include_router_with_version(entregas, prefix="/entregas", tags=["Entregas"])
include_router_with_version(dashboard, prefix="/dashboard", tags=["Dashboard"])
include_router_with_version(features, prefix="", tags=["Feature Flags"])
include_router_with_version(crm_enterprise, prefix="", tags=["CRM Enterprise"])

# ===========================================
# Routers v2 - Clean Architecture
# ===========================================
if V2_ROUTERS_AVAILABLE:
    if clientes_v2:
        app.include_router(clientes_v2)
        api_router.include_router(clientes_v2)
    if cotacoes_v2:
        app.include_router(cotacoes_v2)
        api_router.include_router(cotacoes_v2)
    if pedidos_v2:
        app.include_router(pedidos_v2)
        api_router.include_router(pedidos_v2)
    logger.info("Routers v2 (Clean Architecture) carregados")

# Admin routers (protegidos por RBAC)
include_router_with_version(quota_router, prefix="/admin", tags=["Admin - Quotas"])

app.include_router(api_router)


# ===========================================
# Healthcheck
# ===========================================
@app.get("/health", tags=["Health"])
@api_router.get("/health", tags=["Health"])
async def healthcheck(request: Request):
    """Healthcheck simples (liveness) + verificação de Redis quando disponível."""
    redis_ok = False
    try:
        redis_client = getattr(request.app.state, "redis", None)
        if redis_client:
            redis_client.ping()
            redis_ok = True
    except Exception as e:
        logger.warning(f"Healthcheck Redis falhou: {e}")
    
    return {
        "status": "ok",
        "redis": redis_ok
    }


@app.get("/ready", tags=["Health"])
@api_router.get("/ready", tags=["Health"])
async def readiness(request: Request):
    """Readiness check básico."""
    redis_ok = False
    try:
        redis_client = getattr(request.app.state, "redis", None)
        if redis_client:
            redis_client.ping()
            redis_ok = True
    except Exception as e:
        logger.error(f"Readiness Redis falhou: {e}")
    
    status = "ready" if redis_ok else "degraded"
    return {
        "status": status,
        "redis": redis_ok
    }


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Expõe métricas Prometheus"""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(get_metrics())


# ===========================================
# Exception Handlers
# ===========================================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação do Pydantic"""
    body = await request.body()
    logger.error(f"❌ Erro de validação na requisição {request.method} {request.url.path}")
    logger.error(f"📦 Body recebido: {body.decode('utf-8')}")
    logger.error(f"🔍 Erros de validação: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Erro de validação dos dados",
            "details": exc.errors(),
            "status_code": 422
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Erro interno do servidor",
            "status_code": 500
        }
    )


# ===========================================
# Arquivos Estáticos
# ===========================================
# Montar pasta static para servir arquivos
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/download/guia-completo")
async def download_guia():
    """Download do guia completo em PDF"""
    pdf_path = static_path / "guia-completo-logiflow.pdf"
    if pdf_path.exists():
        return FileResponse(
            path=str(pdf_path),
            filename="LogiFlow-CRM-Guia-Completo.pdf",
            media_type="application/pdf"
        )
    raise HTTPException(status_code=404, detail="Guia não encontrado")


# ===========================================
# Root Endpoint
# ===========================================
@app.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    return {
        "name": "LogiFlow CRM API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.DEBUG else "disabled",
        "downloads": {
            "guia_completo": "/download/guia-completo"
        }
    }
