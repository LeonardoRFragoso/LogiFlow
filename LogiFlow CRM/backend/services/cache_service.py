"""
LogiFlow CRM - Redis Cache Service
===================================
Serviço centralizado de cache Redis para performance enterprise
"""

import redis
import json
from typing import Optional, Any
from loguru import logger
from config import settings


class CacheService:
    """Serviço de cache Redis com TTL configurável"""
    
    def __init__(self):
        """Inicializa conexão Redis"""
        try:
            if settings.REDIS_URL:
                self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
            else:
                self.redis = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                    decode_responses=True
                )
            # Testar conexão
            self.redis.ping()
            logger.info("✅ Redis conectado com sucesso")
        except Exception as e:
            logger.warning(f"⚠️ Redis indisponível: {e}. Cache desabilitado.")
            self.redis = None
    
    def get(self, key: str) -> Optional[Any]:
        """
        Recupera valor do cache
        
        Args:
            key: Chave do cache (ex: crm:metrics:dashboard)
        
        Returns:
            Valor deserializado ou None se não existir/erro
        """
        if not self.redis:
            return None
        
        try:
            cached = self.redis.get(key)
            if cached:
                return json.loads(cached)
            return None
        except Exception as e:
            logger.error(f"Erro ao ler cache {key}: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """
        Armazena valor no cache com TTL
        
        Args:
            key: Chave do cache
            value: Valor a ser armazenado (será serializado como JSON)
            ttl: Time-to-live em segundos (padrão: 5 minutos)
        
        Returns:
            True se sucesso, False se erro
        """
        if not self.redis:
            return False
        
        try:
            serialized = json.dumps(value, default=str)
            self.redis.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Erro ao gravar cache {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Remove chave do cache
        
        Args:
            key: Chave a ser removida
        
        Returns:
            True se sucesso, False se erro
        """
        if not self.redis:
            return False
        
        try:
            self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar cache {key}: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """
        Remove todas as chaves que correspondem ao padrão
        
        Args:
            pattern: Padrão (ex: crm:cliente:*)
        
        Returns:
            Número de chaves deletadas
        """
        if not self.redis:
            return 0
        
        try:
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Erro ao deletar padrão {pattern}: {e}")
            return 0
    
    def invalidate_crm_metrics(self):
        """Invalida todos os caches de métricas CRM"""
        return self.delete_pattern("crm:metrics:*")
    
    def invalidate_cliente_360(self, cliente_id: str):
        """Invalida cache do Cliente 360"""
        return self.delete(f"crm:cliente360:{cliente_id}")


# Instância global do cache
cache = CacheService()
