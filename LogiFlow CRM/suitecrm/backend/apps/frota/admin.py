from django.contrib import admin
from .models import Motorista, Veiculo, Manutencao


class ManutencaoInline(admin.TabularInline):
    model = Manutencao
    extra = 0


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'cnh_categoria', 'cnh_validade', 'status', 'cnh_vencida', 'cnh_vencendo']
    list_filter = ['status', 'cnh_categoria', 'tenant']
    search_fields = ['nome', 'cpf', 'cnh_numero']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Dados Pessoais', {'fields': ('tenant', 'nome', 'cpf', 'rg', 'data_nascimento')}),
        ('CNH', {'fields': ('cnh_numero', 'cnh_categoria', 'cnh_validade')}),
        ('Contato', {'fields': ('telefone', 'celular', 'email')}),
        ('Endereço', {'fields': ('cep', 'endereco', 'cidade', 'uf')}),
        ('Situação', {'fields': ('status', 'data_admissao', 'data_demissao', 'usuario')}),
        ('Observações', {'fields': ('observacoes',)}),
    )


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'tipo', 'marca', 'modelo', 'km_atual', 'status', 'motorista_fixo']
    list_filter = ['status', 'tipo', 'propriedade', 'tenant']
    search_fields = ['placa', 'renavam', 'chassi']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ManutencaoInline]
    
    fieldsets = (
        ('Identificação', {'fields': ('tenant', 'placa', 'renavam', 'chassi')}),
        ('Características', {'fields': ('tipo', 'marca', 'modelo', 'ano_fabricacao', 'ano_modelo', 'cor')}),
        ('Capacidade', {'fields': ('capacidade_kg', 'capacidade_m3')}),
        ('Documentação', {'fields': ('licenciamento_validade', 'seguro_validade', 'seguro_apolice')}),
        ('Operacional', {'fields': ('motorista_fixo', 'km_atual', 'status')}),
        ('Propriedade', {'fields': ('propriedade', 'proprietario_nome', 'proprietario_documento')}),
        ('Observações', {'fields': ('observacoes',)}),
    )


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'tipo', 'descricao', 'valor']
    list_filter = ['tipo']
    search_fields = ['veiculo__placa', 'descricao']
