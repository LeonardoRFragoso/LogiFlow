"""
LogiFlow CRM - SLA Serializers
"""

from rest_framework import serializers
from .sla_models import SLAConfig, SLAClienteConfig, SLARotaConfig


class SLAConfigSerializer(serializers.ModelSerializer):
    """Serializer para configuração global de SLA"""
    
    class Meta:
        model = SLAConfig
        fields = [
            'id', 'limite_verde', 'limite_amarelo',
            'considerar_dias_uteis', 'alertar_sla_amarelo', 'alertar_sla_vermelho',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SLAClienteConfigSerializer(serializers.ModelSerializer):
    """Serializer para SLA por cliente"""
    
    cliente_nome = serializers.CharField(source='cliente.razao_social', read_only=True)
    
    class Meta:
        model = SLAClienteConfig
        fields = [
            'id', 'cliente', 'cliente_nome', 'limite_verde', 'limite_amarelo',
            'prioridade', 'bonus_horas', 'observacoes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SLARotaConfigSerializer(serializers.ModelSerializer):
    """Serializer para SLA por rota"""
    
    rota_display = serializers.SerializerMethodField()
    
    class Meta:
        model = SLARotaConfig
        fields = [
            'id', 'nome', 'origem_uf', 'origem_cidade', 'destino_uf', 'destino_cidade',
            'dias_adicionais', 'limite_verde_customizado', 'limite_amarelo_customizado',
            'prazo_medio_dias', 'ativo', 'rota_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'rota_display', 'created_at', 'updated_at']
    
    def get_rota_display(self, obj):
        origem = f"{obj.origem_cidade}/{obj.origem_uf}" if obj.origem_cidade else obj.origem_uf
        destino = f"{obj.destino_cidade}/{obj.destino_uf}" if obj.destino_cidade else obj.destino_uf
        return f"{origem} → {destino}"
