from django.contrib import admin
from .models import CTe, MDFe


@admin.register(CTe)
class CTeAdmin(admin.ModelAdmin):
    list_display = ['numero', 'pedido', 'valor_total', 'status', 'data_emissao', 'chave']
    list_filter = ['status', 'tenant']
    search_fields = ['numero', 'chave', 'pedido__numero']
    readonly_fields = ['chave', 'protocolo', 'focusnfe_id', 'focusnfe_ref', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(MDFe)
class MDFeAdmin(admin.ModelAdmin):
    list_display = ['numero', 'veiculo', 'motorista', 'uf_inicio', 'uf_fim', 'status']
    list_filter = ['status', 'tenant']
    search_fields = ['numero', 'chave']
    readonly_fields = ['chave', 'protocolo', 'focusnfe_id', 'focusnfe_ref', 'created_at']
    filter_horizontal = ['ctes']
