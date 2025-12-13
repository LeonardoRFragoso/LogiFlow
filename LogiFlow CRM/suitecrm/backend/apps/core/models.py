"""
LogiFlow CRM - Core Models
Modelos base e abstratos
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """Modelo base com campos comuns a todos os modelos"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    is_active = models.BooleanField('Ativo', default=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class Tenant(BaseModel):
    """Multi-tenant: cada cliente SaaS é um tenant"""
    
    name = models.CharField('Nome da Empresa', max_length=255)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True, blank=True, null=True)
    email = models.EmailField('E-mail')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    
    # Plano e limites
    PLAN_CHOICES = [
        ('trial', 'Trial'),
        ('start', 'Start'),
        ('pro', 'Pro'),
        ('premium', 'Premium'),
    ]
    plan = models.CharField('Plano', max_length=20, choices=PLAN_CHOICES, default='trial')
    max_users = models.PositiveIntegerField('Máx. Usuários', default=5)
    storage_limit_mb = models.PositiveIntegerField('Limite Storage (MB)', default=1024)
    
    # Datas
    trial_ends_at = models.DateTimeField('Trial expira em', blank=True, null=True)
    
    # Configurações JSON
    settings = models.JSONField('Configurações', default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    """Usuário customizado com suporte a multi-tenant"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.CASCADE, 
        related_name='users',
        verbose_name='Tenant',
        null=True, blank=True
    )
    
    phone = models.CharField('Telefone', max_length=20, blank=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True, null=True)
    
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('operator', 'Operador'),
        ('driver', 'Motorista'),
        ('viewer', 'Visualizador'),
    ]
    role = models.CharField('Função', max_length=20, choices=ROLE_CHOICES, default='operator')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.get_full_name() or self.username


class TenantModel(BaseModel):
    """Modelo base para modelos que pertencem a um tenant"""
    
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Tenant'
    )
    
    class Meta:
        abstract = True
