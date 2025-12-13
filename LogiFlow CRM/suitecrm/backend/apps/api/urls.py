"""
LogiFlow CRM - API URLs
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserViewSet,
    ClienteViewSet,
    CotacaoViewSet,
    PedidoFreteViewSet,
    EntregaViewSet,
    MotoristaViewSet,
    VeiculoViewSet,
    ManutencaoViewSet,
    OcorrenciaViewSet,
)
from apps.fiscal.views import CTeViewSet, MDFeViewSet
from apps.core.sla_views import SLAConfigViewSet, SLAClienteConfigViewSet, SLARotaConfigViewSet

# Router para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'cotacoes', CotacaoViewSet, basename='cotacao')
router.register(r'pedidos', PedidoFreteViewSet, basename='pedido')
router.register(r'entregas', EntregaViewSet, basename='entrega')
router.register(r'motoristas', MotoristaViewSet, basename='motorista')
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'ocorrencias', OcorrenciaViewSet, basename='ocorrencia')
router.register(r'ctes', CTeViewSet, basename='cte')
router.register(r'mdfes', MDFeViewSet, basename='mdfe')
router.register(r'sla/config', SLAConfigViewSet, basename='sla-config')
router.register(r'sla/clientes', SLAClienteConfigViewSet, basename='sla-cliente')
router.register(r'sla/rotas', SLARotaConfigViewSet, basename='sla-rota')

urlpatterns = [
    # JWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('', include(router.urls)),
]
