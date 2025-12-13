"""
LogiFlow CRM - Operacional Models
Pedidos de frete, entregas e rastreamento
"""

from django.db import models
from django.utils import timezone
from apps.core.models import TenantModel
from decimal import Decimal


class PedidoFrete(TenantModel):
    """Pedido de frete confirmado (gerado a partir de cotação aprovada)"""
    
    # Identificação
    numero = models.CharField('Número do Pedido', max_length=20, db_index=True, blank=True)
    data_pedido = models.DateField('Data do Pedido', default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.numero:
            import random
            self.numero = f"PED-{timezone.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)
    
    # Origem (cotação)
    cotacao = models.ForeignKey(
        'comercial.Cotacao',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='pedidos',
        verbose_name='Cotação'
    )
    
    # Cliente
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name='Cliente'
    )
    
    # Origem
    origem_cep = models.CharField('CEP Origem', max_length=10, blank=True)
    origem_endereco = models.CharField('Endereço Origem', max_length=255)
    origem_cidade = models.CharField('Cidade Origem', max_length=100)
    origem_uf = models.CharField('UF Origem', max_length=2)
    remetente_nome = models.CharField('Nome do Remetente', max_length=200, blank=True)
    remetente_telefone = models.CharField('Telefone Remetente', max_length=20, blank=True)
    
    # Destino
    destino_cep = models.CharField('CEP Destino', max_length=10, blank=True)
    destino_endereco = models.CharField('Endereço Destino', max_length=255)
    destino_cidade = models.CharField('Cidade Destino', max_length=100)
    destino_uf = models.CharField('UF Destino', max_length=2)
    destinatario_nome = models.CharField('Nome do Destinatário', max_length=200)
    destinatario_telefone = models.CharField('Telefone Destinatário', max_length=20, blank=True)
    destinatario_documento = models.CharField('CPF/CNPJ Destinatário', max_length=18, blank=True)
    
    # Carga
    tipo_carga = models.CharField('Tipo de Carga', max_length=30)
    peso_kg = models.DecimalField('Peso (kg)', max_digits=10, decimal_places=2)
    cubagem_m3 = models.DecimalField('Cubagem (m³)', max_digits=10, decimal_places=3, blank=True, null=True)
    quantidade_volumes = models.PositiveIntegerField('Qtd. Volumes', default=1)
    valor_mercadoria = models.DecimalField('Valor da Mercadoria', max_digits=12, decimal_places=2, blank=True, null=True)
    descricao_carga = models.TextField('Descrição da Carga', blank=True)
    
    # Valores
    valor_frete = models.DecimalField('Valor do Frete', max_digits=12, decimal_places=2)
    valor_seguro = models.DecimalField('Valor do Seguro', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    valor_adicional = models.DecimalField('Valor Adicional', max_digits=12, decimal_places=2, default=Decimal('0.00'))
    custo_estimado = models.DecimalField('Custo Estimado', max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Atribuição
    motorista = models.ForeignKey(
        'frota.Motorista',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='pedidos',
        verbose_name='Motorista'
    )
    veiculo = models.ForeignKey(
        'frota.Veiculo',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='pedidos',
        verbose_name='Veículo'
    )
    
    # Datas operacionais
    previsao_coleta = models.DateTimeField('Previsão de Coleta', blank=True, null=True)
    data_coleta = models.DateTimeField('Data da Coleta', blank=True, null=True)
    previsao_entrega = models.DateField('Previsão de Entrega')
    data_entrega = models.DateTimeField('Data da Entrega', blank=True, null=True)
    
    # Status
    STATUS_CHOICES = [
        ('em_planejamento', 'Em Planejamento'),
        ('aguardando_coleta', 'Aguardando Coleta'),
        ('em_coleta', 'Em Coleta'),
        ('coletado', 'Coletado'),
        ('em_transito', 'Em Trânsito'),
        ('em_transferencia', 'Em Transferência'),
        ('saiu_entrega', 'Saiu para Entrega'),
        ('entregue', 'Entregue'),
        ('tentativa_entrega', 'Tentativa de Entrega'),
        ('devolvido', 'Devolvido'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField('Status', max_length=30, choices=STATUS_CHOICES, default='em_planejamento')
    
    SLA_CHOICES = [
        ('verde', 'No Prazo'),
        ('amarelo', 'Atenção'),
        ('vermelho', 'Atrasado'),
    ]
    sla_status = models.CharField('SLA', max_length=10, choices=SLA_CHOICES, default='verde')
    
    # CT-e
    cte_numero = models.CharField('Número CT-e', max_length=20, blank=True)
    cte_chave = models.CharField('Chave CT-e', max_length=44, blank=True)
    cte_status = models.CharField('Status CT-e', max_length=20, blank=True)
    
    observacoes = models.TextField('Observações', blank=True)
    
    # Responsável
    responsavel = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pedidos',
        verbose_name='Responsável'
    )
    
    class Meta:
        verbose_name = 'Pedido de Frete'
        verbose_name_plural = 'Pedidos de Frete'
        unique_together = ['tenant', 'numero']
        ordering = ['-data_pedido', '-created_at']
    
    def __str__(self):
        return f"Pedido {self.numero} - {self.cliente}"
    
    @property
    def valor_total(self):
        return self.valor_frete + self.valor_seguro + self.valor_adicional
    
    @property
    def lucro_estimado(self):
        if self.custo_estimado:
            return self.valor_total - self.custo_estimado
        return None
    
    @property
    def rota(self):
        return f"{self.origem_cidade}/{self.origem_uf} → {self.destino_cidade}/{self.destino_uf}"
    
    def atualizar_sla(self):
        """Atualiza o status do SLA baseado na previsão de entrega e configurações"""
        if self.status == 'entregue':
            return
        
        from apps.core.sla_views import calcular_sla_pedido
        
        novo_sla = calcular_sla_pedido(self)
        if novo_sla != self.sla_status:
            self.sla_status = novo_sla
            self.save(update_fields=['sla_status'])


class Entrega(TenantModel):
    """Registro de entrega e rastreamento"""
    
    pedido = models.ForeignKey(
        PedidoFrete,
        on_delete=models.CASCADE,
        related_name='entregas',
        verbose_name='Pedido'
    )
    
    # Status
    STATUS_CHOICES = [
        ('aguardando', 'Aguardando'),
        ('em_rota', 'Em Rota'),
        ('chegou_destino', 'Chegou ao Destino'),
        ('entregue', 'Entregue'),
        ('entregue_parcial', 'Entregue Parcialmente'),
        ('ausente', 'Destinatário Ausente'),
        ('recusado', 'Recusado'),
        ('endereco_incorreto', 'Endereço Incorreto'),
        ('avariado', 'Avariado'),
        ('devolvido', 'Devolvido'),
    ]
    status = models.CharField('Status', max_length=30, choices=STATUS_CHOICES, default='aguardando')
    
    # Localização
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, blank=True, null=True)
    local_descricao = models.CharField('Local', max_length=255, blank=True)
    
    # Comprovante
    recebedor_nome = models.CharField('Nome do Recebedor', max_length=200, blank=True)
    recebedor_documento = models.CharField('Documento do Recebedor', max_length=20, blank=True)
    foto_comprovante = models.ImageField('Foto Comprovante', upload_to='comprovantes/', blank=True, null=True)
    assinatura = models.ImageField('Assinatura', upload_to='assinaturas/', blank=True, null=True)
    
    data_evento = models.DateTimeField('Data do Evento', default=timezone.now)
    observacao = models.TextField('Observação', blank=True)
    
    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-data_evento']
    
    def __str__(self):
        return f"{self.pedido.numero} - {self.get_status_display()}"


class EventoRastreamento(TenantModel):
    """Eventos de rastreamento do pedido"""
    
    pedido = models.ForeignKey(
        PedidoFrete,
        on_delete=models.CASCADE,
        related_name='eventos',
        verbose_name='Pedido'
    )
    
    tipo = models.CharField('Tipo do Evento', max_length=50)
    descricao = models.CharField('Descrição', max_length=255)
    local = models.CharField('Local', max_length=255, blank=True)
    
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, blank=True, null=True)
    
    data_evento = models.DateTimeField('Data do Evento', default=timezone.now)
    
    # Quem registrou
    usuario = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Usuário'
    )
    
    class Meta:
        verbose_name = 'Evento de Rastreamento'
        verbose_name_plural = 'Eventos de Rastreamento'
        ordering = ['-data_evento']
    
    def __str__(self):
        return f"{self.pedido.numero} - {self.tipo} - {self.data_evento}"
