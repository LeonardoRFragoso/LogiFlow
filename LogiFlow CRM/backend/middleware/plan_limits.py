"""
Middleware para Validar Limites do Plano
Verifica se o tenant não excedeu os limites do plano contratado
"""

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from models import Tenant
from datetime import datetime, timedelta
from loguru import logger


class PlanLimitsMiddleware:
    """Middleware para validar limites do plano"""
    
    @staticmethod
    def check_user_limit(tenant: Tenant, db: Session) -> bool:
        """
        Verifica se o tenant pode adicionar mais usuários
        """
        if tenant.max_users == -1:  # ilimitado
            return True
        
        from models import Motorista
        current_users = db.query(Motorista).count()
        
        if current_users >= tenant.max_users:
            logger.warning(f"Tenant {tenant.id} atingiu limite de usuários: {current_users}/{tenant.max_users}")
            raise HTTPException(
                status_code=403,
                detail=f"Limite de usuários atingido ({tenant.max_users}). Faça upgrade do seu plano."
            )
        
        return True
    
    @staticmethod
    def check_vehicle_limit(tenant: Tenant, db: Session) -> bool:
        """
        Verifica se o tenant pode adicionar mais veículos
        """
        if tenant.max_vehicles == -1:  # ilimitado
            return True
        
        from models import Veiculo
        current_vehicles = db.query(Veiculo).count()
        
        if current_vehicles >= tenant.max_vehicles:
            logger.warning(f"Tenant {tenant.id} atingiu limite de veículos: {current_vehicles}/{tenant.max_vehicles}")
            raise HTTPException(
                status_code=403,
                detail=f"Limite de veículos atingido ({tenant.max_vehicles}). Faça upgrade do seu plano."
            )
        
        return True
    
    @staticmethod
    def check_order_limit(tenant: Tenant, db: Session) -> bool:
        """
        Verifica se o tenant pode criar mais pedidos no mês atual
        """
        if tenant.max_orders_per_month == -1:  # ilimitado
            return True
        
        # Contar pedidos do mês atual
        from models import Pedido
        
        first_day = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # TODO: Filtrar por tenant_id quando implementar multi-tenant
        orders_count = db.query(Pedido).filter(
            Pedido.created_at >= first_day
        ).count()
        
        if orders_count >= tenant.max_orders_per_month:
            logger.warning(f"Tenant {tenant.id} atingiu limite de pedidos: {orders_count}/{tenant.max_orders_per_month}")
            raise HTTPException(
                status_code=403,
                detail=f"Limite de pedidos do mês atingido ({tenant.max_orders_per_month}). Faça upgrade do seu plano."
            )
        
        return True
    
    @staticmethod
    def get_usage_stats(tenant: Tenant, db: Session) -> dict:
        """
        Retorna estatísticas de uso do tenant
        """
        from models import Pedido, Veiculo, Motorista
        
        # Contar pedidos do mês atual
        first_day = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        orders_this_month = db.query(Pedido).filter(
            Pedido.created_at >= first_day
        ).count()
        
        # Contar veículos ativos
        vehicles_count = db.query(Veiculo).count()
        
        # Contar motoristas (proxy para usuários até implementar User model)
        users_count = db.query(Motorista).count()
        
        return {
            "plan": tenant.plan,
            "limits": {
                "users": {
                    "max": tenant.max_users if tenant.max_users != -1 else "ilimitado",
                    "current": users_count,
                    "available": (tenant.max_users - users_count) if tenant.max_users != -1 else "ilimitado"
                },
                "vehicles": {
                    "max": tenant.max_vehicles if tenant.max_vehicles != -1 else "ilimitado",
                    "current": vehicles_count,
                    "available": (tenant.max_vehicles - vehicles_count) if tenant.max_vehicles != -1 else "ilimitado"
                },
                "orders_per_month": {
                    "max": tenant.max_orders_per_month if tenant.max_orders_per_month != -1 else "ilimitado",
                    "current": orders_this_month,
                    "available": (tenant.max_orders_per_month - orders_this_month) if tenant.max_orders_per_month != -1 else "ilimitado"
                }
            },
            "trial_ends_at": tenant.trial_ends_at.isoformat() if tenant.trial_ends_at else None,
            "is_trial": tenant.status == "trial"
        }


# Funções helper
def check_user_limit(tenant: Tenant, db: Session) -> bool:
    """Helper para verificar limite de usuários"""
    return PlanLimitsMiddleware.check_user_limit(tenant, db)


def check_vehicle_limit(tenant: Tenant, db: Session) -> bool:
    """Helper para verificar limite de veículos"""
    return PlanLimitsMiddleware.check_vehicle_limit(tenant, db)


def check_order_limit(tenant: Tenant, db: Session) -> bool:
    """Helper para verificar limite de pedidos"""
    return PlanLimitsMiddleware.check_order_limit(tenant, db)


def get_usage_stats(tenant: Tenant, db: Session) -> dict:
    """Helper para obter estatísticas de uso"""
    return PlanLimitsMiddleware.get_usage_stats(tenant, db)
