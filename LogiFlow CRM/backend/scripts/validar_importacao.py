"""
Script de Validação de Dados para Importação
Valida templates CSV/Excel antes de importar para o LogiFlow CRM
"""

import pandas as pd
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import argparse

class ValidadorImportacao:
    """Validador de dados de importação"""
    
    def __init__(self, arquivo: str, tipo: str):
        self.arquivo = Path(arquivo)
        self.tipo = tipo.lower()
        self.erros = []
        self.avisos = []
        self.df = None
        
    def validar_cpf(self, cpf: str) -> bool:
        """Valida CPF"""
        if pd.isna(cpf):
            return False
        
        cpf = re.sub(r'[^0-9]', '', str(cpf))
        
        if len(cpf) != 11:
            return False
        
        if cpf == cpf[0] * 11:
            return False
        
        # Validar dígitos verificadores
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        
        return cpf[-2:] == f"{digito1}{digito2}"
    
    def validar_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ"""
        if pd.isna(cnpj):
            return False
        
        cnpj = re.sub(r'[^0-9]', '', str(cnpj))
        
        if len(cnpj) != 14:
            return False
        
        if cnpj == cnpj[0] * 14:
            return False
        
        # Validar dígitos verificadores
        def calcular_digito(cnpj_parcial, pesos):
            soma = sum(int(cnpj_parcial[i]) * pesos[i] for i in range(len(pesos)))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
        pesos2 = [6,5,4,3,2,9,8,7,6,5,4,3,2]
        
        digito1 = calcular_digito(cnpj[:12], pesos1)
        digito2 = calcular_digito(cnpj[:13], pesos2)
        
        return cnpj[-2:] == f"{digito1}{digito2}"
    
    def validar_email(self, email: str) -> bool:
        """Valida email"""
        if pd.isna(email):
            return False
        
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, str(email)))
    
    def validar_telefone(self, telefone: str) -> bool:
        """Valida telefone"""
        if pd.isna(telefone):
            return False
        
        telefone = re.sub(r'[^0-9]', '', str(telefone))
        return len(telefone) in [10, 11]  # (11) 98888-8888 ou (11) 3888-8888
    
    def validar_cep(self, cep: str) -> bool:
        """Valida CEP"""
        if pd.isna(cep):
            return False
        
        cep = re.sub(r'[^0-9]', '', str(cep))
        return len(cep) == 8
    
    def validar_placa(self, placa: str) -> bool:
        """Valida placa de veículo (Mercosul ou antiga)"""
        if pd.isna(placa):
            return False
        
        placa = str(placa).upper().replace('-', '').replace(' ', '')
        
        # Mercosul: ABC1D23
        mercosul = bool(re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', placa))
        
        # Antiga: ABC1234
        antiga = bool(re.match(r'^[A-Z]{3}[0-9]{4}$', placa))
        
        return mercosul or antiga
    
    def validar_data(self, data: str) -> bool:
        """Valida data"""
        if pd.isna(data):
            return False
        
        formatos = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']
        
        for formato in formatos:
            try:
                datetime.strptime(str(data), formato)
                return True
            except ValueError:
                continue
        
        return False
    
    def carregar_arquivo(self) -> bool:
        """Carrega arquivo CSV/Excel"""
        try:
            if self.arquivo.suffix == '.csv':
                self.df = pd.read_csv(self.arquivo)
            elif self.arquivo.suffix in ['.xlsx', '.xls']:
                self.df = pd.read_excel(self.arquivo)
            else:
                self.erros.append(f"Formato de arquivo não suportado: {self.arquivo.suffix}")
                return False
            
            print(f"✅ Arquivo carregado: {len(self.df)} registros encontrados")
            return True
        
        except Exception as e:
            self.erros.append(f"Erro ao carregar arquivo: {str(e)}")
            return False
    
    def validar_clientes(self):
        """Valida template de clientes"""
        print("\n🔍 Validando clientes...")
        
        # Campos obrigatórios
        campos_obrigatorios = ['nome', 'cnpj', 'email', 'telefone']
        
        for campo in campos_obrigatorios:
            if campo not in self.df.columns:
                self.erros.append(f"Campo obrigatório ausente: {campo}")
        
        if self.erros:
            return
        
        # Validar cada registro
        for idx, row in self.df.iterrows():
            linha = idx + 2  # +2 porque Excel começa em 1 e tem header
            
            # Nome
            if pd.isna(row['nome']) or str(row['nome']).strip() == '':
                self.erros.append(f"Linha {linha}: Nome vazio")
            
            # CNPJ
            if not self.validar_cnpj(row['cnpj']):
                self.erros.append(f"Linha {linha}: CNPJ inválido ({row['cnpj']})")
            
            # Email
            if not self.validar_email(row['email']):
                self.erros.append(f"Linha {linha}: Email inválido ({row['email']})")
            
            # Telefone
            if not self.validar_telefone(row['telefone']):
                self.avisos.append(f"Linha {linha}: Telefone pode estar inválido ({row['telefone']})")
            
            # CEP (opcional)
            if 'cep' in row and not pd.isna(row['cep']):
                if not self.validar_cep(row['cep']):
                    self.avisos.append(f"Linha {linha}: CEP inválido ({row['cep']})")
        
        # Verificar duplicatas
        duplicatas = self.df[self.df.duplicated(subset=['cnpj'], keep=False)]
        if not duplicatas.empty:
            cnpjs = duplicatas['cnpj'].unique()
            self.avisos.append(f"CNPJs duplicados encontrados: {', '.join(map(str, cnpjs))}")
    
    def validar_motoristas(self):
        """Valida template de motoristas"""
        print("\n🔍 Validando motoristas...")
        
        campos_obrigatorios = ['nome', 'cpf', 'cnh', 'categoria_cnh']
        
        for campo in campos_obrigatorios:
            if campo not in self.df.columns:
                self.erros.append(f"Campo obrigatório ausente: {campo}")
        
        if self.erros:
            return
        
        categorias_validas = ['A', 'B', 'C', 'D', 'E', 'AB', 'AC', 'AD', 'AE']
        
        for idx, row in self.df.iterrows():
            linha = idx + 2
            
            # Nome
            if pd.isna(row['nome']) or str(row['nome']).strip() == '':
                self.erros.append(f"Linha {linha}: Nome vazio")
            
            # CPF
            if not self.validar_cpf(row['cpf']):
                self.erros.append(f"Linha {linha}: CPF inválido ({row['cpf']})")
            
            # CNH
            if pd.isna(row['cnh']) or len(str(row['cnh']).replace(' ', '')) != 11:
                self.erros.append(f"Linha {linha}: CNH inválida ({row['cnh']})")
            
            # Categoria CNH
            categoria = str(row['categoria_cnh']).upper().strip()
            if categoria not in categorias_validas:
                self.erros.append(f"Linha {linha}: Categoria CNH inválida ({categoria}). Válidas: {', '.join(categorias_validas)}")
            
            # Data vencimento CNH (opcional)
            if 'vencimento_cnh' in row and not pd.isna(row['vencimento_cnh']):
                if not self.validar_data(row['vencimento_cnh']):
                    self.avisos.append(f"Linha {linha}: Data de vencimento CNH inválida")
        
        # Verificar duplicatas
        duplicatas = self.df[self.df.duplicated(subset=['cpf'], keep=False)]
        if not duplicatas.empty:
            cpfs = duplicatas['cpf'].unique()
            self.avisos.append(f"CPFs duplicados encontrados: {', '.join(map(str, cpfs))}")
    
    def validar_veiculos(self):
        """Valida template de veículos"""
        print("\n🔍 Validando veículos...")
        
        campos_obrigatorios = ['placa', 'tipo', 'marca', 'modelo']
        
        for campo in campos_obrigatorios:
            if campo not in self.df.columns:
                self.erros.append(f"Campo obrigatório ausente: {campo}")
        
        if self.erros:
            return
        
        tipos_validos = ['Caminhão', 'Van', 'Carreta', 'Bitrem', 'Truck', 'Toco', '3/4']
        
        for idx, row in self.df.iterrows():
            linha = idx + 2
            
            # Placa
            if not self.validar_placa(row['placa']):
                self.erros.append(f"Linha {linha}: Placa inválida ({row['placa']})")
            
            # Tipo
            if pd.isna(row['tipo']) or str(row['tipo']).strip() == '':
                self.erros.append(f"Linha {linha}: Tipo vazio")
            elif row['tipo'] not in tipos_validos:
                self.avisos.append(f"Linha {linha}: Tipo '{row['tipo']}' não está na lista padrão")
            
            # Marca e Modelo
            if pd.isna(row['marca']) or str(row['marca']).strip() == '':
                self.erros.append(f"Linha {linha}: Marca vazia")
            
            if pd.isna(row['modelo']) or str(row['modelo']).strip() == '':
                self.erros.append(f"Linha {linha}: Modelo vazio")
        
        # Verificar duplicatas
        duplicatas = self.df[self.df.duplicated(subset=['placa'], keep=False)]
        if not duplicatas.empty:
            placas = duplicatas['placa'].unique()
            self.avisos.append(f"Placas duplicadas encontradas: {', '.join(map(str, placas))}")
    
    def validar_cotacoes(self):
        """Valida template de cotações"""
        print("\n🔍 Validando cotações...")
        
        campos_obrigatorios = ['cliente', 'origem', 'destino', 'valor', 'data']
        
        for campo in campos_obrigatorios:
            if campo not in self.df.columns:
                self.erros.append(f"Campo obrigatório ausente: {campo}")
        
        if self.erros:
            return
        
        for idx, row in self.df.iterrows():
            linha = idx + 2
            
            # Cliente
            if pd.isna(row['cliente']) or str(row['cliente']).strip() == '':
                self.erros.append(f"Linha {linha}: Cliente vazio")
            
            # Origem e Destino
            if pd.isna(row['origem']) or str(row['origem']).strip() == '':
                self.erros.append(f"Linha {linha}: Origem vazia")
            
            if pd.isna(row['destino']) or str(row['destino']).strip() == '':
                self.erros.append(f"Linha {linha}: Destino vazio")
            
            # Valor
            try:
                valor = float(str(row['valor']).replace(',', '.').replace('R$', '').strip())
                if valor <= 0:
                    self.avisos.append(f"Linha {linha}: Valor zerado ou negativo")
            except:
                self.erros.append(f"Linha {linha}: Valor inválido ({row['valor']})")
            
            # Data
            if not self.validar_data(row['data']):
                self.erros.append(f"Linha {linha}: Data inválida ({row['data']})")
    
    def executar(self) -> bool:
        """Executa validação completa"""
        print(f"\n{'='*60}")
        print(f"🔍 VALIDAÇÃO DE IMPORTAÇÃO - LogiFlow CRM")
        print(f"{'='*60}")
        print(f"Arquivo: {self.arquivo}")
        print(f"Tipo: {self.tipo}")
        
        # Carregar arquivo
        if not self.carregar_arquivo():
            return False
        
        # Validar conforme tipo
        if self.tipo == 'clientes':
            self.validar_clientes()
        elif self.tipo == 'motoristas':
            self.validar_motoristas()
        elif self.tipo == 'veiculos':
            self.validar_veiculos()
        elif self.tipo == 'cotacoes':
            self.validar_cotacoes()
        else:
            self.erros.append(f"Tipo inválido: {self.tipo}. Use: clientes, motoristas, veiculos ou cotacoes")
            return False
        
        # Exibir resultados
        self.exibir_resultados()
        
        return len(self.erros) == 0
    
    def exibir_resultados(self):
        """Exibe resultados da validação"""
        print(f"\n{'='*60}")
        print("📊 RESULTADO DA VALIDAÇÃO")
        print(f"{'='*60}")
        
        if not self.erros and not self.avisos:
            print("✅ Nenhum erro ou aviso encontrado!")
            print("✅ Arquivo pronto para importação!")
        else:
            if self.erros:
                print(f"\n❌ ERROS ({len(self.erros)}):")
                for erro in self.erros[:20]:  # Limitar a 20 erros
                    print(f"   • {erro}")
                if len(self.erros) > 20:
                    print(f"   ... e mais {len(self.erros) - 20} erros")
            
            if self.avisos:
                print(f"\n⚠️  AVISOS ({len(self.avisos)}):")
                for aviso in self.avisos[:10]:  # Limitar a 10 avisos
                    print(f"   • {aviso}")
                if len(self.avisos) > 10:
                    print(f"   ... e mais {len(self.avisos) - 10} avisos")
        
        print(f"\n{'='*60}")
        
        if self.erros:
            print("❌ Corrija os erros antes de importar")
            print(f"{'='*60}\n")
            return False
        elif self.avisos:
            print("⚠️  Revise os avisos antes de importar")
            print(f"{'='*60}\n")
            return True
        else:
            print("✅ Validação concluída com sucesso!")
            print(f"{'='*60}\n")
            return True


def main():
    parser = argparse.ArgumentParser(description='Validar dados para importação no LogiFlow CRM')
    parser.add_argument('--arquivo', required=True, help='Caminho do arquivo CSV/Excel')
    parser.add_argument('--tipo', required=True, choices=['clientes', 'motoristas', 'veiculos', 'cotacoes'],
                       help='Tipo de dados a validar')
    
    args = parser.parse_args()
    
    validador = ValidadorImportacao(args.arquivo, args.tipo)
    sucesso = validador.executar()
    
    sys.exit(0 if sucesso else 1)


if __name__ == '__main__':
    main()
