"""
LogiFlow CRM - Script de Importação de Dados
==============================================
Importa dados de planilhas CSV/Excel para o sistema

Uso:
    python importar_dados.py --tipo clientes --arquivo template_clientes.csv
    python importar_dados.py --tipo motoristas --arquivo template_motoristas.csv --dry-run
    python importar_dados.py --tipo veiculos --arquivo template_veiculos.csv
    python importar_dados.py --tipo cotacoes --arquivo template_cotacoes.csv
"""

import csv
import sys
import argparse
import re
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path
import json

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class DataValidator:
    """Validador de dados para importação"""
    
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Valida CPF"""
        if not cpf:
            return False
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) != 11:
            return False
        # Validação básica (não verifica dígitos verificadores)
        return cpf != cpf[0] * 11
    
    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """Valida CNPJ"""
        if not cnpj:
            return False
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        if len(cnpj) != 14:
            return False
        return cnpj != cnpj[0] * 14
    
    @staticmethod
    def validar_cep(cep: str) -> bool:
        """Valida CEP"""
        if not cep:
            return False
        cep = re.sub(r'[^0-9]', '', cep)
        return len(cep) == 8
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida email"""
        if not email:
            return True  # Email é opcional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """Valida telefone"""
        if not telefone:
            return True  # Telefone é opcional
        telefone = re.sub(r'[^0-9]', '', telefone)
        return len(telefone) >= 10 and len(telefone) <= 11
    
    @staticmethod
    def validar_placa(placa: str) -> bool:
        """Valida placa de veículo (formato antigo ou Mercosul)"""
        if not placa:
            return False
        placa = placa.upper().replace('-', '').replace(' ', '')
        # Formato antigo: ABC1234
        # Formato Mercosul: ABC1D23
        pattern = r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$'
        return re.match(pattern, placa) is not None
    
    @staticmethod
    def validar_data(data: str) -> bool:
        """Valida data no formato YYYY-MM-DD ou DD/MM/YYYY"""
        if not data:
            return True  # Data é opcional
        try:
            if '/' in data:
                datetime.strptime(data, '%d/%m/%Y')
            else:
                datetime.strptime(data, '%Y-%m-%d')
            return True
        except:
            return False


class DataImporter:
    """Importador de dados"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.validator = DataValidator()
        self.erros = []
        self.avisos = []
        self.sucessos = 0
    
    def importar_clientes(self, arquivo: str) -> Dict:
        """Importa clientes de CSV"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}=== Importando Clientes ==={Colors.RESET}\n")
        
        clientes = []
        linha_num = 1
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    linha_num += 1
                    erros_linha = []
                    
                    # Validações obrigatórias
                    if not row.get('nome'):
                        erros_linha.append("Nome é obrigatório")
                    
                    # Validar CPF ou CNPJ
                    if row.get('cnpj'):
                        if not self.validator.validar_cnpj(row['cnpj']):
                            erros_linha.append(f"CNPJ inválido: {row['cnpj']}")
                    elif row.get('cpf'):
                        if not self.validator.validar_cpf(row['cpf']):
                            erros_linha.append(f"CPF inválido: {row['cpf']}")
                    else:
                        erros_linha.append("CPF ou CNPJ é obrigatório")
                    
                    # Validar CEP
                    if row.get('cep') and not self.validator.validar_cep(row['cep']):
                        erros_linha.append(f"CEP inválido: {row['cep']}")
                    
                    # Validar email
                    if row.get('email') and not self.validator.validar_email(row['email']):
                        erros_linha.append(f"Email inválido: {row['email']}")
                    
                    # Validar telefone
                    if row.get('telefone') and not self.validator.validar_telefone(row['telefone']):
                        self.avisos.append(f"Linha {linha_num}: Telefone pode estar inválido: {row['telefone']}")
                    
                    if erros_linha:
                        self.erros.append(f"Linha {linha_num} ({row.get('nome', 'SEM NOME')}): {', '.join(erros_linha)}")
                    else:
                        clientes.append(row)
                        self.sucessos += 1
                        print(f"{Colors.GREEN}✓{Colors.RESET} Cliente: {row['nome']}")
        
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Arquivo não encontrado: {arquivo}{Colors.RESET}")
            return {"success": False, "error": "Arquivo não encontrado"}
        except Exception as e:
            print(f"{Colors.RED}✗ Erro ao ler arquivo: {e}{Colors.RESET}")
            return {"success": False, "error": str(e)}
        
        return {
            "success": len(self.erros) == 0,
            "total": len(clientes),
            "importados": clientes
        }
    
    def importar_motoristas(self, arquivo: str) -> Dict:
        """Importa motoristas de CSV"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}=== Importando Motoristas ==={Colors.RESET}\n")
        
        motoristas = []
        linha_num = 1
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    linha_num += 1
                    erros_linha = []
                    
                    # Validações obrigatórias
                    if not row.get('nome'):
                        erros_linha.append("Nome é obrigatório")
                    
                    if not row.get('cpf') or not self.validator.validar_cpf(row['cpf']):
                        erros_linha.append(f"CPF inválido: {row.get('cpf', 'VAZIO')}")
                    
                    if not row.get('cnh'):
                        erros_linha.append("CNH é obrigatória")
                    
                    if not row.get('categoria_cnh'):
                        erros_linha.append("Categoria CNH é obrigatória")
                    
                    # Validar vencimento CNH
                    if row.get('vencimento_cnh'):
                        if not self.validator.validar_data(row['vencimento_cnh']):
                            erros_linha.append(f"Data de vencimento CNH inválida: {row['vencimento_cnh']}")
                        else:
                            # Verificar se CNH está vencida
                            try:
                                vencimento = datetime.strptime(row['vencimento_cnh'], '%Y-%m-%d')
                                if vencimento < datetime.now():
                                    self.avisos.append(f"Linha {linha_num}: CNH vencida - {row['nome']}")
                            except:
                                pass
                    
                    # Validar telefone
                    if row.get('telefone') and not self.validator.validar_telefone(row['telefone']):
                        self.avisos.append(f"Linha {linha_num}: Telefone pode estar inválido")
                    
                    if erros_linha:
                        self.erros.append(f"Linha {linha_num} ({row.get('nome', 'SEM NOME')}): {', '.join(erros_linha)}")
                    else:
                        motoristas.append(row)
                        self.sucessos += 1
                        print(f"{Colors.GREEN}✓{Colors.RESET} Motorista: {row['nome']}")
        
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Arquivo não encontrado: {arquivo}{Colors.RESET}")
            return {"success": False, "error": "Arquivo não encontrado"}
        except Exception as e:
            print(f"{Colors.RED}✗ Erro ao ler arquivo: {e}{Colors.RESET}")
            return {"success": False, "error": str(e)}
        
        return {
            "success": len(self.erros) == 0,
            "total": len(motoristas),
            "importados": motoristas
        }
    
    def importar_veiculos(self, arquivo: str) -> Dict:
        """Importa veículos de CSV"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}=== Importando Veículos ==={Colors.RESET}\n")
        
        veiculos = []
        linha_num = 1
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    linha_num += 1
                    erros_linha = []
                    
                    # Validações obrigatórias
                    if not row.get('placa') or not self.validator.validar_placa(row['placa']):
                        erros_linha.append(f"Placa inválida: {row.get('placa', 'VAZIO')}")
                    
                    if not row.get('tipo'):
                        erros_linha.append("Tipo de veículo é obrigatório")
                    
                    if not row.get('marca'):
                        self.avisos.append(f"Linha {linha_num}: Marca não informada")
                    
                    if not row.get('modelo'):
                        self.avisos.append(f"Linha {linha_num}: Modelo não informado")
                    
                    # Validar capacidade
                    if row.get('capacidade_kg'):
                        try:
                            cap = float(row['capacidade_kg'])
                            if cap <= 0:
                                erros_linha.append("Capacidade deve ser maior que zero")
                        except:
                            erros_linha.append(f"Capacidade inválida: {row['capacidade_kg']}")
                    
                    if erros_linha:
                        self.erros.append(f"Linha {linha_num} ({row.get('placa', 'SEM PLACA')}): {', '.join(erros_linha)}")
                    else:
                        veiculos.append(row)
                        self.sucessos += 1
                        print(f"{Colors.GREEN}✓{Colors.RESET} Veículo: {row['placa']} - {row.get('modelo', 'N/A')}")
        
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Arquivo não encontrado: {arquivo}{Colors.RESET}")
            return {"success": False, "error": "Arquivo não encontrado"}
        except Exception as e:
            print(f"{Colors.RED}✗ Erro ao ler arquivo: {e}{Colors.RESET}")
            return {"success": False, "error": str(e)}
        
        return {
            "success": len(self.erros) == 0,
            "total": len(veiculos),
            "importados": veiculos
        }
    
    def importar_cotacoes(self, arquivo: str) -> Dict:
        """Importa histórico de cotações de CSV"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}=== Importando Cotações ==={Colors.RESET}\n")
        
        cotacoes = []
        linha_num = 1
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    linha_num += 1
                    erros_linha = []
                    
                    # Validações obrigatórias
                    if not row.get('numero'):
                        erros_linha.append("Número da cotação é obrigatório")
                    
                    if not row.get('cliente_nome'):
                        erros_linha.append("Nome do cliente é obrigatório")
                    
                    # Validar CEPs
                    if not row.get('origem_cep') or not self.validator.validar_cep(row['origem_cep']):
                        erros_linha.append(f"CEP origem inválido: {row.get('origem_cep', 'VAZIO')}")
                    
                    if not row.get('destino_cep') or not self.validator.validar_cep(row['destino_cep']):
                        erros_linha.append(f"CEP destino inválido: {row.get('destino_cep', 'VAZIO')}")
                    
                    # Validar valores
                    if row.get('peso_kg'):
                        try:
                            peso = float(row['peso_kg'])
                            if peso <= 0:
                                erros_linha.append("Peso deve ser maior que zero")
                        except:
                            erros_linha.append(f"Peso inválido: {row['peso_kg']}")
                    else:
                        erros_linha.append("Peso é obrigatório")
                    
                    if row.get('valor_total'):
                        try:
                            valor = float(row['valor_total'])
                            if valor < 0:
                                erros_linha.append("Valor total não pode ser negativo")
                        except:
                            erros_linha.append(f"Valor total inválido: {row['valor_total']}")
                    
                    if erros_linha:
                        self.erros.append(f"Linha {linha_num} ({row.get('numero', 'SEM NÚMERO')}): {', '.join(erros_linha)}")
                    else:
                        cotacoes.append(row)
                        self.sucessos += 1
                        print(f"{Colors.GREEN}✓{Colors.RESET} Cotação: {row['numero']} - {row['cliente_nome']}")
        
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Arquivo não encontrado: {arquivo}{Colors.RESET}")
            return {"success": False, "error": "Arquivo não encontrado"}
        except Exception as e:
            print(f"{Colors.RED}✗ Erro ao ler arquivo: {e}{Colors.RESET}")
            return {"success": False, "error": str(e)}
        
        return {
            "success": len(self.erros) == 0,
            "total": len(cotacoes),
            "importados": cotacoes
        }
    
    def gerar_relatorio(self, resultado: Dict, tipo: str):
        """Gera relatório de importação"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}RELATÓRIO DE IMPORTAÇÃO - {tipo.upper()}{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠ MODO DRY-RUN (Simulação) - Nenhum dado foi importado{Colors.RESET}\n")
        
        print(f"Total de registros processados: {resultado.get('total', 0)}")
        print(f"{Colors.GREEN}✓ Sucessos: {self.sucessos}{Colors.RESET}")
        print(f"{Colors.RED}✗ Erros: {len(self.erros)}{Colors.RESET}")
        print(f"{Colors.YELLOW}⚠ Avisos: {len(self.avisos)}{Colors.RESET}\n")
        
        if self.erros:
            print(f"{Colors.RED}{Colors.BOLD}ERROS ENCONTRADOS:{Colors.RESET}")
            for erro in self.erros:
                print(f"  {Colors.RED}✗{Colors.RESET} {erro}")
            print()
        
        if self.avisos:
            print(f"{Colors.YELLOW}{Colors.BOLD}AVISOS:{Colors.RESET}")
            for aviso in self.avisos:
                print(f"  {Colors.YELLOW}⚠{Colors.RESET} {aviso}")
            print()
        
        # Salvar relatório em arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        relatorio_file = f"relatorio_importacao_{tipo}_{timestamp}.json"
        
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            json.dump({
                "tipo": tipo,
                "timestamp": timestamp,
                "dry_run": self.dry_run,
                "total": resultado.get('total', 0),
                "sucessos": self.sucessos,
                "erros": self.erros,
                "avisos": self.avisos
            }, f, indent=2, ensure_ascii=False)
        
        print(f"Relatório salvo em: {relatorio_file}\n")
        
        if resultado.get('success'):
            print(f"{Colors.GREEN}{Colors.BOLD}✓ Importação concluída com sucesso!{Colors.RESET}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}✗ Importação concluída com erros{Colors.RESET}")
        
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def main():
    parser = argparse.ArgumentParser(description='Importar dados para LogiFlow CRM')
    parser.add_argument('--tipo', required=True, choices=['clientes', 'motoristas', 'veiculos', 'cotacoes'],
                       help='Tipo de dados a importar')
    parser.add_argument('--arquivo', required=True, help='Arquivo CSV a importar')
    parser.add_argument('--dry-run', action='store_true', help='Simular importação sem gravar dados')
    
    args = parser.parse_args()
    
    importer = DataImporter(dry_run=args.dry_run)
    
    # Executar importação
    if args.tipo == 'clientes':
        resultado = importer.importar_clientes(args.arquivo)
    elif args.tipo == 'motoristas':
        resultado = importer.importar_motoristas(args.arquivo)
    elif args.tipo == 'veiculos':
        resultado = importer.importar_veiculos(args.arquivo)
    elif args.tipo == 'cotacoes':
        resultado = importer.importar_cotacoes(args.arquivo)
    
    # Gerar relatório
    importer.gerar_relatorio(resultado, args.tipo)
    
    # Retornar código de saída
    sys.exit(0 if resultado.get('success') else 1)


if __name__ == '__main__':
    main()
