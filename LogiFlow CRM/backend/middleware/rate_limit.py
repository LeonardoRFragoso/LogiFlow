"""
Middleware de Rate Limiting para LogiFlow CRM
Protege endpoints críticos contra abuso
"""
import time
import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class RateLimitStore:
    """
    Armazena contadores de rate limit em memória
    Para produção, considerar Redis
    """
    def __init__(self):
        # {ip: {endpoint: [(timestamp, count), ...]}}
        self._store: Dict[str, Dict[str, list]] = defaultdict(lambda: defaultdict(list))
    
    def check_rate_limit(
        self, 
        key: str, 
        endpoint: str, 
        limit: int, 
        window_seconds: int
    ) -> tuple[bool, Optional[int]]:
        """
        Verifica se uma requisição excede o rate limit
        
        Args:
            key: Chave de identificação (geralmente IP)
            endpoint: Endpoint sendo acessado
            limit: Número máximo de requisições
            window_seconds: Janela de tempo em segundos
        
        Returns:
            (is_allowed, retry_after_seconds)
        """
        now = time.time()
        window_start = now - window_seconds
        
        # Limpar requisições antigas
        requests = self._store[key][endpoint]
        requests = [req_time for req_time in requests if req_time > window_start]
        self._store[key][endpoint] = requests
        
        # Verificar limite
        if len(requests) >= limit:
            oldest_request = min(requests)
            retry_after = int(oldest_request + window_seconds - now)
            return False, max(retry_after, 1)
        
        # Adicionar nova requisição
        self._store[key][endpoint].append(now)
        return True, None
    
    def clear_old_entries(self, max_age_seconds: int = 3600):
        """
        Limpa entradas antigas (executar periodicamente)
        """
        now = time.time()
        cutoff = now - max_age_seconds
        
        for key in list(self._store.keys()):
            for endpoint in list(self._store[key].keys()):
                requests = [t for t in self._store[key][endpoint] if t > cutoff]
                if requests:
                    self._store[key][endpoint] = requests
                else:
                    del self._store[key][endpoint]
            
            if not self._store[key]:
                del self._store[key]


# Instância global
rate_limit_store = RateLimitStore()


# Configuração de rate limits por endpoint
RATE_LIMIT_CONFIG = {
    "/api/v1/auth/login": {"limit": 5, "window": 300},  # 5 tentativas por 5min
    "/api/v1/auth/refresh": {"limit": 10, "window": 300},  # 10 por 5min
    "/api/v1/auth/register": {"limit": 3, "window": 3600},  # 3 por hora
    "/api/v1/auth/reset-password": {"limit": 3, "window": 3600},  # 3 por hora
    # Endpoints de integração (evitar abuse de APIs externas)
    "/api/v1/gps": {"limit": 100, "window": 60},  # 100 por minuto
    "/api/v1/cotacao-automatica": {"limit": 30, "window": 60},  # 30 por minuto
}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware de rate limiting
    """
    
    async def dispatch(self, request: Request, call_next):
        # Obter IP do cliente
        client_ip = self._get_client_ip(request)
        
        # Verificar se endpoint tem rate limit configurado
        path = request.url.path
        rate_limit = self._get_rate_limit_for_path(path)
        
        if rate_limit:
            limit = rate_limit["limit"]
            window = rate_limit["window"]
            
            # Verificar rate limit
            is_allowed, retry_after = rate_limit_store.check_rate_limit(
                key=client_ip,
                endpoint=path,
                limit=limit,
                window=window
            )
            
            if not is_allowed:
                logger.warning(
                    f"Rate limit exceeded for {client_ip} on {path}",
                    extra={
                        "client_ip": client_ip,
                        "endpoint": path,
                        "limit": limit,
                        "window": window,
                        "retry_after": retry_after
                    }
                )
                
                raise HTTPException(
                    status_code=429,
                    detail=f"Limite de requisições excedido. Tente novamente em {retry_after}s.",
                    headers={"Retry-After": str(retry_after)}
                )
        
        # Processar requisição
        response = await call_next(request)
        
        # Adicionar headers de rate limit
        if rate_limit:
            response.headers["X-RateLimit-Limit"] = str(rate_limit["limit"])
            response.headers["X-RateLimit-Window"] = str(rate_limit["window"])
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Obtém IP do cliente considerando proxies
        """
        # Verificar headers de proxy
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback para IP direto
        return request.client.host if request.client else "unknown"
    
    def _get_rate_limit_for_path(self, path: str) -> Optional[Dict]:
        """
        Obtém configuração de rate limit para um path
        Suporta match por prefixo
        """
        # Match exato
        if path in RATE_LIMIT_CONFIG:
            return RATE_LIMIT_CONFIG[path]
        
        # Match por prefixo
        for pattern, config in RATE_LIMIT_CONFIG.items():
            if path.startswith(pattern):
                return config
        
        return None


def cleanup_rate_limit_store():
    """
    Função para limpar entradas antigas do store
    Deve ser executada periodicamente (via scheduler ou background task)
    """
    rate_limit_store.clear_old_entries()
    logger.info("Rate limit store cleaned up")

