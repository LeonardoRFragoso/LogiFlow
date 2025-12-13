from django.contrib import admin
from .models import Cotacao


@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'rota', 'valor_total', 'status', 'validade', 'created_at']
    list_filter = ['status', 'modal', 'tenant']
    search_fields = ['numero', 'cliente__razao_social']
    readonly_fields = ['numero', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Identificação', {'fields': ('tenant', 'numero', 'cliente', 'contato')}),
        ('Rota', {'fields': ('origem_cidade', 'origem_uf', 'destino_cidade', 'destino_uf')}),
        ('Carga', {'fields': ('tipo_carga', 'peso_kg', 'volume_m3', 'valor_mercadoria', 'modal')}),
        ('Valores', {'fields': ('valor_frete', 'valor_pedagio', 'valor_seguro', 'valor_total')}),
        ('Status', {'fields': ('status', 'validade', 'prazo_estimado_dias', 'motivo_perda')}),
        ('Responsável', {'fields': ('criado_por',)}),
    )

    def rota(self, obj):
        return f"{obj.origem_cidade}/{obj.origem_uf} → {obj.destino_cidade}/{obj.destino_uf}"
