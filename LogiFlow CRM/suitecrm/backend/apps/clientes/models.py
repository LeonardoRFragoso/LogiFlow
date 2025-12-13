"""
LogiFlow CRM - Clientes Models
Gestão de clientes (embarcadores/shippers)
"""

from django.db import models
from apps.core.models import TenantModel


class Cliente(TenantModel):
    """Cliente/Embarcador que contrata os serviços de frete"""
    
    # Dados básicos
    razao_social = models.CharField('Razão Social', max_length=255)
    nome_fantasia = models.CharField('Nome Fantasia', max_length=255, blank=True)
    cnpj = models.CharField('CNPJ', max_length=18, db_index=True)
    inscricao_estadual = models.CharField('Inscrição Estadual', max_length=20, blank=True)
    
    # Contato principal
    contato_nome = models.CharField('Nome do Contato', max_length=150, blank=True)
    email = models.EmailField('E-mail', blank=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    celular = models.CharField('Celular', max_length=20, blank=True)
    
    # Endereço
    cep = models.CharField('CEP', max_length=10, blank=True)
    logradouro = models.CharField('Logradouro', max_length=255, blank=True)
    numero = models.CharField('Número', max_length=20, blank=True)
    complemento = models.CharField('Complemento', max_length=100, blank=True)
    bairro = models.CharField('Bairro', max_length=100, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    uf = models.CharField('UF', max_length=2, blank=True)
    
    # Comercial
    CONDICAO_PAGAMENTO_CHOICES = [
        ('a_vista', 'À Vista'),
        ('7_dias', '7 dias'),
        ('14_dias', '14 dias'),
        ('21_dias', '21 dias'),
        ('28_dias', '28 dias'),
        ('30_dias', '30 dias'),
        ('45_dias', '45 dias'),
        ('60_dias', '60 dias'),
        ('faturado', 'Faturado'),
    ]
    condicao_pagamento = models.CharField(
        'Condição de Pagamento', 
        max_length=20, 
        choices=CONDICAO_PAGAMENTO_CHOICES,
        default='30_dias'
    )
    limite_credito = models.DecimalField(
        'Limite de Crédito', 
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    
    # Responsável
    responsavel = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='clientes_responsavel',
        verbose_name='Responsável'
    )
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        unique_together = ['tenant', 'cnpj']
        ordering = ['razao_social']
    
    def __str__(self):
        return self.nome_fantasia or self.razao_social
    
    @property
    def endereco_completo(self):
        partes = [self.logradouro, self.numero, self.bairro, self.cidade, self.uf]
        return ', '.join(p for p in partes if p)


class ContatoCliente(TenantModel):
    """Contatos adicionais do cliente"""
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='contatos',
        verbose_name='Cliente'
    )
    nome = models.CharField('Nome', max_length=150)
    cargo = models.CharField('Cargo', max_length=100, blank=True)
    email = models.EmailField('E-mail', blank=True)
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    celular = models.CharField('Celular', max_length=20, blank=True)
    is_principal = models.BooleanField('Contato Principal', default=False)
    
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
    
    def __str__(self):
        return f"{self.nome} ({self.cliente})"
