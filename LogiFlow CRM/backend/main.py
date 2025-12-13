"""
LogiFlow CRM - FastAPI Backend
================================
API principal para orquestração do LogiFlow CRM
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import redis
from loguru import logger
from pathlib import Path

from config import settings
# Importar routers
try:
    from routers import fiscal, rastreamento, cotacoes, pedidos, motoristas, veiculos, auth, whatsapp, maps, suitecrm, demo, ocorrencias
    # db_api é opcional (requer SQLAlchemy)
    try:
        from routers import db_api
    except ImportError:
        db_api = None
        logger.warning("db_api não disponível (SQLAlchemy não instalado)")
except ImportError as e:
    logger.warning(f"Erro ao importar routers: {e}")
    fiscal = None
    rastreamento = None
    cotacoes = None
    pedidos = None
    motoristas = None
    veiculos = None
    auth = None
    whatsapp = None
    maps = None
    suitecrm = None
    demo = None
    db_api = None
    ocorrencias = None

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
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        redis_client.ping()
        logger.info("Redis conectado com sucesso")
        app.state.redis = redis_client
    except Exception as e:
        logger.error(f"Erro ao conectar Redis: {e}")
    
    # Inicializar cliente SuiteCRM (quando necessário)
    # app.state.suitecrm = SuiteCRMClient(
    #     base_url=settings.SUITECRM_URL,
    #     client_id=settings.SUITECRM_CLIENT_ID,
    #     client_secret=settings.SUITECRM_CLIENT_SECRET
    # )
    
    logger.info("LogiFlow API iniciada com sucesso!")
    
    yield
    
    # Shutdown
    logger.info("Encerrando LogiFlow API...")
    if hasattr(app.state, 'redis'):
        app.state.redis.close()


# Criar aplicação FastAPI
app = FastAPI(
    title="LogiFlow CRM API",
    description="API de orquestração para o LogiFlow CRM - Sistema especializado para Transportadoras",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===========================================
# Routers
# ===========================================
if fiscal:
    app.include_router(fiscal.router, prefix="/fiscal", tags=["Fiscal"])
if rastreamento:
    app.include_router(rastreamento.router, prefix="/rastreamento", tags=["Rastreamento"])
if cotacoes:
    app.include_router(cotacoes.router, prefix="/cotacoes", tags=["Cotações"])
if pedidos:
    app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
if motoristas:
    app.include_router(motoristas.router, prefix="/motoristas", tags=["Motoristas"])
if veiculos:
    app.include_router(veiculos.router, prefix="/veiculos", tags=["Veículos"])
if auth:
    app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
if whatsapp:
    app.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
if maps:
    app.include_router(maps.router, prefix="/maps", tags=["Google Maps"])
if suitecrm:
    app.include_router(suitecrm.router)
if demo:
    app.include_router(demo.router)
if db_api:
    app.include_router(db_api.router)
if ocorrencias:
    app.include_router(ocorrencias.router, prefix="/ocorrencias", tags=["Ocorrências"])


# ===========================================
# Exception Handlers
# ===========================================
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
