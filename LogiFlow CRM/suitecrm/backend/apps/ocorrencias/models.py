"""
LogiFlow CRM - Ocorrências Models
Registro de ocorrências e problemas nas entregas
"""

from django.db import models
from django.utils import timezone
from apps.core.models import TenantModel


class Ocorrencia(TenantModel):
    """Registro de ocorrências durante o transporte"""
    
    # Vínculo com pedido
    pedido = models.ForeignKey(
        'operacional.PedidoFrete',
        on_delete=models.CASCADE,
        related_name='ocorrencias',
        verbose_name='Pedido'
    )
    
    # Tipo e descrição
    TIPO_CHOICES = [
        ('atraso', 'Atraso'),
        ('avaria', 'Avaria'),
        ('extravio', 'Extravio'),
        ('roubo', 'Roubo/Furto'),
        ('acidente', 'Acidente'),
        ('devolucao', 'Devolução'),
        ('recusa', 'Recusa'),
        ('reentrega', 'Reentrega'),
        ('fiscalizacao', 'Fiscalização'),
        ('outro', 'Outro'),
    ]
    tipo = models.CharField('Tipo', max_length=30, choices=TIPO_CHOICES)
    
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição')
    
    # Data e local
    data_ocorrencia = models.DateTimeField('Data da Ocorrência', default=timezone.now)
    local = models.CharField('Local da Ocorrência', max_length=255, blank=True)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, blank=True, null=True)
    
    # Status
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_analise', 'Em Análise'),
        ('resolvida', 'Resolvida'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='aberta')
    
    # Prioridade
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    prioridade = models.CharField('Prioridade', max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    
    # Valores (se aplicável)
    valor_prejuizo = models.DecimalField(
        'Valor do Prejuízo', 
        max_digits=12, 
        decimal_places=2, 
        blank=True, null=True
    )
    valor_ressarcimento = models.DecimalField(
        'Valor Ressarcido', 
        max_digits=12, 
        decimal_places=2, 
        blank=True, null=True
    )
    
    # Responsáveis
    registrado_por = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='ocorrencias_registradas',
        verbose_name='Registrado Por'
    )
    responsavel = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ocorrencias_responsavel',
        verbose_name='Responsável pela Resolução'
    )
    
    # Resolução
    data_resolucao = models.DateTimeField('Data da Resolução', blank=True, null=True)
    resolucao = models.TextField('Resolução', blank=True)
    
    # Boletim de Ocorrência (se aplicável)
    numero_bo = models.CharField('Número do B.O.', max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'
        ordering = ['-data_ocorrencia']
    
    def __str__(self):
        return f"{self.pedido.numero} - {self.get_tipo_display()} - {self.titulo}"
    
    def resolver(self, resolucao, usuario=None):
        """Marca a ocorrência como resolvida"""
        self.status = 'resolvida'
        self.resolucao = resolucao
        self.data_resolucao = timezone.now()
        if usuario:
            self.responsavel = usuario
        self.save()


class AnexoOcorrencia(TenantModel):
    """Anexos de uma ocorrência (fotos, documentos)"""
    
    ocorrencia = models.ForeignKey(
        Ocorrencia,
        on_delete=models.CASCADE,
        related_name='anexos',
        verbose_name='Ocorrência'
    )
    
    TIPO_CHOICES = [
        ('foto', 'Foto'),
        ('documento', 'Documento'),
        ('video', 'Vídeo'),
        ('outro', 'Outro'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='foto')
    
    titulo = models.CharField('Título', max_length=200, blank=True)
    arquivo = models.FileField('Arquivo', upload_to='ocorrencias/anexos/')
    
    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
    
    def __str__(self):
        return f"{self.ocorrencia} - {self.titulo or self.arquivo.name}"


class ComentarioOcorrencia(TenantModel):
    """Comentários/histórico de uma ocorrência"""
    
    ocorrencia = models.ForeignKey(
        Ocorrencia,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name='Ocorrência'
    )
    
    autor = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Autor'
    )
    
    texto = models.TextField('Comentário')
    
    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.ocorrencia} - {self.autor} - {self.created_at}"
