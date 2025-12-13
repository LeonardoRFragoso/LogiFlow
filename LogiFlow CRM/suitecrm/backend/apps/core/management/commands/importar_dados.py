"""
LogiFlow CRM - Comando de Importação de Dados
Importa dados de planilhas Excel para o sistema
"""

import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
import pandas as pd
from decimal import Decimal, InvalidOperation

from apps.core.models import Tenant
from apps.clientes.models import Cliente
from apps.frota.models import Motorista, Veiculo


class Command(BaseCommand):
    help = 'Importa dados de planilhas Excel para o LogiFlow CRM'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', type=str, help='Caminho do arquivo Excel')
        parser.add_argument('tipo', type=str, choices=['clientes', 'motoristas', 'veiculos'],
                          help='Tipo de dados a importar')
        parser.add_argument('--tenant', type=str, required=True, help='Slug do tenant')
        parser.add_argument('--dry-run', action='store_true', help='Simula importação sem salvar')

    def handle(self, *args, **options):
        arquivo = options['arquivo']
        tipo = options['tipo']
        tenant_slug = options['tenant']
        dry_run = options['dry_run']

        # Validar arquivo
        if not os.path.exists(arquivo):
            raise CommandError(f'Arquivo não encontrado: {arquivo}')

        # Obter tenant
        try:
            tenant = Tenant.objects.get(slug=tenant_slug)
        except Tenant.DoesNotExist:
            raise CommandError(f'Tenant não encontrado: {tenant_slug}')

        self.stdout.write(f'Importando {tipo} para tenant: {tenant.name}')
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: Nenhum dado será salvo'))

        # Ler Excel
        try:
            df = pd.read_excel(arquivo, dtype=str)
            df = df.fillna('')
        except Exception as e:
            raise CommandError(f'Erro ao ler arquivo: {e}')

        self.stdout.write(f'Registros encontrados: {len(df)}')

        # Importar conforme tipo
        if tipo == 'clientes':
            self._importar_clientes(df, tenant, dry_run)
        elif tipo == 'motoristas':
            self._importar_motoristas(df, tenant, dry_run)
        elif tipo == 'veiculos':
            self._importar_veiculos(df, tenant, dry_run)

    def _importar_clientes(self, df, tenant, dry_run):
        """Importa clientes do DataFrame"""
        colunas_obrigatorias = ['razao_social', 'cnpj']
        self._validar_colunas(df, colunas_obrigatorias)

        sucesso = 0
        erros = []

        for idx, row in df.iterrows():
            try:
                dados = {
                    'tenant': tenant,
                    'razao_social': row.get('razao_social', '').strip(),
                    'nome_fantasia': row.get('nome_fantasia', '').strip(),
                    'cnpj': self._limpar_documento(row.get('cnpj', '')),
                    'inscricao_estadual': row.get('inscricao_estadual', '').strip(),
                    'contato_nome': row.get('contato_nome', '').strip(),
                    'email': row.get('email', '').strip().lower(),
                    'telefone': row.get('telefone', '').strip(),
                    'celular': row.get('celular', '').strip(),
                    'cep': row.get('cep', '').strip(),
                    'logradouro': row.get('logradouro', row.get('endereco', '')).strip(),
                    'numero': row.get('numero', '').strip(),
                    'complemento': row.get('complemento', '').strip(),
                    'bairro': row.get('bairro', '').strip(),
                    'cidade': row.get('cidade', '').strip(),
                    'uf': row.get('uf', row.get('estado', '')).strip().upper()[:2],
                    'condicao_pagamento': self._mapear_condicao_pagamento(row.get('condicao_pagamento', '')),
                    'observacoes': row.get('observacoes', '').strip(),
                }

                if not dados['razao_social'] or not dados['cnpj']:
                    erros.append(f'Linha {idx+2}: Razão social e CNPJ são obrigatórios')
                    continue

                if not dry_run:
                    Cliente.objects.update_or_create(
                        tenant=tenant,
                        cnpj=dados['cnpj'],
                        defaults=dados
                    )
                sucesso += 1

            except Exception as e:
                erros.append(f'Linha {idx+2}: {str(e)}')

        self._exibir_resultado('Clientes', sucesso, erros)

    def _importar_motoristas(self, df, tenant, dry_run):
        """Importa motoristas do DataFrame"""
        colunas_obrigatorias = ['nome', 'cpf', 'cnh_numero', 'cnh_categoria', 'cnh_validade']
        self._validar_colunas(df, colunas_obrigatorias)

        sucesso = 0
        erros = []

        for idx, row in df.iterrows():
            try:
                dados = {
                    'tenant': tenant,
                    'nome': row.get('nome', '').strip(),
                    'cpf': self._limpar_documento(row.get('cpf', '')),
                    'rg': row.get('rg', '').strip(),
                    'cnh_numero': row.get('cnh_numero', '').strip(),
                    'cnh_categoria': row.get('cnh_categoria', '').strip().upper(),
                    'cnh_validade': self._parse_data(row.get('cnh_validade', '')),
                    'telefone': row.get('telefone', '').strip(),
                    'celular': row.get('celular', '').strip(),
                    'email': row.get('email', '').strip().lower(),
                    'cep': row.get('cep', '').strip(),
                    'endereco': row.get('endereco', '').strip(),
                    'cidade': row.get('cidade', '').strip(),
                    'uf': row.get('uf', '').strip().upper()[:2],
                    'status': self._mapear_status_motorista(row.get('status', 'ativo')),
                    'observacoes': row.get('observacoes', '').strip(),
                }

                if not dados['nome'] or not dados['cpf']:
                    erros.append(f'Linha {idx+2}: Nome e CPF são obrigatórios')
                    continue

                if not dados['cnh_validade']:
                    erros.append(f'Linha {idx+2}: Data de validade da CNH inválida')
                    continue

                if not dry_run:
                    Motorista.objects.update_or_create(
                        tenant=tenant,
                        cpf=dados['cpf'],
                        defaults=dados
                    )
                sucesso += 1

            except Exception as e:
                erros.append(f'Linha {idx+2}: {str(e)}')

        self._exibir_resultado('Motoristas', sucesso, erros)

    def _importar_veiculos(self, df, tenant, dry_run):
        """Importa veículos do DataFrame"""
        colunas_obrigatorias = ['placa', 'tipo']
        self._validar_colunas(df, colunas_obrigatorias)

        sucesso = 0
        erros = []

        for idx, row in df.iterrows():
            try:
                dados = {
                    'tenant': tenant,
                    'placa': row.get('placa', '').strip().upper().replace('-', ''),
                    'renavam': row.get('renavam', '').strip(),
                    'chassi': row.get('chassi', '').strip(),
                    'tipo': self._mapear_tipo_veiculo(row.get('tipo', '')),
                    'marca': row.get('marca', '').strip(),
                    'modelo': row.get('modelo', '').strip(),
                    'ano_fabricacao': self._parse_int(row.get('ano_fabricacao', '')),
                    'ano_modelo': self._parse_int(row.get('ano_modelo', '')),
                    'cor': row.get('cor', '').strip(),
                    'capacidade_kg': self._parse_decimal(row.get('capacidade_kg', '')),
                    'capacidade_m3': self._parse_decimal(row.get('capacidade_m3', '')),
                    'propriedade': self._mapear_propriedade(row.get('propriedade', 'proprio')),
                    'proprietario_nome': row.get('proprietario_nome', '').strip(),
                    'km_atual': self._parse_int(row.get('km_atual', '0')) or 0,
                    'status': 'disponivel',
                    'observacoes': row.get('observacoes', '').strip(),
                }

                if not dados['placa'] or not dados['tipo']:
                    erros.append(f'Linha {idx+2}: Placa e tipo são obrigatórios')
                    continue

                if not dry_run:
                    Veiculo.objects.update_or_create(
                        tenant=tenant,
                        placa=dados['placa'],
                        defaults=dados
                    )
                sucesso += 1

            except Exception as e:
                erros.append(f'Linha {idx+2}: {str(e)}')

        self._exibir_resultado('Veículos', sucesso, erros)

    # Helpers
    def _validar_colunas(self, df, obrigatorias):
        faltando = [c for c in obrigatorias if c not in df.columns]
        if faltando:
            raise CommandError(f'Colunas obrigatórias faltando: {", ".join(faltando)}')

    def _limpar_documento(self, doc):
        return ''.join(c for c in str(doc) if c.isdigit())

    def _parse_data(self, valor):
        if not valor:
            return None
        try:
            return pd.to_datetime(valor).date()
        except:
            return None

    def _parse_decimal(self, valor):
        if not valor:
            return None
        try:
            return Decimal(str(valor).replace(',', '.'))
        except InvalidOperation:
            return None

    def _parse_int(self, valor):
        if not valor:
            return None
        try:
            return int(float(str(valor)))
        except:
            return None

    def _mapear_condicao_pagamento(self, valor):
        mapa = {
            'a vista': 'a_vista', 'à vista': 'a_vista', 'avista': 'a_vista',
            '7': '7_dias', '7 dias': '7_dias',
            '14': '14_dias', '14 dias': '14_dias',
            '21': '21_dias', '21 dias': '21_dias',
            '28': '28_dias', '28 dias': '28_dias',
            '30': '30_dias', '30 dias': '30_dias',
            '45': '45_dias', '45 dias': '45_dias',
            '60': '60_dias', '60 dias': '60_dias',
            'faturado': 'faturado',
        }
        return mapa.get(str(valor).lower().strip(), '30_dias')

    def _mapear_status_motorista(self, valor):
        mapa = {
            'ativo': 'ativo', 'ativa': 'ativo',
            'inativo': 'inativo', 'inativa': 'inativo',
            'ferias': 'ferias', 'férias': 'ferias',
            'afastado': 'afastado',
            'desligado': 'desligado',
        }
        return mapa.get(str(valor).lower().strip(), 'ativo')

    def _mapear_tipo_veiculo(self, valor):
        mapa = {
            'moto': 'moto', 'motocicleta': 'moto',
            'fiorino': 'fiorino', 'kangoo': 'fiorino',
            'van': 'van',
            'vuc': 'vuc', '3/4': 'vuc',
            'toco': 'toco',
            'truck': 'truck',
            'carreta': 'carreta',
            'bitrem': 'bitrem',
            'rodotrem': 'rodotrem',
        }
        return mapa.get(str(valor).lower().strip(), 'toco')

    def _mapear_propriedade(self, valor):
        mapa = {
            'proprio': 'proprio', 'próprio': 'proprio',
            'terceiro': 'terceiro',
            'agregado': 'agregado',
            'alugado': 'alugado',
        }
        return mapa.get(str(valor).lower().strip(), 'proprio')

    def _exibir_resultado(self, tipo, sucesso, erros):
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'{tipo} importados com sucesso: {sucesso}'))
        if erros:
            self.stdout.write(self.style.ERROR(f'Erros encontrados: {len(erros)}'))
            for erro in erros[:10]:
                self.stdout.write(self.style.WARNING(f'  - {erro}'))
            if len(erros) > 10:
                self.stdout.write(self.style.WARNING(f'  ... e mais {len(erros)-10} erros'))
