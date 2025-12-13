"""
LogiFlow CRM - Comercial Models
Cotações e gestão comercial
"""

from django.db import models
from django.utils import timezone
from apps.core.models import TenantModel
from decimal import Decimal


class Cotacao(TenantModel):
    """Cotação de frete para cliente"""
    
    # Identificação
    numero = models.CharField('Número', max_length=20, db_index=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.numero:
            from django.utils import timezone
            import random
            self.numero = f"COT-{timezone.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)
    
    # Cliente
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='cotacoes',
        verbose_name='Cliente'
    )
    contato_nome = models.CharField('Nome do Contato', max_length=150, blank=True)
    contato_telefone = models.CharField('Telefone do Contato', max_length=20, blank=True)
    contato_email = models.EmailField('E-mail do Contato', blank=True)
    
    # Origem
    origem_cep = models.CharField('CEP Origem', max_length=10, blank=True)
    origem_endereco = models.CharField('Endereço Origem', max_length=255, blank=True)
    origem_cidade = models.CharField('Cidade Origem', max_length=100)
    origem_uf = models.CharField('UF Origem', max_length=2)
    
    # Destino
    destino_cep = models.CharField('CEP Destino', max_length=10, blank=True)
    destino_endereco = models.CharField('Endereço Destino', max_length=255, blank=True)
    destino_cidade = models.CharField('Cidade Destino', max_length=100)
    destino_uf = models.CharField('UF Destino', max_length=2)
    
    # Carga
    TIPO_CARGA_CHOICES = [
        ('geral', 'Carga Geral'),
        ('fracionada', 'Fracionada'),
        ('lotacao', 'Lotação Completa'),
        ('container', 'Container'),
        ('granel_solido', 'Granel Sólido'),
        ('granel_liquido', 'Granel Líquido'),
        ('refrigerada', 'Refrigerada'),
        ('perigosa', 'Carga Perigosa'),
        ('viva', 'Carga Viva'),
        ('indivisivel', 'Carga Indivisível'),
        ('mudanca', 'Mudança'),
    ]
    tipo_carga = models.CharField(
        'Tipo de Carga', 
        max_length=30, 
        choices=TIPO_CARGA_CHOICES,
        default='geral'
    )
    peso_kg = models.DecimalField('Peso (kg)', max_digits=10, decimal_places=2)
    cubagem_m3 = models.DecimalField('Cubagem (m³)', max_digits=10, decimal_places=3, blank=True, null=True)
    quantidade_volumes = models.PositiveIntegerField('Qtd. Volumes', default=1)
    valor_mercadoria = models.DecimalField(
        'Valor da Mercadoria', 
        max_digits=12, 
        decimal_places=2, 
        blank=True, null=True
    )
    descricao_carga = models.TextField('Descrição da Carga', blank=True)
    
    # Modal e Prazo
    MODAL_CHOICES = [
        ('rodoviario', 'Rodoviário'),
        ('aereo', 'Aéreo'),
        ('maritimo', 'Marítimo'),
        ('ferroviario', 'Ferroviário'),
        ('fluvial', 'Fluvial'),
        ('multimodal', 'Multimodal'),
    ]
    modal = models.CharField('Modal', max_length=20, choices=MODAL_CHOICES, default='rodoviario')
    prazo_estimado = models.PositiveIntegerField('Prazo Estimado (dias)')
    
    # Valores
    valor_frete = models.DecimalField('Valor do Frete', max_digits=12, decimal_places=2)
    valor_seguro = models.DecimalField('Valor do Seguro', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    valor_adicional = models.DecimalField('Valor Adicional', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Status
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_negociacao', 'Em Negociação'),
        ('aprovada', 'Aprovada'),
        ('perdida', 'Perdida'),
        ('expirada', 'Expirada'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='aberta')
    validade = models.DateField('Válido Até')
    
    MOTIVO_PERDA_CHOICES = [
        ('preco', 'Preço'),
        ('prazo', 'Prazo'),
        ('concorrente', 'Perdeu para Concorrente'),
        ('desistencia', 'Cliente Desistiu'),
        ('sem_retorno', 'Sem Retorno do Cliente'),
        ('fora_area', 'Fora da Área de Atuação'),
        ('outro', 'Outro'),
    ]
    motivo_perda = models.CharField(
        'Motivo da Perda', 
        max_length=30, 
        choices=MOTIVO_PERDA_CHOICES,
        blank=True
    )
    
    observacoes = models.TextField('Observações', blank=True)
    
    # Responsável
    responsavel = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='cotacoes',
        verbose_name='Responsável'
    )
    
    class Meta:
        verbose_name = 'Cotação'
        verbose_name_plural = 'Cotações'
        unique_together = ['tenant', 'numero']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Cotação {self.numero} - {self.cliente}"
    
    @property
    def valor_total(self):
        return self.valor_frete + self.valor_seguro + self.valor_adicional
    
    @property
    def is_expirada(self):
        return self.validade < timezone.now().date() and self.status == 'aberta'
    
    @property
    def rota(self):
        return f"{self.origem_cidade}/{self.origem_uf} → {self.destino_cidade}/{self.destino_uf}"
    
    def aprovar(self):
        """Aprova a cotação e prepara para criar pedido"""
        self.status = 'aprovada'
        self.save()
    
    def marcar_perdida(self, motivo='outro'):
        """Marca cotação como perdida"""
        self.status = 'perdida'
        self.motivo_perda = motivo
        self.save()
