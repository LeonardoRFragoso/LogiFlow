"""
LogiFlow CRM - SLA Views
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .sla_models import SLAConfig, SLAClienteConfig, SLARotaConfig
from .sla_serializers import SLAConfigSerializer, SLAClienteConfigSerializer, SLARotaConfigSerializer


class SLAConfigViewSet(viewsets.ModelViewSet):
    """ViewSet para configuração global de SLA"""
    
    serializer_class = SLAConfigSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SLAConfig.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def atual(self, request):
        """Retorna ou atualiza a configuração atual do tenant"""
        tenant = getattr(request.user, 'tenant', None)
        
        if not tenant or not tenant.id:
            # Retorna configuração padrão sem salvar no banco
            return Response({
                'id': None,
                'limite_verde': 2,
                'limite_amarelo': 1,
                'considerar_dias_uteis': False,
                'alertar_sla_amarelo': True,
                'alertar_sla_vermelho': True,
            })
        
        config, created = SLAConfig.objects.get_or_create(
            tenant=tenant,
            defaults={
                'limite_verde': 2,
                'limite_amarelo': 1
            }
        )
        
        if request.method == 'GET':
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        
        serializer = self.get_serializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SLAClienteConfigViewSet(viewsets.ModelViewSet):
    """ViewSet para SLA por cliente"""
    
    serializer_class = SLAClienteConfigSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SLAClienteConfig.objects.filter(tenant=self.request.user.tenant).select_related('cliente')
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=False, methods=['get'])
    def por_cliente(self, request):
        """Retorna SLA de um cliente específico"""
        cliente_id = request.query_params.get('cliente_id')
        if not cliente_id:
            return Response({'error': 'cliente_id é obrigatório'}, status=400)
        
        try:
            config = self.get_queryset().get(cliente_id=cliente_id)
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        except SLAClienteConfig.DoesNotExist:
            return Response({'error': 'SLA não configurado para este cliente'}, status=404)


class SLARotaConfigViewSet(viewsets.ModelViewSet):
    """ViewSet para SLA por rota"""
    
    serializer_class = SLARotaConfigSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        qs = SLARotaConfig.objects.filter(tenant=self.request.user.tenant)
        
        # Filtros
        ativo = self.request.query_params.get('ativo')
        if ativo is not None:
            qs = qs.filter(ativo=ativo.lower() == 'true')
        
        origem_uf = self.request.query_params.get('origem_uf')
        if origem_uf:
            qs = qs.filter(origem_uf=origem_uf.upper())
        
        destino_uf = self.request.query_params.get('destino_uf')
        if destino_uf:
            qs = qs.filter(destino_uf=destino_uf.upper())
        
        return qs
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=False, methods=['get'])
    def buscar_rota(self, request):
        """Busca SLA para uma rota específica"""
        origem_uf = request.query_params.get('origem_uf', '').upper()
        origem_cidade = request.query_params.get('origem_cidade', '')
        destino_uf = request.query_params.get('destino_uf', '').upper()
        destino_cidade = request.query_params.get('destino_cidade', '')
        
        if not origem_uf or not destino_uf:
            return Response({'error': 'origem_uf e destino_uf são obrigatórios'}, status=400)
        
        # Tenta encontrar rota específica (cidade + UF)
        config = self.get_queryset().filter(
            origem_uf=origem_uf,
            origem_cidade__iexact=origem_cidade,
            destino_uf=destino_uf,
            destino_cidade__iexact=destino_cidade,
            ativo=True
        ).first()
        
        # Se não encontrar, tenta apenas por UF
        if not config:
            config = self.get_queryset().filter(
                origem_uf=origem_uf,
                origem_cidade='',
                destino_uf=destino_uf,
                destino_cidade='',
                ativo=True
            ).first()
        
        if config:
            serializer = self.get_serializer(config)
            return Response(serializer.data)
        
        return Response({'error': 'Nenhuma configuração de SLA encontrada para esta rota'}, status=404)


def calcular_sla_pedido(pedido):
    """
    Calcula o SLA de um pedido considerando:
    1. Configuração global do tenant
    2. Configuração específica do cliente (se houver)
    3. Configuração da rota (se houver)
    
    Retorna: 'verde', 'amarelo' ou 'vermelho'
    """
    from django.utils import timezone
    
    if pedido.status == 'entregue':
        return pedido.sla_status  # Mantém o status final
    
    tenant = pedido.tenant
    hoje = timezone.now().date()
    dias_restantes = (pedido.previsao_entrega - hoje).days
    
    # Busca configurações
    config_global = SLAConfig.objects.filter(tenant=tenant).first()
    config_cliente = SLAClienteConfig.objects.filter(tenant=tenant, cliente=pedido.cliente).first()
    config_rota = SLARotaConfig.objects.filter(
        tenant=tenant,
        origem_uf=pedido.origem_uf,
        destino_uf=pedido.destino_uf,
        ativo=True
    ).first()
    
    # Define limites padrão
    limite_verde = 2
    limite_amarelo = 1
    
    # Aplica configuração global
    if config_global:
        limite_verde = config_global.limite_verde
        limite_amarelo = config_global.limite_amarelo
    
    # Aplica configuração de rota (adiciona dias)
    if config_rota:
        if config_rota.limite_verde_customizado is not None:
            limite_verde = config_rota.limite_verde_customizado
        else:
            limite_verde += config_rota.dias_adicionais
        
        if config_rota.limite_amarelo_customizado is not None:
            limite_amarelo = config_rota.limite_amarelo_customizado
        else:
            limite_amarelo += config_rota.dias_adicionais
    
    # Aplica configuração de cliente (sobrescreve)
    if config_cliente:
        limite_verde = config_cliente.limite_verde
        limite_amarelo = config_cliente.limite_amarelo
        
        # Aplica bônus de horas para VIP (converte para dias)
        if config_cliente.bonus_horas > 0:
            bonus_dias = config_cliente.bonus_horas / 24
            dias_restantes += bonus_dias
    
    # Calcula SLA
    if dias_restantes < 0:
        return 'vermelho'
    elif dias_restantes <= limite_amarelo:
        return 'amarelo'
    else:
        return 'verde'
