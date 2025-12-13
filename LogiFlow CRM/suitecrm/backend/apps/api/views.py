"""
LogiFlow CRM - API Views
Django REST Framework ViewSets
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

from apps.core.models import Tenant, User
from apps.clientes.models import Cliente, ContatoCliente
from apps.comercial.models import Cotacao
from apps.operacional.models import PedidoFrete, Entrega, EventoRastreamento
from apps.frota.models import Motorista, Veiculo, Manutencao
from apps.ocorrencias.models import Ocorrencia, AnexoOcorrencia, ComentarioOcorrencia

from .serializers import (
    TenantSerializer, UserSerializer, UserCreateSerializer,
    ClienteSerializer, ClienteListSerializer, ContatoClienteSerializer,
    CotacaoSerializer, CotacaoListSerializer, CotacaoAprovarSerializer, CotacaoPerderSerializer,
    PedidoFreteSerializer, PedidoFreteListSerializer, AtribuirMotoristaSerializer,
    AtualizarStatusPedidoSerializer, RastreioPublicoSerializer,
    EntregaSerializer, EventoRastreamentoSerializer,
    MotoristaSerializer, MotoristaListSerializer,
    VeiculoSerializer, VeiculoListSerializer, ManutencaoSerializer,
    OcorrenciaSerializer, OcorrenciaListSerializer, ResolverOcorrenciaSerializer,
    AnexoOcorrenciaSerializer, ComentarioOcorrenciaSerializer,
    DashboardOperacionalSerializer, DashboardComercialSerializer,
)


class TenantFilterMixin:
    """Mixin para filtrar por tenant do usuário logado"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.tenant:
            return queryset.filter(tenant=self.request.user.tenant)
        return queryset.none()
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)


# ==================================================
# CORE VIEWSETS
# ==================================================

class UserViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para gerenciamento de usuários"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Retorna ou atualiza dados do usuário logado"""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        
        # PUT ou PATCH - atualizar perfil
        partial = request.method == 'PATCH'
        serializer = UserSerializer(request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Altera a senha do usuário logado"""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'error': 'old_password e new_password são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not request.user.check_password(old_password):
            return Response(
                {'error': 'Senha atual incorreta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.set_password(new_password)
        request.user.save()
        return Response({'message': 'Senha alterada com sucesso'})


# ==================================================
# CLIENTES VIEWSETS
# ==================================================

class ClienteViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para gerenciamento de clientes"""
    queryset = Cliente.objects.select_related('responsavel').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cidade', 'uf', 'condicao_pagamento', 'is_active']
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj', 'email']
    ordering_fields = ['razao_social', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        return ClienteSerializer
    
    @action(detail=True, methods=['get', 'post'])
    def contatos(self, request, pk=None):
        """Lista ou adiciona contatos do cliente"""
        cliente = self.get_object()
        
        if request.method == 'GET':
            contatos = cliente.contatos.all()
            serializer = ContatoClienteSerializer(contatos, many=True)
            return Response(serializer.data)
        
        serializer = ContatoClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cliente=cliente, tenant=request.user.tenant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==================================================
# COMERCIAL VIEWSETS
# ==================================================

class CotacaoViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para gerenciamento de cotações"""
    queryset = Cotacao.objects.select_related('cliente', 'responsavel').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'cliente', 'modal', 'tipo_carga', 'responsavel']
    search_fields = ['numero', 'cliente__razao_social', 'origem_cidade', 'destino_cidade']
    ordering_fields = ['created_at', 'validade', 'valor_frete']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CotacaoListSerializer
        return CotacaoSerializer
    
    @action(detail=True, methods=['post'])
    def aprovar(self, request, pk=None):
        """Aprova a cotação e opcionalmente gera pedido"""
        cotacao = self.get_object()
        serializer = CotacaoAprovarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if cotacao.status != 'aberta' and cotacao.status != 'em_negociacao':
            return Response(
                {'error': 'Apenas cotações abertas ou em negociação podem ser aprovadas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cotacao.aprovar()
        
        pedido = None
        if serializer.validated_data.get('gerar_pedido', True):
            # Criar pedido automaticamente
            pedido = PedidoFrete.objects.create(
                tenant=cotacao.tenant,
                numero=f"PED-{cotacao.numero}",
                cotacao=cotacao,
                cliente=cotacao.cliente,
                origem_cep=cotacao.origem_cep,
                origem_endereco=cotacao.origem_endereco,
                origem_cidade=cotacao.origem_cidade,
                origem_uf=cotacao.origem_uf,
                destino_cep=cotacao.destino_cep,
                destino_endereco=cotacao.destino_endereco,
                destino_cidade=cotacao.destino_cidade,
                destino_uf=cotacao.destino_uf,
                tipo_carga=cotacao.tipo_carga,
                peso_kg=cotacao.peso_kg,
                cubagem_m3=cotacao.cubagem_m3,
                quantidade_volumes=cotacao.quantidade_volumes,
                valor_mercadoria=cotacao.valor_mercadoria,
                valor_frete=cotacao.valor_frete,
                valor_seguro=cotacao.valor_seguro,
                valor_adicional=cotacao.valor_adicional,
                previsao_entrega=timezone.now().date() + timedelta(days=cotacao.prazo_estimado),
                responsavel=request.user,
            )
        
        return Response({
            'message': 'Cotação aprovada com sucesso',
            'cotacao_id': str(cotacao.id),
            'pedido_id': str(pedido.id) if pedido else None,
            'pedido_numero': pedido.numero if pedido else None,
        })
    
    @action(detail=True, methods=['post'])
    def perder(self, request, pk=None):
        """Marca cotação como perdida"""
        cotacao = self.get_object()
        serializer = CotacaoPerderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cotacao.marcar_perdida(serializer.validated_data['motivo'])
        if serializer.validated_data.get('observacao'):
            cotacao.observacoes = serializer.validated_data['observacao']
            cotacao.save()
        
        return Response({'message': 'Cotação marcada como perdida'})
    
    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        """Duplica a cotação"""
        cotacao = self.get_object()
        
        nova_cotacao = Cotacao.objects.create(
            tenant=cotacao.tenant,
            numero=f"{cotacao.numero}-COPIA",
            cliente=cotacao.cliente,
            origem_cep=cotacao.origem_cep,
            origem_endereco=cotacao.origem_endereco,
            origem_cidade=cotacao.origem_cidade,
            origem_uf=cotacao.origem_uf,
            destino_cep=cotacao.destino_cep,
            destino_endereco=cotacao.destino_endereco,
            destino_cidade=cotacao.destino_cidade,
            destino_uf=cotacao.destino_uf,
            tipo_carga=cotacao.tipo_carga,
            peso_kg=cotacao.peso_kg,
            cubagem_m3=cotacao.cubagem_m3,
            quantidade_volumes=cotacao.quantidade_volumes,
            valor_mercadoria=cotacao.valor_mercadoria,
            modal=cotacao.modal,
            prazo_estimado=cotacao.prazo_estimado,
            valor_frete=cotacao.valor_frete,
            valor_seguro=cotacao.valor_seguro,
            valor_adicional=cotacao.valor_adicional,
            status='aberta',
            validade=timezone.now().date() + timedelta(days=15),
            responsavel=request.user,
        )
        
        serializer = CotacaoSerializer(nova_cotacao)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==================================================
# OPERACIONAL VIEWSETS
# ==================================================

class PedidoFreteViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para gerenciamento de pedidos de frete"""
    queryset = PedidoFrete.objects.select_related(
        'cliente', 'cotacao', 'motorista', 'veiculo', 'responsavel'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'sla_status', 'cliente', 'motorista', 'veiculo']
    search_fields = ['numero', 'cliente__razao_social', 'destinatario_nome']
    ordering_fields = ['created_at', 'data_pedido', 'previsao_entrega']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PedidoFreteListSerializer
        return PedidoFreteSerializer
    
    @action(detail=True, methods=['post'])
    def atribuir_motorista(self, request, pk=None):
        """Atribui motorista e veículo ao pedido"""
        pedido = self.get_object()
        serializer = AtribuirMotoristaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        motorista = Motorista.objects.get(
            id=serializer.validated_data['motorista_id'],
            tenant=request.user.tenant
        )
        veiculo = Veiculo.objects.get(
            id=serializer.validated_data['veiculo_id'],
            tenant=request.user.tenant
        )
        
        pedido.motorista = motorista
        pedido.veiculo = veiculo
        pedido.status = 'aguardando_coleta'
        if serializer.validated_data.get('previsao_coleta'):
            pedido.previsao_coleta = serializer.validated_data['previsao_coleta']
        pedido.save()
        
        # Registrar evento
        EventoRastreamento.objects.create(
            tenant=request.user.tenant,
            pedido=pedido,
            tipo='atribuicao',
            descricao=f'Motorista {motorista.nome} e veículo {veiculo.placa} atribuídos',
            usuario=request.user,
        )
        
        return Response({'message': 'Motorista e veículo atribuídos com sucesso'})
    
    @action(detail=True, methods=['post'])
    def atualizar_status(self, request, pk=None):
        """Atualiza status do pedido"""
        pedido = self.get_object()
        serializer = AtualizarStatusPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        novo_status = serializer.validated_data['status']
        pedido.status = novo_status
        
        if novo_status == 'entregue':
            pedido.data_entrega = timezone.now()
        
        pedido.save()
        pedido.atualizar_sla()
        
        # Registrar evento
        EventoRastreamento.objects.create(
            tenant=request.user.tenant,
            pedido=pedido,
            tipo='status',
            descricao=f'Status alterado para: {pedido.get_status_display()}',
            local=serializer.validated_data.get('observacao', ''),
            latitude=serializer.validated_data.get('latitude'),
            longitude=serializer.validated_data.get('longitude'),
            usuario=request.user,
        )
        
        return Response({'message': f'Status atualizado para {pedido.get_status_display()}'})
    
    @action(detail=True, methods=['get'])
    def rastreio(self, request, pk=None):
        """Retorna dados de rastreio do pedido"""
        pedido = self.get_object()
        serializer = RastreioPublicoSerializer(pedido)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Retorna dados para dashboard operacional"""
        tenant = request.user.tenant
        hoje = timezone.now().date()
        
        pedidos = PedidoFrete.objects.filter(tenant=tenant)
        
        data = {
            'em_transito': pedidos.filter(status='em_transito').count(),
            'entregas_hoje': pedidos.filter(previsao_entrega=hoje).count(),
            'atrasados': pedidos.filter(sla_status='vermelho').exclude(status='entregue').count(),
            'aguardando_coleta': pedidos.filter(status='aguardando_coleta').count(),
            'sla': {
                'verde': pedidos.filter(sla_status='verde').exclude(status='entregue').count(),
                'amarelo': pedidos.filter(sla_status='amarelo').exclude(status='entregue').count(),
                'vermelho': pedidos.filter(sla_status='vermelho').exclude(status='entregue').count(),
            },
            'entregas_semana': [],
            'top_motoristas': [],
        }
        
        serializer = DashboardOperacionalSerializer(data)
        return Response(serializer.data)


class EntregaViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para entregas"""
    queryset = Entrega.objects.select_related('pedido').all()
    serializer_class = EntregaSerializer
    permission_classes = [IsAuthenticated]


# ==================================================
# FROTA VIEWSETS
# ==================================================

class MotoristaViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para motoristas"""
    queryset = Motorista.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'cnh_categoria']
    search_fields = ['nome', 'cpf', 'celular']
    ordering_fields = ['nome', 'cnh_validade']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MotoristaListSerializer
        return MotoristaSerializer
    
    @action(detail=False, methods=['get'])
    def cnh_vencendo(self, request):
        """Lista motoristas com CNH vencendo em 30 dias"""
        limite = timezone.now().date() + timedelta(days=30)
        motoristas = self.get_queryset().filter(
            cnh_validade__lte=limite,
            status='ativo'
        ).order_by('cnh_validade')
        serializer = MotoristaListSerializer(motoristas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        """Lista motoristas disponíveis"""
        motoristas = self.get_queryset().filter(status='ativo')
        serializer = MotoristaListSerializer(motoristas, many=True)
        return Response(serializer.data)


class VeiculoViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para veículos"""
    queryset = Veiculo.objects.select_related('motorista_fixo').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'tipo', 'propriedade']
    search_fields = ['placa', 'marca', 'modelo']
    ordering_fields = ['placa', 'km_atual']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VeiculoListSerializer
        return VeiculoSerializer
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        """Lista veículos disponíveis"""
        veiculos = self.get_queryset().filter(status='disponivel')
        serializer = VeiculoListSerializer(veiculos, many=True)
        return Response(serializer.data)


class ManutencaoViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para manutenções"""
    queryset = Manutencao.objects.select_related('veiculo').all()
    serializer_class = ManutencaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['veiculo', 'tipo', 'status']
    ordering_fields = ['data_entrada', 'data_saida']


# ==================================================
# OCORRENCIAS VIEWSETS
# ==================================================

class OcorrenciaViewSet(TenantFilterMixin, viewsets.ModelViewSet):
    """ViewSet para ocorrências"""
    queryset = Ocorrencia.objects.select_related(
        'pedido', 'registrado_por', 'responsavel'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'tipo', 'prioridade', 'pedido']
    search_fields = ['titulo', 'pedido__numero']
    ordering_fields = ['data_ocorrencia', 'prioridade']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OcorrenciaListSerializer
        return OcorrenciaSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            registrado_por=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """Resolve a ocorrência"""
        ocorrencia = self.get_object()
        serializer = ResolverOcorrenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        ocorrencia.resolver(
            serializer.validated_data['resolucao'],
            usuario=request.user
        )
        
        if serializer.validated_data.get('valor_ressarcimento'):
            ocorrencia.valor_ressarcimento = serializer.validated_data['valor_ressarcimento']
            ocorrencia.save()
        
        return Response({'message': 'Ocorrência resolvida com sucesso'})
    
    @action(detail=True, methods=['post'])
    def comentar(self, request, pk=None):
        """Adiciona comentário à ocorrência"""
        ocorrencia = self.get_object()
        serializer = ComentarioOcorrenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            ocorrencia=ocorrencia,
            tenant=request.user.tenant,
            autor=request.user
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def mudar_status(self, request, pk=None):
        """Muda o status da ocorrência"""
        ocorrencia = self.get_object()
        novo_status = request.data.get('status')
        
        if novo_status not in dict(Ocorrencia.STATUS_CHOICES):
            return Response(
                {'error': 'Status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ocorrencia.status = novo_status
        ocorrencia.save(update_fields=['status', 'updated_at'])
        
        # Adiciona comentário automático sobre a mudança
        ComentarioOcorrencia.objects.create(
            ocorrencia=ocorrencia,
            tenant=request.user.tenant,
            autor=request.user,
            texto=f"Status alterado para: {ocorrencia.get_status_display()}"
        )
        
        return Response({'message': f'Status alterado para {ocorrencia.get_status_display()}'})
    
    @action(detail=True, methods=['post'])
    def atribuir(self, request, pk=None):
        """Atribui um responsável à ocorrência"""
        from apps.core.models import User
        
        ocorrencia = self.get_object()
        responsavel_id = request.data.get('responsavel_id')
        
        if responsavel_id:
            try:
                responsavel = User.objects.get(id=responsavel_id, tenant=request.user.tenant)
                ocorrencia.responsavel = responsavel
                ocorrencia.save(update_fields=['responsavel', 'updated_at'])
                
                # Adiciona comentário automático
                ComentarioOcorrencia.objects.create(
                    ocorrencia=ocorrencia,
                    tenant=request.user.tenant,
                    autor=request.user,
                    texto=f"Ocorrência atribuída para: {responsavel.get_full_name() or responsavel.username}"
                )
                
                return Response({'message': f'Ocorrência atribuída para {responsavel.get_full_name() or responsavel.username}'})
            except User.DoesNotExist:
                return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            ocorrencia.responsavel = None
            ocorrencia.save(update_fields=['responsavel', 'updated_at'])
            return Response({'message': 'Responsável removido'})
    
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """Retorna o histórico/comentários da ocorrência"""
        ocorrencia = self.get_object()
        comentarios = ocorrencia.comentarios.select_related('autor').all()
        serializer = ComentarioOcorrenciaSerializer(comentarios, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get', 'post'])
    def anexos(self, request, pk=None):
        """Lista ou adiciona anexos à ocorrência"""
        ocorrencia = self.get_object()
        
        if request.method == 'GET':
            anexos = ocorrencia.anexos.all()
            serializer = AnexoOcorrenciaSerializer(anexos, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = AnexoOcorrenciaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                ocorrencia=ocorrencia,
                tenant=request.user.tenant
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
