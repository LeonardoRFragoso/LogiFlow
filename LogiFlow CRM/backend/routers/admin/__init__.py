# LogiFlow CRM - Admin Routers
from routers.admin.quota import router as quota_router
from routers.admin.leads import router as leads_router

__all__ = ["quota_router", "leads_router"]

