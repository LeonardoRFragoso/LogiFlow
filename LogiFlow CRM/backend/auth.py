"""
LogiFlow CRM - Auth shim
Re-exports from routers.auth so that 'from auth import get_current_user' works.
"""

from routers.auth import (
    get_current_user,
    get_current_admin,
    get_current_gerente_ou_admin,
    verificar_token,
    criar_access_token,
)

__all__ = [
    "get_current_user",
    "get_current_admin",
    "get_current_gerente_ou_admin",
    "verificar_token",
    "criar_access_token",
]
