"""
Endereco Value Object - Representa um endereço completo
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Endereco:
    """
    Value Object imutável para endereço.
    Dois endereços são iguais se todos os campos forem iguais.
    """
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    uf: str
    cep: str
    complemento: Optional[str] = None
    
    def __post_init__(self):
        if not self.logradouro or not self.logradouro.strip():
            raise ValueError("Logradouro é obrigatório")
        if not self.cidade or not self.cidade.strip():
            raise ValueError("Cidade é obrigatória")
        if not self.uf or len(self.uf) != 2:
            raise ValueError("UF deve ter 2 caracteres")
        if not self.cep:
            raise ValueError("CEP é obrigatório")
    
    @property
    def cep_formatado(self) -> str:
        """Retorna CEP formatado (XXXXX-XXX)"""
        cep_limpo = "".join(filter(str.isdigit, self.cep))
        if len(cep_limpo) == 8:
            return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
        return self.cep
    
    @property
    def endereco_completo(self) -> str:
        """Retorna endereço formatado em uma linha"""
        partes = [self.logradouro, self.numero]
        if self.complemento:
            partes.append(self.complemento)
        partes.extend([self.bairro, self.cidade, self.uf, self.cep_formatado])
        return ", ".join(partes)
    
    def __str__(self) -> str:
        return self.endereco_completo
