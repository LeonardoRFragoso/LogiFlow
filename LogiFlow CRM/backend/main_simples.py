"""
LogiFlow CRM - FastAPI Backend (Versão Simplificada)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="LogiFlow CRM API",
    description="API para LogiFlow CRM - Sistema para Transportadoras",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "LogiFlow CRM API",
        "version": "1.0.0",
        "status": "running",
        "framework": "FastAPI"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Importar routers que existem
try:
    from routers.fiscal import router as fiscal_router
    app.include_router(fiscal_router, prefix="/fiscal", tags=["Fiscal"])
except ImportError as e:
    print(f"Router fiscal não carregado: {e}")

try:
    from routers.rastreamento import router as rastreamento_router
    app.include_router(rastreamento_router, prefix="/rastreamento", tags=["Rastreamento"])
except ImportError as e:
    print(f"Router rastreamento não carregado: {e}")
