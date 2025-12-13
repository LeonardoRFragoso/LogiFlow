from rest_framework import serializers
from .models import CTe, MDFe


class CTeListSerializer(serializers.ModelSerializer):
    pedido_numero = serializers.CharField(source='pedido.numero', read_only=True)
    
    class Meta:
        model = CTe
        fields = ['id', 'numero', 'pedido', 'pedido_numero', 'valor_total', 'status', 'chave', 'data_emissao', 'pdf_url']


class CTeDetailSerializer(serializers.ModelSerializer):
    pedido_numero = serializers.CharField(source='pedido.numero', read_only=True)
    
    class Meta:
        model = CTe
        fields = '__all__'
        read_only_fields = ['numero', 'chave', 'protocolo', 'focusnfe_id', 'focusnfe_ref', 'xml_autorizacao', 'data_autorizacao']


class CTeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CTe
        fields = ['pedido', 'valor_total', 'valor_servico', 'valor_carga', 'icms_base', 'icms_aliquota', 'icms_valor']


class MDFeListSerializer(serializers.ModelSerializer):
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    motorista_nome = serializers.CharField(source='motorista.nome', read_only=True)
    
    class Meta:
        model = MDFe
        fields = ['id', 'numero', 'veiculo', 'veiculo_placa', 'motorista', 'motorista_nome', 'uf_inicio', 'uf_fim', 'status', 'pdf_url']


class MDFeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MDFe
        fields = '__all__'
        read_only_fields = ['numero', 'chave', 'protocolo', 'focusnfe_id', 'focusnfe_ref']


class MDFeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MDFe
        fields = ['veiculo', 'motorista', 'uf_inicio', 'uf_fim', 'ctes']
