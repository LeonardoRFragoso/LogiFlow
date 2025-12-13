from django.db import models
from apps.core.models import TenantModel
from apps.operacional.models import PedidoFrete


class CTe(TenantModel):
    """Conhecimento de Transporte Eletrônico"""
    
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('processando', 'Processando'),
        ('autorizado', 'Autorizado'),
        ('cancelado', 'Cancelado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    pedido = models.ForeignKey(PedidoFrete, on_delete=models.PROTECT, related_name='ctes')
    numero = models.CharField(max_length=20, blank=True)
    serie = models.CharField(max_length=5, default='1')
    chave = models.CharField(max_length=44, blank=True)
    protocolo = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    
    # Valores
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    valor_servico = models.DecimalField(max_digits=12, decimal_places=2)
    valor_carga = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Impostos
    icms_base = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    icms_aliquota = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    icms_valor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Focus NFe
    focusnfe_id = models.CharField(max_length=100, blank=True)
    focusnfe_ref = models.CharField(max_length=100, blank=True)
    
    # XML e PDF
    xml_autorizacao = models.TextField(blank=True)
    pdf_url = models.URLField(blank=True)
    
    # Datas
    data_emissao = models.DateTimeField(null=True, blank=True)
    data_autorizacao = models.DateTimeField(null=True, blank=True)
    
    # Erros
    mensagem_erro = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'CT-e'
        verbose_name_plural = 'CT-es'
        ordering = ['-created_at']

    def __str__(self):
        return f"CT-e {self.numero or 'Rascunho'} - {self.pedido.numero}"


class MDFe(TenantModel):
    """Manifesto de Documentos Fiscais Eletrônico"""
    
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('processando', 'Processando'),
        ('autorizado', 'Autorizado'),
        ('encerrado', 'Encerrado'),
        ('cancelado', 'Cancelado'),
    ]
    
    numero = models.CharField(max_length=20, blank=True)
    serie = models.CharField(max_length=5, default='1')
    chave = models.CharField(max_length=44, blank=True)
    protocolo = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    
    # Veículo e motorista
    veiculo = models.ForeignKey('frota.Veiculo', on_delete=models.PROTECT)
    motorista = models.ForeignKey('frota.Motorista', on_delete=models.PROTECT)
    
    # Rota
    uf_inicio = models.CharField(max_length=2)
    uf_fim = models.CharField(max_length=2)
    
    # CT-es vinculados
    ctes = models.ManyToManyField(CTe, related_name='mdfes')
    
    # Focus NFe
    focusnfe_id = models.CharField(max_length=100, blank=True)
    focusnfe_ref = models.CharField(max_length=100, blank=True)
    
    # XML e PDF
    xml_autorizacao = models.TextField(blank=True)
    pdf_url = models.URLField(blank=True)
    
    # Datas
    data_emissao = models.DateTimeField(null=True, blank=True)
    data_autorizacao = models.DateTimeField(null=True, blank=True)
    data_encerramento = models.DateTimeField(null=True, blank=True)
    
    mensagem_erro = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'MDF-e'
        verbose_name_plural = 'MDF-es'
        ordering = ['-created_at']

    def __str__(self):
        return f"MDF-e {self.numero or 'Rascunho'}"
