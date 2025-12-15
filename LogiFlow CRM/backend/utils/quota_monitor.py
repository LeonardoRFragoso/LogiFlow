"""
Sistema de Monitoramento de Quotas para APIs Externas
Monitora uso e previne excesso de chamadas
"""
import time
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class QuotaMonitor:
    """
    Monitora quotas de uso de APIs externas
    """
    
    def __init__(self):
        # {api_name: {"count": int, "reset_time": float, "limit": int}}
        self._quotas: Dict[str, Dict] = {}
        # {api_name: [timestamp, ...]} - histórico de chamadas
        self._call_history: Dict[str, list] = defaultdict(list)
    
    def register_api(
        self, 
        api_name: str, 
        daily_limit: int, 
        monthly_limit: Optional[int] = None
    ):
        """
        Registra uma API para monitoramento
        
        Args:
            api_name: Nome da API (ex: "google_maps_distance_matrix")
            daily_limit: Limite diário de requisições
            monthly_limit: Limite mensal (opcional)
        """
        self._quotas[api_name] = {
            "daily_limit": daily_limit,
            "monthly_limit": monthly_limit,
            "daily_count": 0,
            "monthly_count": 0,
            "daily_reset": self._get_next_day_reset(),
            "monthly_reset": self._get_next_month_reset()
        }
        logger.info(f"Quota registered for {api_name}: {daily_limit}/day")
    
    def check_quota(self, api_name: str) -> tuple[bool, Optional[str]]:
        """
        Verifica se ainda há quota disponível
        
        Returns:
            (is_available, error_message)
        """
        if api_name not in self._quotas:
            # API não monitorada, permitir
            return True, None
        
        quota = self._quotas[api_name]
        now = time.time()
        
        # Reset diário
        if now >= quota["daily_reset"]:
            quota["daily_count"] = 0
            quota["daily_reset"] = self._get_next_day_reset()
            logger.info(f"Daily quota reset for {api_name}")
        
        # Reset mensal
        if quota["monthly_limit"] and now >= quota["monthly_reset"]:
            quota["monthly_count"] = 0
            quota["monthly_reset"] = self._get_next_month_reset()
            logger.info(f"Monthly quota reset for {api_name}")
        
        # Verificar limite diário
        if quota["daily_count"] >= quota["daily_limit"]:
            return False, f"Limite diário de {quota['daily_limit']} requisições atingido para {api_name}"
        
        # Verificar limite mensal
        if quota["monthly_limit"] and quota["monthly_count"] >= quota["monthly_limit"]:
            return False, f"Limite mensal de {quota['monthly_limit']} requisições atingido para {api_name}"
        
        return True, None
    
    def record_call(
        self, 
        api_name: str, 
        success: bool = True, 
        cost: float = 0.0
    ):
        """
        Registra uma chamada à API
        
        Args:
            api_name: Nome da API
            success: Se a chamada foi bem-sucedida
            cost: Custo estimado da chamada (USD)
        """
        now = time.time()
        
        # Registrar no histórico
        self._call_history[api_name].append({
            "timestamp": now,
            "success": success,
            "cost": cost
        })
        
        # Atualizar contadores
        if api_name in self._quotas:
            if success:
                self._quotas[api_name]["daily_count"] += 1
                if self._quotas[api_name].get("monthly_limit"):
                    self._quotas[api_name]["monthly_count"] += 1
            
            # Log de alerta se aproximando do limite
            daily_usage_percent = (
                self._quotas[api_name]["daily_count"] / 
                self._quotas[api_name]["daily_limit"] * 100
            )
            
            if daily_usage_percent >= 80:
                logger.warning(
                    f"Quota alert for {api_name}: {daily_usage_percent:.1f}% used",
                    extra={
                        "api_name": api_name,
                        "daily_count": self._quotas[api_name]["daily_count"],
                        "daily_limit": self._quotas[api_name]["daily_limit"],
                        "usage_percent": daily_usage_percent
                    }
                )
    
    def get_usage_stats(self, api_name: str) -> Dict:
        """
        Obtém estatísticas de uso de uma API
        """
        if api_name not in self._quotas:
            return {"error": "API not monitored"}
        
        quota = self._quotas[api_name]
        history = self._call_history.get(api_name, [])
        
        # Estatísticas das últimas 24h
        now = time.time()
        last_24h = [call for call in history if call["timestamp"] > now - 86400]
        
        total_cost = sum(call.get("cost", 0) for call in last_24h)
        success_rate = (
            sum(1 for call in last_24h if call["success"]) / len(last_24h) * 100
            if last_24h else 0
        )
        
        return {
            "api_name": api_name,
            "daily": {
                "count": quota["daily_count"],
                "limit": quota["daily_limit"],
                "remaining": quota["daily_limit"] - quota["daily_count"],
                "usage_percent": quota["daily_count"] / quota["daily_limit"] * 100,
                "reset_at": datetime.fromtimestamp(quota["daily_reset"]).isoformat()
            },
            "monthly": {
                "count": quota.get("monthly_count", 0),
                "limit": quota.get("monthly_limit"),
                "remaining": (
                    quota["monthly_limit"] - quota["monthly_count"]
                    if quota.get("monthly_limit") else None
                ),
                "reset_at": datetime.fromtimestamp(quota["monthly_reset"]).isoformat()
            } if quota.get("monthly_limit") else None,
            "last_24h": {
                "calls": len(last_24h),
                "success_rate": success_rate,
                "total_cost_usd": total_cost
            }
        }
    
    def _get_next_day_reset(self) -> float:
        """Retorna timestamp do próximo reset diário (meia-noite)"""
        tomorrow = datetime.now() + timedelta(days=1)
        midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        return midnight.timestamp()
    
    def _get_next_month_reset(self) -> float:
        """Retorna timestamp do próximo reset mensal (dia 1)"""
        now = datetime.now()
        if now.month == 12:
            next_month = now.replace(year=now.year + 1, month=1, day=1)
        else:
            next_month = now.replace(month=now.month + 1, day=1)
        return next_month.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


# Instância global
quota_monitor = QuotaMonitor()


# Registrar APIs monitoradas
def init_quota_monitoring():
    """
    Inicializa monitoramento de quotas
    Chamar no startup da aplicação
    """
    # Google Maps Distance Matrix
    # Preço: $5 por 1000 requisições
    # Free tier: $200 de crédito/mês = ~40,000 requisições
    quota_monitor.register_api(
        "google_maps_distance_matrix",
        daily_limit=1000,  # ~30k/mês
        monthly_limit=30000
    )
    
    # Outras APIs podem ser adicionadas aqui
    logger.info("Quota monitoring initialized")

