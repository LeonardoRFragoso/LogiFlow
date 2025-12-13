from django.contrib import admin
from .models import PedidoFrete, Entrega, EventoRastreamento


class EntregaInline(admin.StackedInline):
    model = Entrega
    extra = 0


class EventoRastreamentoInline(admin.TabularInline):
    model = EventoRastreamento
    extra = 0


@admin.register(PedidoFrete)
class PedidoFreteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'rota', 'motorista', 'status', 'sla_status', 'previsao_entrega']
    list_filter = ['status', 'sla_status', 'tenant']
    search_fields = ['numero', 'cliente__razao_social', 'motorista__nome']
    readonly_fields = ['numero', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [EntregaInline, EventoRastreamentoInline]
    
    fieldsets = (
        ('Identificação', {'fields': ('tenant', 'numero', 'cotacao', 'cliente')}),
        ('Rota', {'fields': ('origem_cidade', 'origem_uf', 'destino_cidade', 'destino_uf', 'destino_cep', 'destino_endereco')}),
        ('Carga', {'fields': ('tipo_carga', 'peso_kg', 'volume_m3', 'valor_mercadoria')}),
        ('Valores', {'fields': ('valor_frete', 'valor_pedagio', 'valor_total')}),
        ('Operacional', {'fields': ('motorista', 'veiculo', 'status', 'sla_status')}),
        ('Datas', {'fields': ('data_coleta', 'previsao_entrega', 'data_entrega_real')}),
        ('Documentos', {'fields': ('cte_numero', 'nf_numero')}),
    )

    def rota(self, obj):
        return f"{obj.origem_cidade}/{obj.origem_uf} → {obj.destino_cidade}/{obj.destino_uf}"


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'status']
    list_filter = ['status', 'pedido__tenant']
    search_fields = ['pedido__numero']
