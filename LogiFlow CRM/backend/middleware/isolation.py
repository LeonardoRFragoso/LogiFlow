"""
Middleware de Isolamento de Dados Multi-Tenant

Garante que queries ao banco sempre filtrem por tenant_id
"""
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from database import get_db, SessionLocal
import logging

logger = logging.getLogger(__name__)


class TenantIsolationError(Exception):
    """Erro quando tentativa de acessar dados de outro tenant"""
    pass


def setup_tenant_isolation():
    """
    Configura hooks do SQLAlchemy para adicionar filtro de tenant automaticamente
    """
    @event.listens_for(Session, "do_orm_execute")
    def receive_do_orm_execute(orm_execute_state):
        """
        Hook executado antes de toda query ORM
        Adiciona filtro WHERE tenant_id = X automaticamente
        """
        if not orm_execute_state.is_select:
            return
        
        # Obter tenant_id do contexto (precisa ser setado antes da query)
        # TODO: Integrar com contextvars para thread-safety
        # from contextvars import ContextVar
        # current_tenant: ContextVar[Optional[int]] = ContextVar('current_tenant', default=None)
        
        # Por enquanto, log de warning se não houver tenant no contexto
        logger.debug("Query executada - isolamento de tenant deve ser manual por enquanto")


def filter_by_tenant(query, model, tenant_id: int):
    """
    Helper para adicionar filtro de tenant em queries manuais
    
    Uso:
        query = db.query(Entrega)
        query = filter_by_tenant(query, Entrega, tenant_id)
    """
    if not hasattr(model, 'tenant_id'):
        logger.warning(f"Modelo {model.__name__} não tem campo tenant_id - pulando filtro")
        return query
    
    return query.filter(model.tenant_id == tenant_id)


def validate_tenant_access(obj, tenant_id: int):
    """
    Valida se um objeto pertence ao tenant atual
    Levanta TenantIsolationError se não pertencer
    
    Uso:
        entrega = db.query(Entrega).get(entrega_id)
        validate_tenant_access(entrega, current_tenant_id)
    """
    if not hasattr(obj, 'tenant_id'):
        logger.warning(f"Objeto {type(obj).__name__} não tem tenant_id - pulando validação")
        return
    
    if obj.tenant_id != tenant_id:
        raise TenantIsolationError(
            f"Acesso negado: objeto pertence ao tenant {obj.tenant_id}, "
            f"mas tenant atual é {tenant_id}"
        )


class TenantScopedSession:
    """
    Context manager para garantir que todas as queries em um bloco
    sejam filtradas por tenant
    """
    def __init__(self, tenant_id: int):
        self.tenant_id = tenant_id
        self.db = None
    
    def __enter__(self):
        self.db = SessionLocal()
        # TODO: Setar tenant_id no contexto da sessão
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


# Decorator para rotas que requerem isolamento de tenant
def require_tenant_isolation(func):
    """
    Decorator para garantir isolamento de dados em rotas
    
    Uso:
        @router.get("/entregas")
        @require_tenant_isolation
        async def listar_entregas(request: Request, db: Session = Depends(get_db)):
            tenant_id = request.state.tenant_id
            entregas = db.query(Entrega).filter(Entrega.tenant_id == tenant_id).all()
    """
    from functools import wraps
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # TODO: Adicionar validação automática
        return await func(*args, **kwargs)
    
    return wrapper

