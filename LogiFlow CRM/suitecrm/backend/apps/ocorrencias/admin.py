from django.contrib import admin
from .models import Ocorrencia, AnexoOcorrencia, ComentarioOcorrencia


class AnexoOcorrenciaInline(admin.TabularInline):
    model = AnexoOcorrencia
    extra = 0


class ComentarioOcorrenciaInline(admin.StackedInline):
    model = ComentarioOcorrencia
    extra = 0


@admin.register(Ocorrencia)
class OcorrenciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'tipo', 'titulo', 'prioridade', 'status', 'data_ocorrencia']
    list_filter = ['status', 'tipo', 'prioridade', 'tenant']
    search_fields = ['titulo', 'descricao', 'pedido__numero']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'data_ocorrencia'
    inlines = [AnexoOcorrenciaInline, ComentarioOcorrenciaInline]
    
    fieldsets = (
        ('Identificação', {'fields': ('tenant', 'pedido', 'entrega')}),
        ('Ocorrência', {'fields': ('tipo', 'titulo', 'descricao', 'prioridade')}),
        ('Data/Local', {'fields': ('data_ocorrencia', 'local_ocorrencia')}),
        ('Status', {'fields': ('status', 'data_resolucao', 'resolucao')}),
        ('Valores', {'fields': ('valor_prejuizo', 'valor_ressarcimento')}),
        ('Responsáveis', {'fields': ('registrado_por', 'responsavel')}),
    )
