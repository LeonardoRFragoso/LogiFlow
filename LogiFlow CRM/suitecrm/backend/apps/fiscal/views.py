from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.api.views import TenantFilterMixin
from .models import CTe, MDFe
from .serializers import (
    CTeListSerializer, CTeDetailSerializer, CTeCreateSerializer,
    MDFeListSerializer, MDFeDetailSerializer, MDFeCreateSerializer
)
from .services import CTeService, MDFeService


class CTeViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = CTe.objects.select_related('pedido', 'tenant')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'pedido']
    search_fields = ['numero', 'chave', 'pedido__numero']
    ordering_fields = ['created_at', 'numero', 'valor_total']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CTeListSerializer
        elif self.action == 'create':
            return CTeCreateSerializer
        return CTeDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=True, methods=['post'])
    def emitir(self, request, pk=None):
        """Emite o CT-e via Focus NFe"""
        cte = self.get_object()
        
        if cte.status not in ['rascunho', 'rejeitado']:
            return Response({'error': 'CT-e já foi emitido'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = CTeService(cte.tenant)
        try:
            result = service.emitir(cte)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def consultar(self, request, pk=None):
        """Consulta status do CT-e"""
        cte = self.get_object()
        service = CTeService(cte.tenant)
        result = service.consultar(cte)
        return Response(result or {'status': cte.status})
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancela CT-e autorizado"""
        cte = self.get_object()
        justificativa = request.data.get('justificativa', '')
        
        if len(justificativa) < 15:
            return Response({'error': 'Justificativa deve ter no mínimo 15 caracteres'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = CTeService(cte.tenant)
        try:
            result = service.cancelar(cte, justificativa)
            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MDFeViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    queryset = MDFe.objects.select_related('veiculo', 'motorista', 'tenant')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'veiculo', 'motorista']
    search_fields = ['numero', 'chave']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MDFeListSerializer
        elif self.action == 'create':
            return MDFeCreateSerializer
        return MDFeDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=True, methods=['post'])
    def emitir(self, request, pk=None):
        """Emite o MDF-e via Focus NFe"""
        mdfe = self.get_object()
        
        if mdfe.status not in ['rascunho', 'rejeitado']:
            return Response({'error': 'MDF-e já foi emitido'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = MDFeService(mdfe.tenant)
        try:
            result = service.emitir(mdfe)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def encerrar(self, request, pk=None):
        """Encerra MDF-e autorizado"""
        mdfe = self.get_object()
        uf = request.data.get('uf_encerramento')
        municipio = request.data.get('municipio_encerramento')
        
        if not uf or not municipio:
            return Response({'error': 'UF e município são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = MDFeService(mdfe.tenant)
        try:
            result = service.encerrar(mdfe, uf, municipio)
            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
