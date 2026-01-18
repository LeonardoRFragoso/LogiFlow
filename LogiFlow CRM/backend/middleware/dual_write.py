"""
LogiFlow CRM - Middleware de Escrita Dupla
==========================================
Intercepta operações de escrita e sincroniza com SuiteCRM automaticamente
"""

from typing import Any, Optional
from loguru import logger
from functools import wraps
import asyncio


class DualWriteHelper:
    """
    Helper para escrita dupla: local + SuiteCRM
    
    Estratégia:
    - Escrita local sempre acontece (prioritária)
    - Escrita SuiteCRM é assíncrona (fire-and-forget)
    - Se falhar no CRM, registra para retry posterior
    """
    
    def __init__(self):
        self.failed_syncs = []
    
    async def write_with_sync(
        self,
        local_write_func,
        module_name: str,
        operation: str = "create",
        sync_enabled: bool = True
    ):
        """
        Executa escrita local + sincronização com SuiteCRM
        
        Args:
            local_write_func: Função que executa a escrita local
            module_name: Nome do módulo (pedidos, motoristas, etc)
            operation: create, update, delete
            sync_enabled: Se False, apenas escrita local
        
        Returns:
            Resultado da escrita local
        """
        # 1. Executar escrita local (prioritária)
        local_result = await local_write_func() if asyncio.iscoroutinefunction(local_write_func) else local_write_func()
        
        # 2. Se sync desabilitado, retornar
        if not sync_enabled:
            return local_result
        
        # 3. Sincronizar com SuiteCRM (fire-and-forget)
        try:
            from services.sync_service import sync_service
            
            # Executar sync de forma assíncrona sem bloquear
            asyncio.create_task(
                self._sync_to_suitecrm_background(
                    sync_service,
                    module_name,
                    local_result,
                    operation
                )
            )
            
        except Exception as e:
            logger.warning(f"⚠️ Falha ao iniciar sync para SuiteCRM: {e}")
            self.failed_syncs.append({
                "module": module_name,
                "operation": operation,
                "record_id": getattr(local_result, 'id', None),
                "timestamp": None
            })
        
        return local_result
    
    async def _sync_to_suitecrm_background(
        self,
        sync_service,
        module_name: str,
        local_record: Any,
        operation: str
    ):
        """Executa sincronização em background"""
        try:
            result = await sync_service.sync_to_suitecrm(
                module_name,
                local_record,
                operation
            )
            
            if result:
                logger.debug(f"✅ Sync automático: {module_name}/{getattr(local_record, 'id', 'unknown')}")
            else:
                logger.warning(f"⚠️ Sync falhou: {module_name}/{getattr(local_record, 'id', 'unknown')}")
                
        except Exception as e:
            logger.error(f"❌ Erro no sync background: {e}")
    
    def get_failed_syncs(self):
        """Retorna sincronizações que falharam"""
        return self.failed_syncs
    
    def clear_failed_syncs(self):
        """Limpa lista de sincronizações falhadas"""
        self.failed_syncs.clear()


# Instância global
dual_write = DualWriteHelper()


def with_suitecrm_sync(module_name: str, operation: str = "create"):
    """
    Decorator para adicionar sincronização automática com SuiteCRM
    
    Uso:
    @with_suitecrm_sync("pedidos", "create")
    async def criar_pedido(data):
        # ... lógica de criação local
        return pedido_criado
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Executar função original
            result = await func(*args, **kwargs)
            
            # Sincronizar com SuiteCRM em background
            try:
                from services.sync_service import sync_service
                asyncio.create_task(
                    sync_service.sync_to_suitecrm(module_name, result, operation)
                )
            except Exception as e:
                logger.warning(f"⚠️ Falha ao sincronizar {module_name}: {e}")
            
            return result
        
        return wrapper
    return decorator
