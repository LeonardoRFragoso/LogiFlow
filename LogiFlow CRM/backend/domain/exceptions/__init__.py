"""Domain Exceptions - Exceções específicas do domínio"""
from .domain_exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    BusinessRuleException,
)

__all__ = [
    "DomainException",
    "EntityNotFoundException", 
    "ValidationException",
    "BusinessRuleException",
]
