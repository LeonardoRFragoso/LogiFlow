"""
Domain Exceptions - Exceções específicas da camada de domínio
"""
from typing import Optional


class DomainException(Exception):
    """Exceção base para erros de domínio"""
    
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code or "DOMAIN_ERROR"
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    """Exceção quando uma entidade não é encontrada"""
    
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(
            message=f"{entity_type} não encontrado(a): {entity_id}",
            code="ENTITY_NOT_FOUND"
        )


class ValidationException(DomainException):
    """Exceção para erros de validação de dados"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(
            message=message,
            code="VALIDATION_ERROR"
        )


class BusinessRuleException(DomainException):
    """Exceção para violação de regras de negócio"""
    
    def __init__(self, message: str, rule: Optional[str] = None):
        self.rule = rule
        super().__init__(
            message=message,
            code="BUSINESS_RULE_VIOLATION"
        )
