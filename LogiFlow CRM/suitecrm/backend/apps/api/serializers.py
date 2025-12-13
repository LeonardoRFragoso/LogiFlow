"""
LogiFlow CRM - API Serializers
Django REST Framework Serializers
"""

from rest_framework import serializers
from apps.core.models import Tenant, User
from apps.clientes.models import Cliente, ContatoCliente
from apps.comercial.models import Cotacao
from apps.operacional.models import PedidoFrete, Entrega, EventoRastreamento
from apps.frota.models import Motorista, Veiculo, Manutencao
from apps.ocorrencias.models import Ocorrencia, AnexoOcorrencia, ComentarioOcorrencia


# ==================================================
# CORE SERIALIZERS
# ==================================================

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'slug', 'cnpj', 'email', 'phone', 'plan', 
                  'max_users', 'storage_limit_mb', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'role', 'tenant', 'tenant_name', 'is_active']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 
                  'phone', 'role', 'tenant']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ==================================================
# CLIENTES SERIALIZERS
# ==================================================

class ContatoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoCliente
        fields = ['id', 'nome', 'cargo', 'email', 'telefone', 'celular', 'is_principal']
        read_only_fields = ['id']


class ClienteListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""
    endereco_completo = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'razao_social', 'nome_fantasia', 'cnpj', 'cidade', 'uf',
                  'telefone', 'email', 'condicao_pagamento', 'is_active', 'endereco_completo']


class ClienteSerializer(serializers.ModelSerializer):
    """Serializer completo para detalhe/criação"""
    contatos = ContatoClienteSerializer(many=True, read_only=True)
    endereco_completo = serializers.ReadOnlyField()
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


# ==================================================
# COMERCIAL SERIALIZERS
# ==================================================

class CotacaoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""
    cliente_nome = serializers.CharField(source='cliente.nome_fantasia', read_only=True)
    valor_total = serializers.ReadOnlyField()
    rota = serializers.ReadOnlyField()
    is_expirada = serializers.ReadOnlyField()
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    
    class Meta:
        model = Cotacao
        fields = ['id', 'numero', 'cliente', 'cliente_nome', 'origem_cidade', 'origem_uf',
                  'destino_cidade', 'destino_uf', 'rota', 'tipo_carga', 'peso_kg',
                  'valor_frete', 'valor_total', 'status', 'validade', 'is_expirada',
                  'responsavel_nome', 'created_at']


class CotacaoSerializer(serializers.ModelSerializer):
    """Serializer completo para detalhe/criação"""
    cliente_nome = serializers.CharField(source='cliente.nome_fantasia', read_only=True)
    valor_total = serializers.ReadOnlyField()
    rota = serializers.ReadOnlyField()
    is_expirada = serializers.ReadOnlyField()
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    
    class Meta:
        model = Cotacao
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


class CotacaoAprovarSerializer(serializers.Serializer):
    """Serializer para ação de aprovar cotação"""
    gerar_pedido = serializers.BooleanField(default=True)


class CotacaoPerderSerializer(serializers.Serializer):
    """Serializer para ação de marcar como perdida"""
    motivo = serializers.ChoiceField(choices=Cotacao.MOTIVO_PERDA_CHOICES)
    observacao = serializers.CharField(required=False, allow_blank=True)


# ==================================================
# OPERACIONAL SERIALIZERS
# ==================================================

class EventoRastreamentoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    class Meta:
        model = EventoRastreamento
        fields = ['id', 'tipo', 'descricao', 'local', 'latitude', 'longitude',
                  'data_evento', 'usuario', 'usuario_nome']
        read_only_fields = ['id']


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


class PedidoFreteListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem"""
    cliente_nome = serializers.CharField(source='cliente.nome_fantasia', read_only=True)
    motorista_nome = serializers.CharField(source='motorista.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    valor_total = serializers.ReadOnlyField()
    rota = serializers.ReadOnlyField()
    
    class Meta:
        model = PedidoFrete
        fields = ['id', 'numero', 'data_pedido', 'cliente', 'cliente_nome',
                  'origem_cidade', 'origem_uf', 'destino_cidade', 'destino_uf', 'rota',
                  'motorista', 'motorista_nome', 'veiculo', 'veiculo_placa',
                  'status', 'sla_status', 'previsao_entrega', 'valor_total', 'created_at']


class PedidoFreteSerializer(serializers.ModelSerializer):
    """Serializer completo"""
    cliente_nome = serializers.CharField(source='cliente.nome_fantasia', read_only=True)
    motorista_nome = serializers.CharField(source='motorista.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    cotacao_numero = serializers.CharField(source='cotacao.numero', read_only=True)
    valor_total = serializers.ReadOnlyField()
    lucro_estimado = serializers.ReadOnlyField()
    rota = serializers.ReadOnlyField()
    eventos = EventoRastreamentoSerializer(many=True, read_only=True)
    
    class Meta:
        model = PedidoFrete
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


class AtribuirMotoristaSerializer(serializers.Serializer):
    """Serializer para atribuir motorista e veículo"""
    motorista_id = serializers.UUIDField()
    veiculo_id = serializers.UUIDField()
    previsao_coleta = serializers.DateTimeField(required=False)


class AtualizarStatusPedidoSerializer(serializers.Serializer):
    """Serializer para atualizar status do pedido"""
    status = serializers.ChoiceField(choices=PedidoFrete.STATUS_CHOICES)
    observacao = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=7, required=False)


class RastreioPublicoSerializer(serializers.ModelSerializer):
    """Serializer para rastreio público (sem dados sensíveis)"""
    eventos = EventoRastreamentoSerializer(many=True, read_only=True)
    rota = serializers.ReadOnlyField()
    
    class Meta:
        model = PedidoFrete
        fields = ['numero', 'status', 'sla_status', 'origem_cidade', 'origem_uf',
                  'destino_cidade', 'destino_uf', 'rota', 'previsao_entrega',
                  'data_entrega', 'eventos']


# ==================================================
# FROTA SERIALIZERS
# ==================================================

class MotoristaListSerializer(serializers.ModelSerializer):
    cnh_vencendo = serializers.ReadOnlyField()
    cnh_vencida = serializers.ReadOnlyField()
    dias_para_vencer_cnh = serializers.ReadOnlyField()
    
    class Meta:
        model = Motorista
        fields = ['id', 'nome', 'cpf', 'celular', 'cnh_categoria', 'cnh_validade',
                  'status', 'cnh_vencendo', 'cnh_vencida', 'dias_para_vencer_cnh']


class MotoristaSerializer(serializers.ModelSerializer):
    cnh_vencendo = serializers.ReadOnlyField()
    cnh_vencida = serializers.ReadOnlyField()
    dias_para_vencer_cnh = serializers.ReadOnlyField()
    
    class Meta:
        model = Motorista
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


class VeiculoListSerializer(serializers.ModelSerializer):
    motorista_fixo_nome = serializers.CharField(source='motorista_fixo.nome', read_only=True)
    documento_vencendo = serializers.ReadOnlyField()
    
    class Meta:
        model = Veiculo
        fields = ['id', 'placa', 'tipo', 'marca', 'modelo', 'capacidade_kg',
                  'status', 'motorista_fixo', 'motorista_fixo_nome', 
                  'km_atual', 'documento_vencendo', 'propriedade']


class VeiculoSerializer(serializers.ModelSerializer):
    motorista_fixo_nome = serializers.CharField(source='motorista_fixo.nome', read_only=True)
    documento_vencendo = serializers.ReadOnlyField()
    
    class Meta:
        model = Veiculo
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


class ManutencaoSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    
    class Meta:
        model = Manutencao
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


# ==================================================
# OCORRENCIAS SERIALIZERS
# ==================================================

class AnexoOcorrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoOcorrencia
        fields = ['id', 'tipo', 'titulo', 'arquivo', 'created_at']
        read_only_fields = ['id', 'created_at']


class ComentarioOcorrenciaSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(source='autor.get_full_name', read_only=True)
    
    class Meta:
        model = ComentarioOcorrencia
        fields = ['id', 'autor', 'autor_nome', 'texto', 'created_at']
        read_only_fields = ['id', 'autor', 'created_at']


class OcorrenciaListSerializer(serializers.ModelSerializer):
    pedido_numero = serializers.CharField(source='pedido.numero', read_only=True)
    registrado_por_nome = serializers.CharField(source='registrado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Ocorrencia
        fields = ['id', 'pedido', 'pedido_numero', 'tipo', 'titulo', 'status',
                  'prioridade', 'data_ocorrencia', 'registrado_por_nome']


class OcorrenciaSerializer(serializers.ModelSerializer):
    pedido_numero = serializers.CharField(source='pedido.numero', read_only=True)
    registrado_por_nome = serializers.CharField(source='registrado_por.get_full_name', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.get_full_name', read_only=True)
    anexos = AnexoOcorrenciaSerializer(many=True, read_only=True)
    comentarios = ComentarioOcorrenciaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ocorrencia
        fields = '__all__'
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at']


class ResolverOcorrenciaSerializer(serializers.Serializer):
    """Serializer para resolver uma ocorrência"""
    resolucao = serializers.CharField()
    valor_ressarcimento = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False
    )


# ==================================================
# DASHBOARD SERIALIZERS
# ==================================================

class DashboardOperacionalSerializer(serializers.Serializer):
    """Serializer para dados do dashboard operacional"""
    em_transito = serializers.IntegerField()
    entregas_hoje = serializers.IntegerField()
    atrasados = serializers.IntegerField()
    aguardando_coleta = serializers.IntegerField()
    sla = serializers.DictField()
    entregas_semana = serializers.ListField()
    top_motoristas = serializers.ListField()


class DashboardComercialSerializer(serializers.Serializer):
    """Serializer para dados do dashboard comercial"""
    cotacoes_mes = serializers.IntegerField()
    cotacoes_abertas = serializers.IntegerField()
    taxa_conversao = serializers.FloatField()
    ticket_medio = serializers.DecimalField(max_digits=12, decimal_places=2)
    faturamento_mes = serializers.DecimalField(max_digits=12, decimal_places=2)
    funil = serializers.ListField()
