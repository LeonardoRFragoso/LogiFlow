"""
Documento Value Objects - CNPJ e CPF com validação
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CNPJ:
    """Value Object para CNPJ com validação"""
    valor: str
    
    def __post_init__(self):
        cnpj_limpo = re.sub(r'\D', '', self.valor)
        if len(cnpj_limpo) != 14:
            raise ValueError(f"CNPJ inválido: deve ter 14 dígitos")
        if not self._validar_cnpj(cnpj_limpo):
            raise ValueError(f"CNPJ inválido: dígitos verificadores incorretos")
        # Usar object.__setattr__ porque dataclass é frozen
        object.__setattr__(self, 'valor', cnpj_limpo)
    
    @staticmethod
    def _validar_cnpj(cnpj: str) -> bool:
        """Valida dígitos verificadores do CNPJ"""
        if cnpj == cnpj[0] * 14:
            return False
        
        def calc_digito(cnpj: str, pesos: list) -> int:
            soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        d1 = calc_digito(cnpj[:12], pesos1)
        d2 = calc_digito(cnpj[:12] + str(d1), pesos2)
        
        return cnpj[-2:] == f"{d1}{d2}"
    
    @property
    def formatado(self) -> str:
        """Retorna CNPJ formatado (XX.XXX.XXX/XXXX-XX)"""
        v = self.valor
        return f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"
    
    def __str__(self) -> str:
        return self.formatado


@dataclass(frozen=True)
class CPF:
    """Value Object para CPF com validação"""
    valor: str
    
    def __post_init__(self):
        cpf_limpo = re.sub(r'\D', '', self.valor)
        if len(cpf_limpo) != 11:
            raise ValueError(f"CPF inválido: deve ter 11 dígitos")
        if not self._validar_cpf(cpf_limpo):
            raise ValueError(f"CPF inválido: dígitos verificadores incorretos")
        object.__setattr__(self, 'valor', cpf_limpo)
    
    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """Valida dígitos verificadores do CPF"""
        if cpf == cpf[0] * 11:
            return False
        
        def calc_digito(cpf: str, pesos: list) -> int:
            soma = sum(int(d) * p for d, p in zip(cpf, pesos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        pesos1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        
        d1 = calc_digito(cpf[:9], pesos1)
        d2 = calc_digito(cpf[:9] + str(d1), pesos2)
        
        return cpf[-2:] == f"{d1}{d2}"
    
    @property
    def formatado(self) -> str:
        """Retorna CPF formatado (XXX.XXX.XXX-XX)"""
        v = self.valor
        return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}"
    
    def __str__(self) -> str:
        return self.formatado
