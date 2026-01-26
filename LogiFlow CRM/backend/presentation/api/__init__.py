"""Presentation API - FastAPI Routers"""
from .clientes import router as clientes_router
from .cotacoes import router as cotacoes_router
from .pedidos import router as pedidos_router

__all__ = ["clientes_router", "cotacoes_router", "pedidos_router"]
