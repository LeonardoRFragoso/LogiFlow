from django.contrib import admin
from .models import Cliente, ContatoCliente


class ContatoClienteInline(admin.TabularInline):
    model = ContatoCliente
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'nome_fantasia', 'cnpj', 'cidade', 'uf']
    list_filter = ['uf', 'tenant']
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ContatoClienteInline]
    
    fieldsets = (
        ('Identificação', {'fields': ('tenant', 'razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual')}),
        ('Contato', {'fields': ('contato_nome', 'email', 'telefone', 'celular')}),
        ('Endereço', {'fields': ('cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf')}),
        ('Comercial', {'fields': ('condicao_pagamento', 'limite_credito', 'responsavel', 'is_active')}),
        ('Observações', {'fields': ('observacoes',)}),
    )
