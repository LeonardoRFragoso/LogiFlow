"""
Prometheus Metrics Middleware
==============================
Coleta métricas de performance, latência e erros da API
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry
from typing import Callable

logger = logging.getLogger(__name__)

# Registry centralizado para Prometheus
REGISTRY = CollectorRegistry()

# ========================================
# Métricas de Requisição HTTP
# ========================================

# Contador: Total de requisições por método e path
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total de requisições HTTP processadas",
    ["method", "endpoint", "status_code"],
    registry=REGISTRY
)

# Histogram: Latência das requisições em segundos
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Latência das requisições HTTP em segundos",
    ["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0),
    registry=REGISTRY
)

# Gauge: Requisições ativas no momento
ACTIVE_REQUESTS = Gauge(
    "http_active_requests",
    "Número de requisições HTTP ativas",
    ["method", "endpoint"],
    registry=REGISTRY
)

# Counter: Total de erros por tipo
ERROR_COUNT = Counter(
    "http_errors_total",
    "Total de erros HTTP",
    ["method", "endpoint", "status_code"],
    registry=REGISTRY
)

# ========================================
# Métricas de Database
# ========================================

DATABASE_QUERIES_TOTAL = Counter(
    "database_queries_total",
    "Total de queries executadas",
    ["operation", "table"],
    registry=REGISTRY
)

DATABASE_QUERY_DURATION = Histogram(
    "database_query_duration_seconds",
    "Duração das queries de database",
    ["operation", "table"],
    buckets=(0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0),
    registry=REGISTRY
)

# ========================================
# Métricas de Cache (Redis)
# ========================================

CACHE_HITS = Counter(
    "cache_hits_total",
    "Total de cache hits",
    ["cache_name"],
    registry=REGISTRY
)

CACHE_MISSES = Counter(
    "cache_misses_total",
    "Total de cache misses",
    ["cache_name"],
    registry=REGISTRY
)

# ========================================
# Métricas de Negócio
# ========================================

COTACAO_CREATED = Counter(
    "cotacao_created_total",
    "Total de cotações criadas",
    ["tenant_id"],
    registry=REGISTRY
)

PEDIDO_CREATED = Counter(
    "pedido_created_total",
    "Total de pedidos criados",
    ["tenant_id", "status"],
    registry=REGISTRY
)

PEDIDO_ENTREGUE = Counter(
    "pedido_entregue_total",
    "Total de pedidos entregues",
    ["tenant_id"],
    registry=REGISTRY
)

# Gauge: Pedidos pendentes
PEDIDOS_PENDENTES = Gauge(
    "pedidos_pendentes",
    "Número de pedidos pendentes por tenant",
    ["tenant_id"],
    registry=REGISTRY
)

# ========================================
# Middleware Prometheus
# ========================================

class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Middleware que coleta métricas do Prometheus para cada requisição
    """
    
    def __init__(self, app, group_paths: bool = False):
        super().__init__(app)
        self.group_paths = group_paths
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        """
        Processa requisição e coleta métricas
        """
        start_time = time.time()
        method = request.method
        path = request.url.path
        
        # Agrupar paths (para evitar explosion de métricas)
        endpoint = self._get_endpoint_label(path) if self.group_paths else path
        
        # Incrementar requisições ativas
        ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).inc()
        
        try:
            # Processar requisição
            response = await call_next(request)
            
            # Calcular duração
            duration = time.time() - start_time
            
            # Registrar métrica
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status_code=response.status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
            
            # Registrar erros
            if response.status_code >= 400:
                ERROR_COUNT.labels(
                    method=method,
                    endpoint=endpoint,
                    status_code=response.status_code
                ).inc()
            
            # Log de requisição lenta
            if duration > 1.0:
                logger.warning(
                    f"Slow request detected",
                    extra={
                        "method": method,
                        "path": path,
                        "duration": duration,
                        "status_code": response.status_code
                    }
                )
            
            return response
            
        except Exception as exc:
            # Registrar erro
            ERROR_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status_code=500
            ).inc()
            raise exc
            
        finally:
            # Decrementar requisições ativas
            ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).dec()
    
    def _get_endpoint_label(self, path: str) -> str:
        """
        Agrupa paths para evitar explosion de métricas
        Exemplo: /api/v1/clientes/123/pedidos -> /api/v1/clientes/{id}/pedidos
        """
        parts = path.split("/")
        
        # Substituir IDs numéricos por placeholder
        labeled_parts = []
        for part in parts:
            if part.isdigit():
                labeled_parts.append("{id}")
            elif part.startswith("{") and part.endswith("}"):
                labeled_parts.append(part)
            else:
                labeled_parts.append(part)
        
        return "/".join(labeled_parts)


def setup_prometheus_metrics(app):
    """
    Configurar Prometheus middleware na aplicação
    """
    app.add_middleware(PrometheusMiddleware, group_paths=True)
    logger.info("Prometheus middleware configured")


def get_metrics() -> bytes:
    """
    Retorna métricas em formato Prometheus (para expor em /metrics)
    """
    return generate_latest(REGISTRY)


# ========================================
# Helpers para registrar métricas customizadas
# ========================================

def record_db_query(operation: str, table: str, duration: float):
    """
    Registra execução de query de database
    """
    DATABASE_QUERIES_TOTAL.labels(operation=operation, table=table).inc()
    DATABASE_QUERY_DURATION.labels(operation=operation, table=table).observe(duration)


def record_cache_hit(cache_name: str):
    """Registra cache hit"""
    CACHE_HITS.labels(cache_name=cache_name).inc()


def record_cache_miss(cache_name: str):
    """Registra cache miss"""
    CACHE_MISSES.labels(cache_name=cache_name).inc()


def record_cotacao(tenant_id: str):
    """Registra nova cotação criada"""
    COTACAO_CREATED.labels(tenant_id=tenant_id).inc()


def record_pedido(tenant_id: str, status: str):
    """Registra novo pedido criado"""
    PEDIDO_CREATED.labels(tenant_id=tenant_id, status=status).inc()


def record_pedido_entregue(tenant_id: str):
    """Registra entrega de pedido"""
    PEDIDO_ENTREGUE.labels(tenant_id=tenant_id).inc()


def set_pedidos_pendentes(tenant_id: str, count: int):
    """Define gauge de pedidos pendentes"""
    PEDIDOS_PENDENTES.labels(tenant_id=tenant_id).set(count)
