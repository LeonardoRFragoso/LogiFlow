#!/usr/bin/env python3
"""
LogiFlow CRM - Script de Importação de Dados
Importa dados de arquivos CSV para o SuiteCRM
"""

import csv
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/importacao_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ImportadorDados:
    """Importador de dados CSV para LogiFlow CRM"""
    
    def __init__(self, modo_atualizacao: bool = False):
        self.modo_atualizacao = modo_atualizacao
        self.estatisticas = {
            'total': 0,
            'sucesso': 0,
            'erro': 0,
            'duplicado': 0,
            'atualizado': 0
        }
    
    def validar_cpf(self, cpf: str) -> bool:
        """Valida CPF"""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11:
            return False
        # Validação básica (pode ser melhorada)
        return True
    
    def validar_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ"""
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14:
            return False
        return True
    
    def validar_data(self, data: str) -> Optional[str]:
        """Valida e converte data DD/MM/AAAA para AAAA-MM-DD"""
        if not data:
            return None
        try:
            dt = datetime.strptime(data, '%d/%m/%Y')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            return None
    
    def limpar_numero(self, valor: str) -> Optional[float]:
        """Limpa e converte valor numérico"""
        if not valor:
            return None
        try:
            valor = re.sub(r'[^\d,.-]', '', valor)
            valor = valor.replace(',', '.')
            return float(valor)
        except ValueError:
            return None
    
    def importar_clientes(self, arquivo: str) -> None:
        """Importa clientes de arquivo CSV"""
        logger.info(f"Importando clientes de {arquivo}")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for linha_num, row in enumerate(reader, start=2):
                    self.estatisticas['total'] += 1
                    
                    try:
                        # Validar campos obrigatórios
                        if not row.get('nome'):
                            raise ValueError("Campo 'nome' é obrigatório")
                        
                        if not row.get('cnpj'):
                            raise ValueError("Campo 'cnpj' é obrigatório")
                        
                        if not self.validar_cnpj(row['cnpj']):
                            raise ValueError(f"CNPJ inválido: {row['cnpj']}")
                        
                        # Preparar dados
                        cliente = {
                            'name': row['nome'],
                            'cnpj': re.sub(r'\D', '', row['cnpj']),
                            'email1': row.get('email', ''),
                            'phone_office': row.get('telefone', ''),
                            'billing_address_street': row.get('endereco', ''),
                            'billing_address_city': row.get('cidade', ''),
                            'billing_address_state': row.get('uf', ''),
                            'billing_address_postalcode': row.get('cep', ''),
                            'description': row.get('observacoes', '')
                        }
                        
                        # TODO: Enviar para SuiteCRM API
                        # suitecrm_client.create_account(cliente)
                        
                        logger.info(f"Linha {linha_num}: Cliente '{row['nome']}' importado com sucesso")
                        self.estatisticas['sucesso'] += 1
                        
                    except Exception as e:
                        logger.error(f"Linha {linha_num}: Erro ao importar cliente - {e}")
                        self.estatisticas['erro'] += 1
                        
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {arquivo}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {e}")
            sys.exit(1)
    
    def importar_motoristas(self, arquivo: str) -> None:
        """Importa motoristas de arquivo CSV"""
        logger.info(f"Importando motoristas de {arquivo}")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for linha_num, row in enumerate(reader, start=2):
                    self.estatisticas['total'] += 1
                    
                    try:
                        # Validar campos obrigatórios
                        if not row.get('nome'):
                            raise ValueError("Campo 'nome' é obrigatório")
                        
                        if not row.get('cpf'):
                            raise ValueError("Campo 'cpf' é obrigatório")
                        
                        if not self.validar_cpf(row['cpf']):
                            raise ValueError(f"CPF inválido: {row['cpf']}")
                        
                        if not row.get('cnh'):
                            raise ValueError("Campo 'cnh' é obrigatório")
                        
                        if not row.get('categoria_cnh'):
                            raise ValueError("Campo 'categoria_cnh' é obrigatório")
                        
                        # Validar data de vencimento
                        vencimento_cnh = self.validar_data(row.get('vencimento_cnh', ''))
                        
                        # Preparar dados
                        motorista = {
                            'name': row['nome'],
                            'cpf': re.sub(r'\D', '', row['cpf']),
                            'cnh': row['cnh'],
                            'categoria_cnh': row['categoria_cnh'],
                            'vencimento_cnh': vencimento_cnh,
                            'celular': row.get('celular', ''),
                            'email': row.get('email', ''),
                            'status': row.get('status', 'ativo'),
                            'observacoes': row.get('observacoes', '')
                        }
                        
                        # TODO: Enviar para SuiteCRM API
                        # suitecrm_client.create_motorista(motorista)
                        
                        logger.info(f"Linha {linha_num}: Motorista '{row['nome']}' importado com sucesso")
                        self.estatisticas['sucesso'] += 1
                        
                    except Exception as e:
                        logger.error(f"Linha {linha_num}: Erro ao importar motorista - {e}")
                        self.estatisticas['erro'] += 1
                        
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {arquivo}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {e}")
            sys.exit(1)
    
    def importar_veiculos(self, arquivo: str) -> None:
        """Importa veículos de arquivo CSV"""
        logger.info(f"Importando veículos de {arquivo}")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for linha_num, row in enumerate(reader, start=2):
                    self.estatisticas['total'] += 1
                    
                    try:
                        # Validar campos obrigatórios
                        if not row.get('placa'):
                            raise ValueError("Campo 'placa' é obrigatório")
                        
                        if not row.get('tipo_veiculo'):
                            raise ValueError("Campo 'tipo_veiculo' é obrigatório")
                        
                        # Validar data CRLV
                        crlv_validade = self.validar_data(row.get('crlv_validade', ''))
                        
                        # Preparar dados
                        veiculo = {
                            'name': f"{row['placa']} - {row.get('modelo', 'Veículo')}",
                            'placa': row['placa'].upper(),
                            'tipo_veiculo': row['tipo_veiculo'],
                            'renavam': row.get('renavam', ''),
                            'marca': row.get('marca', ''),
                            'modelo': row.get('modelo', ''),
                            'ano_fabricacao': row.get('ano_fabricacao', ''),
                            'ano_modelo': row.get('ano_modelo', ''),
                            'capacidade_kg': self.limpar_numero(row.get('capacidade_kg', '')),
                            'capacidade_m3': self.limpar_numero(row.get('capacidade_m3', '')),
                            'crlv_validade': crlv_validade,
                            'status': row.get('status', 'disponivel'),
                            'observacoes': row.get('observacoes', '')
                        }
                        
                        # TODO: Enviar para SuiteCRM API
                        # suitecrm_client.create_veiculo(veiculo)
                        
                        logger.info(f"Linha {linha_num}: Veículo '{row['placa']}' importado com sucesso")
                        self.estatisticas['sucesso'] += 1
                        
                    except Exception as e:
                        logger.error(f"Linha {linha_num}: Erro ao importar veículo - {e}")
                        self.estatisticas['erro'] += 1
                        
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {arquivo}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {e}")
            sys.exit(1)
    
    def importar_cotacoes(self, arquivo: str) -> None:
        """Importa cotações de arquivo CSV"""
        logger.info(f"Importando cotações de {arquivo}")
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for linha_num, row in enumerate(reader, start=2):
                    self.estatisticas['total'] += 1
                    
                    try:
                        # Validar campos obrigatórios
                        if not row.get('cliente_cnpj'):
                            raise ValueError("Campo 'cliente_cnpj' é obrigatório")
                        
                        if not self.validar_cnpj(row['cliente_cnpj']):
                            raise ValueError(f"CNPJ inválido: {row['cliente_cnpj']}")
                        
                        # Validar datas
                        data_cotacao = self.validar_data(row.get('data_cotacao', ''))
                        validade = self.validar_data(row.get('validade', ''))
                        
                        # Preparar dados
                        cotacao = {
                            'name': f"Cotação {row['origem_cidade']}-{row['destino_cidade']}",
                            'cliente_cnpj': re.sub(r'\D', '', row['cliente_cnpj']),
                            'data_cotacao': data_cotacao or datetime.now().strftime('%Y-%m-%d'),
                            'origem_cidade': row.get('origem_cidade', ''),
                            'origem_uf': row.get('origem_uf', ''),
                            'destino_cidade': row.get('destino_cidade', ''),
                            'destino_uf': row.get('destino_uf', ''),
                            'tipo_carga': row.get('tipo_carga', 'geral'),
                            'peso_kg': self.limpar_numero(row.get('peso_kg', '')),
                            'valor_proposta': self.limpar_numero(row.get('valor_proposta', '')),
                            'status': row.get('status', 'aberta'),
                            'validade': validade,
                            'observacoes': row.get('observacoes', '')
                        }
                        
                        # TODO: Buscar cliente por CNPJ e associar
                        # cliente = suitecrm_client.find_account_by_cnpj(cotacao['cliente_cnpj'])
                        # cotacao['cliente_id'] = cliente['id']
                        
                        # TODO: Enviar para SuiteCRM API
                        # suitecrm_client.create_cotacao(cotacao)
                        
                        logger.info(f"Linha {linha_num}: Cotação importada com sucesso")
                        self.estatisticas['sucesso'] += 1
                        
                    except Exception as e:
                        logger.error(f"Linha {linha_num}: Erro ao importar cotação - {e}")
                        self.estatisticas['erro'] += 1
                        
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {arquivo}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {e}")
            sys.exit(1)
    
    def exibir_estatisticas(self) -> None:
        """Exibe estatísticas da importação"""
        logger.info("\n" + "="*60)
        logger.info("ESTATÍSTICAS DA IMPORTAÇÃO")
        logger.info("="*60)
        logger.info(f"Total de registros: {self.estatisticas['total']}")
        logger.info(f"Importados com sucesso: {self.estatisticas['sucesso']}")
        logger.info(f"Erros: {self.estatisticas['erro']}")
        logger.info(f"Duplicados: {self.estatisticas['duplicado']}")
        logger.info(f"Atualizados: {self.estatisticas['atualizado']}")
        logger.info("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Importa dados de CSV para LogiFlow CRM'
    )
    parser.add_argument(
        '--tipo',
        required=True,
        choices=['clientes', 'motoristas', 'veiculos', 'cotacoes'],
        help='Tipo de dados a importar'
    )
    parser.add_argument(
        '--arquivo',
        required=True,
        help='Caminho do arquivo CSV'
    )
    parser.add_argument(
        '--atualizar',
        action='store_true',
        help='Atualiza registros existentes (use com cuidado!)'
    )
    
    args = parser.parse_args()
    
    # Verificar se arquivo existe
    if not Path(args.arquivo).exists():
        logger.error(f"Arquivo não encontrado: {args.arquivo}")
        sys.exit(1)
    
    # Criar importador
    importador = ImportadorDados(modo_atualizacao=args.atualizar)
    
    # Executar importação
    logger.info(f"Iniciando importação de {args.tipo}")
    logger.info(f"Arquivo: {args.arquivo}")
    logger.info(f"Modo atualização: {'SIM' if args.atualizar else 'NÃO'}")
    logger.info("-" * 60)
    
    try:
        if args.tipo == 'clientes':
            importador.importar_clientes(args.arquivo)
        elif args.tipo == 'motoristas':
            importador.importar_motoristas(args.arquivo)
        elif args.tipo == 'veiculos':
            importador.importar_veiculos(args.arquivo)
        elif args.tipo == 'cotacoes':
            importador.importar_cotacoes(args.arquivo)
        
        # Exibir estatísticas
        importador.exibir_estatisticas()
        
        # Código de saída
        if importador.estatisticas['erro'] > 0:
            logger.warning("Importação concluída com erros!")
            sys.exit(1)
        else:
            logger.info("Importação concluída com sucesso!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.warning("\nImportação cancelada pelo usuário")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
