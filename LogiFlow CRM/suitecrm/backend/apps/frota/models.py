"""
LogiFlow CRM - Frota Models
Motoristas, veículos e manutenções
"""

from django.db import models
from django.utils import timezone
from apps.core.models import TenantModel
from datetime import timedelta


class Motorista(TenantModel):
    """Cadastro de motoristas"""
    
    # Dados pessoais
    nome = models.CharField('Nome Completo', max_length=200)
    cpf = models.CharField('CPF', max_length=14, db_index=True)
    rg = models.CharField('RG', max_length=20, blank=True)
    data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    
    # CNH
    cnh_numero = models.CharField('Número CNH', max_length=20)
    CNH_CATEGORIA_CHOICES = [
        ('A', 'A - Motocicleta'),
        ('B', 'B - Carro'),
        ('C', 'C - Caminhão'),
        ('D', 'D - Ônibus'),
        ('E', 'E - Carreta'),
        ('AB', 'AB'),
        ('AC', 'AC'),
        ('AD', 'AD'),
        ('AE', 'AE'),
    ]
    cnh_categoria = models.CharField('Categoria CNH', max_length=3, choices=CNH_CATEGORIA_CHOICES)
    cnh_validade = models.DateField('Validade CNH')
    cnh_primeira_habilitacao = models.DateField('Primeira Habilitação', blank=True, null=True)
    
    # Contato
    telefone = models.CharField('Telefone', max_length=20, blank=True)
    celular = models.CharField('Celular', max_length=20)
    email = models.EmailField('E-mail', blank=True)
    
    # Endereço
    cep = models.CharField('CEP', max_length=10, blank=True)
    endereco = models.CharField('Endereço', max_length=255, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    uf = models.CharField('UF', max_length=2, blank=True)
    
    # Status
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('ferias', 'Férias'),
        ('afastado', 'Afastado'),
        ('desligado', 'Desligado'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='ativo')
    data_admissao = models.DateField('Data de Admissão', blank=True, null=True)
    data_demissao = models.DateField('Data de Demissão', blank=True, null=True)
    
    # Vínculo com usuário do sistema (para app do motorista)
    usuario = models.OneToOneField(
        'core.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='motorista_perfil',
        verbose_name='Usuário do Sistema'
    )
    
    # Documentos
    foto = models.ImageField('Foto', upload_to='motoristas/fotos/', blank=True, null=True)
    cnh_arquivo = models.FileField('Arquivo CNH', upload_to='motoristas/cnh/', blank=True, null=True)
    
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'
        unique_together = ['tenant', 'cpf']
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def cnh_vencendo(self):
        """Retorna True se CNH vence em menos de 30 dias"""
        return self.cnh_validade <= timezone.now().date() + timedelta(days=30)
    
    @property
    def cnh_vencida(self):
        """Retorna True se CNH está vencida"""
        return self.cnh_validade < timezone.now().date()
    
    @property
    def dias_para_vencer_cnh(self):
        """Retorna quantidade de dias para vencer a CNH"""
        return (self.cnh_validade - timezone.now().date()).days


class Veiculo(TenantModel):
    """Cadastro de veículos da frota"""
    
    # Identificação
    placa = models.CharField('Placa', max_length=10, db_index=True)
    renavam = models.CharField('RENAVAM', max_length=20, blank=True)
    chassi = models.CharField('Chassi', max_length=20, blank=True)
    
    # Características
    TIPO_CHOICES = [
        ('moto', 'Motocicleta'),
        ('fiorino', 'Fiorino/Kangoo'),
        ('van', 'Van'),
        ('vuc', 'VUC'),
        ('toco', 'Caminhão Toco'),
        ('truck', 'Caminhão Truck'),
        ('carreta', 'Carreta'),
        ('bitrem', 'Bitrem'),
        ('rodotrem', 'Rodotrem'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    marca = models.CharField('Marca', max_length=50, blank=True)
    modelo = models.CharField('Modelo', max_length=100, blank=True)
    ano_fabricacao = models.PositiveIntegerField('Ano Fabricação', blank=True, null=True)
    ano_modelo = models.PositiveIntegerField('Ano Modelo', blank=True, null=True)
    cor = models.CharField('Cor', max_length=30, blank=True)
    
    # Capacidade
    capacidade_kg = models.DecimalField('Capacidade (kg)', max_digits=10, decimal_places=2, blank=True, null=True)
    capacidade_m3 = models.DecimalField('Capacidade (m³)', max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Documentação
    documento_vencimento = models.DateField('Vencimento do Documento', blank=True, null=True)
    seguro_vencimento = models.DateField('Vencimento do Seguro', blank=True, null=True)
    
    # Motorista fixo (opcional)
    motorista_fixo = models.ForeignKey(
        Motorista,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='veiculos',
        verbose_name='Motorista Fixo'
    )
    
    # Status
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('em_viagem', 'Em Viagem'),
        ('manutencao', 'Em Manutenção'),
        ('reservado', 'Reservado'),
        ('inativo', 'Inativo'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='disponivel')
    
    # Controle
    km_atual = models.PositiveIntegerField('KM Atual', default=0)
    ultima_manutencao = models.DateField('Última Manutenção', blank=True, null=True)
    proxima_manutencao_km = models.PositiveIntegerField('Próxima Manutenção (KM)', blank=True, null=True)
    
    # Propriedade
    PROPRIEDADE_CHOICES = [
        ('proprio', 'Próprio'),
        ('terceiro', 'Terceiro'),
        ('agregado', 'Agregado'),
        ('alugado', 'Alugado'),
    ]
    propriedade = models.CharField('Propriedade', max_length=20, choices=PROPRIEDADE_CHOICES, default='proprio')
    proprietario_nome = models.CharField('Nome do Proprietário', max_length=200, blank=True)
    proprietario_cpf_cnpj = models.CharField('CPF/CNPJ Proprietário', max_length=18, blank=True)
    
    # Rastreador
    rastreador_id = models.CharField('ID do Rastreador', max_length=50, blank=True)
    rastreador_modelo = models.CharField('Modelo Rastreador', max_length=50, blank=True)
    
    foto = models.ImageField('Foto', upload_to='veiculos/', blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        unique_together = ['tenant', 'placa']
        ordering = ['placa']
    
    def __str__(self):
        return f"{self.placa} - {self.get_tipo_display()}"
    
    @property
    def documento_vencendo(self):
        """Retorna True se documento vence em menos de 30 dias"""
        if self.documento_vencimento:
            return self.documento_vencimento <= timezone.now().date() + timedelta(days=30)
        return False


class Manutencao(TenantModel):
    """Registro de manutenções dos veículos"""
    
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name='manutencoes',
        verbose_name='Veículo'
    )
    
    TIPO_CHOICES = [
        ('preventiva', 'Preventiva'),
        ('corretiva', 'Corretiva'),
        ('revisao', 'Revisão'),
        ('troca_pneu', 'Troca de Pneu'),
        ('troca_oleo', 'Troca de Óleo'),
        ('documentacao', 'Documentação'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    
    descricao = models.TextField('Descrição')
    km_realizacao = models.PositiveIntegerField('KM na Realização', blank=True, null=True)
    
    data_entrada = models.DateField('Data de Entrada')
    data_saida = models.DateField('Data de Saída', blank=True, null=True)
    previsao_saida = models.DateField('Previsão de Saída', blank=True, null=True)
    
    fornecedor = models.CharField('Fornecedor/Oficina', max_length=200, blank=True)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2, blank=True, null=True)
    
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='agendada')
    
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'
        ordering = ['-data_entrada']
    
    def __str__(self):
        return f"{self.veiculo.placa} - {self.get_tipo_display()} - {self.data_entrada}"
