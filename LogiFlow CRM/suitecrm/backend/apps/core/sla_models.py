"""
LogiFlow CRM - SLA Configuration Models
Modelos para configuração de SLA
"""

from django.db import models
from django.core.validators import MinValueValidator
from .models import TenantModel


class SLAConfig(TenantModel):
    """Configuração global de SLA do tenant"""
    
    # Limites padrão em dias
    limite_verde = models.PositiveIntegerField(
        'Limite Verde (dias)',
        default=2,
        help_text='Pedidos com mais dias que este valor são considerados "No Prazo"'
    )
    limite_amarelo = models.PositiveIntegerField(
        'Limite Amarelo (dias)',
        default=1,
        help_text='Pedidos com dias entre amarelo e verde são considerados "Atenção"'
    )
    # Vermelho = menos que limite_amarelo ou atrasado
    
    # Configurações adicionais
    considerar_dias_uteis = models.BooleanField(
        'Considerar apenas dias úteis',
        default=False
    )
    alertar_sla_amarelo = models.BooleanField(
        'Enviar alerta quando SLA ficar amarelo',
        default=True
    )
    alertar_sla_vermelho = models.BooleanField(
        'Enviar alerta quando SLA ficar vermelho',
        default=True
    )
    
    class Meta:
        verbose_name = 'Configuração de SLA'
        verbose_name_plural = 'Configurações de SLA'
    
    def __str__(self):
        return f"SLA Config - {self.tenant.name}"


class SLAClienteConfig(TenantModel):
    """Configuração de SLA específica por cliente (VIP)"""
    
    cliente = models.OneToOneField(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name='sla_config',
        verbose_name='Cliente'
    )
    
    # Limites customizados
    limite_verde = models.PositiveIntegerField(
        'Limite Verde (dias)',
        validators=[MinValueValidator(1)]
    )
    limite_amarelo = models.PositiveIntegerField(
        'Limite Amarelo (dias)',
        validators=[MinValueValidator(0)]
    )
    
    # Prioridade
    PRIORIDADE_CHOICES = [
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('vip', 'VIP'),
    ]
    prioridade = models.CharField(
        'Prioridade',
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default='normal'
    )
    
    # Desconto no tempo de SLA (em horas)
    bonus_horas = models.PositiveIntegerField(
        'Bônus de horas (reduz SLA)',
        default=0,
        help_text='Horas a serem subtraídas do prazo para clientes VIP'
    )
    
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        verbose_name = 'SLA por Cliente'
        verbose_name_plural = 'SLAs por Cliente'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SLA {self.cliente.razao_social} - {self.prioridade}"


class SLARotaConfig(TenantModel):
    """Configuração de SLA por rota (origem/destino)"""
    
    nome = models.CharField('Nome da Rota', max_length=100)
    
    # Origem
    origem_uf = models.CharField('UF Origem', max_length=2)
    origem_cidade = models.CharField('Cidade Origem', max_length=100, blank=True)
    
    # Destino
    destino_uf = models.CharField('UF Destino', max_length=2)
    destino_cidade = models.CharField('Cidade Destino', max_length=100, blank=True)
    
    # Tempo adicional para esta rota
    dias_adicionais = models.PositiveIntegerField(
        'Dias adicionais',
        default=0,
        help_text='Dias extras a serem adicionados ao prazo padrão'
    )
    
    # Limites customizados (opcional - se não preenchido, usa o padrão + dias_adicionais)
    limite_verde_customizado = models.PositiveIntegerField(
        'Limite Verde customizado (dias)',
        null=True, blank=True
    )
    limite_amarelo_customizado = models.PositiveIntegerField(
        'Limite Amarelo customizado (dias)',
        null=True, blank=True
    )
    
    # Prazo médio de entrega para esta rota
    prazo_medio_dias = models.PositiveIntegerField(
        'Prazo médio de entrega (dias)',
        default=3,
        help_text='Tempo médio de entrega para esta rota'
    )
    
    ativo = models.BooleanField('Ativo', default=True)
    
    class Meta:
        verbose_name = 'SLA por Rota'
        verbose_name_plural = 'SLAs por Rota'
        unique_together = ['tenant', 'origem_uf', 'origem_cidade', 'destino_uf', 'destino_cidade']
        ordering = ['nome']
    
    def __str__(self):
        origem = f"{self.origem_cidade}/{self.origem_uf}" if self.origem_cidade else self.origem_uf
        destino = f"{self.destino_cidade}/{self.destino_uf}" if self.destino_cidade else self.destino_uf
        return f"{origem} → {destino} (+{self.dias_adicionais}d)"
