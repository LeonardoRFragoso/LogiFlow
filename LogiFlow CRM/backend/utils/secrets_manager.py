"""
Secrets Management
==================
Gerenciamento seguro de secrets usando multiple backends
- Local (development): arquivo .env encriptado
- AWS Secrets Manager (production)
- HashiCorp Vault (enterprise)
- Environment variables (fallback)
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from pathlib import Path
import base64

logger = logging.getLogger(__name__)


# ========================================
# Interface Abstrata
# ========================================

class SecretsBackend(ABC):
    """Interface para diferentes backends de secrets"""
    
    @abstractmethod
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Retorna valor de um secret"""
        pass
    
    @abstractmethod
    def get_secrets_dict(self, prefix: str = "") -> Dict[str, str]:
        """Retorna dicionário de secrets com prefix"""
        pass
    
    @abstractmethod
    def set_secret(self, secret_name: str, secret_value: str) -> bool:
        """Define um secret"""
        pass
    
    @abstractmethod
    def delete_secret(self, secret_name: str) -> bool:
        """Deleta um secret"""
        pass
    
    @abstractmethod
    def verify_connection(self) -> bool:
        """Verifica conexão com backend"""
        pass


# ========================================
# Environment Variables Backend
# ========================================

class EnvironmentBackend(SecretsBackend):
    """Lê secrets de variáveis de ambiente"""
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        return os.getenv(secret_name)
    
    def get_secrets_dict(self, prefix: str = "") -> Dict[str, str]:
        """Retorna todas as env vars com prefix"""
        result = {}
        for key, value in os.environ.items():
            if prefix == "" or key.startswith(prefix):
                result[key] = value
        return result
    
    def set_secret(self, secret_name: str, secret_value: str) -> bool:
        os.environ[secret_name] = secret_value
        return True
    
    def delete_secret(self, secret_name: str) -> bool:
        if secret_name in os.environ:
            del os.environ[secret_name]
            return True
        return False
    
    def verify_connection(self) -> bool:
        return True


# ========================================
# AWS Secrets Manager Backend
# ========================================

class AWSSecretsManagerBackend(SecretsBackend):
    """Integração com AWS Secrets Manager"""
    
    def __init__(self, region_name: str = "us-east-1"):
        try:
            import boto3
            self.client = boto3.client("secretsmanager", region_name=region_name)
            self.available = True
        except ImportError:
            logger.warning("boto3 não instalado, AWS Secrets Manager indisponível")
            self.available = False
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        if not self.available:
            return None
        
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            
            if "SecretString" in response:
                return response["SecretString"]
            else:
                # Binary secret
                return base64.b64decode(response["SecretBinary"]).decode("utf-8")
        
        except Exception as e:
            logger.error(f"Erro ao buscar secret {secret_name}: {e}")
            return None
    
    def get_secrets_dict(self, prefix: str = "") -> Dict[str, str]:
        """Retorna secrets começando com prefix"""
        if not self.available:
            return {}
        
        try:
            result = {}
            response = self.client.list_secrets()
            
            for secret in response.get("SecretList", []):
                secret_name = secret["Name"]
                if prefix == "" or secret_name.startswith(prefix):
                    value = self.get_secret(secret_name)
                    if value:
                        result[secret_name] = value
            
            return result
        except Exception as e:
            logger.error(f"Erro ao listar secrets: {e}")
            return {}
    
    def set_secret(self, secret_name: str, secret_value: str) -> bool:
        if not self.available:
            return False
        
        try:
            self.client.put_secret_value(
                SecretId=secret_name,
                SecretString=secret_value
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao definir secret {secret_name}: {e}")
            return False
    
    def delete_secret(self, secret_name: str) -> bool:
        if not self.available:
            return False
        
        try:
            self.client.delete_secret(
                SecretId=secret_name,
                ForceDeleteWithoutRecovery=False
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar secret {secret_name}: {e}")
            return False
    
    def verify_connection(self) -> bool:
        if not self.available:
            return False
        
        try:
            self.client.list_secrets(MaxResults=1)
            return True
        except Exception as e:
            logger.error(f"Falha ao conectar AWS Secrets Manager: {e}")
            return False


# ========================================
# HashiCorp Vault Backend
# ========================================

class VaultBackend(SecretsBackend):
    """Integração com HashiCorp Vault"""
    
    def __init__(self, vault_addr: str = "http://localhost:8200", vault_token: str = None):
        try:
            import hvac
            
            self.addr = vault_addr
            self.token = vault_token or os.getenv("VAULT_TOKEN")
            self.path_prefix = os.getenv("VAULT_SECRET_PREFIX", "secret/logiflow")
            
            self.client = hvac.Client(url=vault_addr, token=self.token)
            self.available = True
        except ImportError:
            logger.warning("hvac não instalado, Vault indisponível")
            self.available = False
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        if not self.available:
            return None
        
        try:
            path = f"{self.path_prefix}/{secret_name}"
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            
            # Vault KV v2 retorna data dentro de um wrapper
            data = response.get("data", {}).get("data", {})
            return data.get("value")
        except Exception as e:
            logger.error(f"Erro ao buscar secret do Vault {secret_name}: {e}")
            return None
    
    def get_secrets_dict(self, prefix: str = "") -> Dict[str, str]:
        """List secrets com prefix no Vault"""
        if not self.available:
            return {}
        
        try:
            result = {}
            path = f"{self.path_prefix}/{prefix}" if prefix else self.path_prefix
            
            response = self.client.secrets.kv.v2.list_secrets(path=path)
            keys = response.get("data", {}).get("keys", [])
            
            for key in keys:
                value = self.get_secret(f"{prefix}/{key}" if prefix else key)
                if value:
                    result[key] = value
            
            return result
        except Exception as e:
            logger.error(f"Erro ao listar secrets do Vault: {e}")
            return {}
    
    def set_secret(self, secret_name: str, secret_value: str) -> bool:
        if not self.available:
            return False
        
        try:
            path = f"{self.path_prefix}/{secret_name}"
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret_data={"value": secret_value}
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao definir secret no Vault {secret_name}: {e}")
            return False
    
    def delete_secret(self, secret_name: str) -> bool:
        if not self.available:
            return False
        
        try:
            path = f"{self.path_prefix}/{secret_name}"
            self.client.secrets.kv.v2.delete_secret_version(path=path)
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar secret do Vault {secret_name}: {e}")
            return False
    
    def verify_connection(self) -> bool:
        if not self.available:
            return False
        
        try:
            self.client.is_authenticated()
            return True
        except Exception as e:
            logger.error(f"Falha ao conectar Vault: {e}")
            return False


# ========================================
# Manager Principal
# ========================================

class SecretsManager:
    """Gerenciador de secrets com suporte a múltiplos backends"""
    
    def __init__(self, backend: SecretsBackend = None):
        """
        Inicializa manager com backend apropriado
        
        Args:
            backend: SecretsBackend customizado (por padrão, detecta automáticamente)
        """
        if backend:
            self.backend = backend
        else:
            self.backend = self._select_backend()
        
        logger.info(f"SecretsManager inicializado com: {self.backend.__class__.__name__}")
    
    def _select_backend(self) -> SecretsBackend:
        """
        Seleciona backend baseado no ambiente
        Priority: Vault > AWS Secrets Manager > Environment
        """
        # Tentar Vault primeiro
        if os.getenv("VAULT_ADDR"):
            vault_backend = VaultBackend()
            if vault_backend.verify_connection():
                logger.info("✓ Vault disponível, usando como secrets backend")
                return vault_backend
        
        # Tentar AWS Secrets Manager
        if os.getenv("AWS_REGION"):
            aws_backend = AWSSecretsManagerBackend(region_name=os.getenv("AWS_REGION"))
            if aws_backend.verify_connection():
                logger.info("✓ AWS Secrets Manager disponível, usando como backend")
                return aws_backend
        
        # Fallback para Environment
        logger.info("Usando Environment Variables como secrets backend")
        return EnvironmentBackend()
    
    def get(self, secret_name: str, default: Optional[str] = None) -> Optional[str]:
        """
        Obtém um secret
        
        Args:
            secret_name: Nome do secret
            default: Valor padrão se não encontrado
        
        Returns:
            Valor do secret ou default
        """
        value = self.backend.get_secret(secret_name)
        if value is None:
            logger.warning(f"Secret '{secret_name}' não encontrado")
            return default
        return value
    
    def get_required(self, secret_name: str) -> str:
        """
        Obtém um secret obrigatório
        
        Args:
            secret_name: Nome do secret
        
        Returns:
            Valor do secret
        
        Raises:
            ValueError: Se secret não encontrado
        """
        value = self.get(secret_name)
        if value is None:
            raise ValueError(f"Secret obrigatório '{secret_name}' não configurado")
        return value
    
    def get_dict(self, prefix: str = "") -> Dict[str, str]:
        """
        Obtém dicionário de secrets com prefix
        
        Args:
            prefix: Prefixo dos secrets (ex: "DB_" para DB_HOST, DB_USER, etc)
        
        Returns:
            Dicionário de secrets
        """
        return self.backend.get_secrets_dict(prefix)
    
    def set(self, secret_name: str, secret_value: str) -> bool:
        """
        Define um secret
        
        Args:
            secret_name: Nome do secret
            secret_value: Valor do secret
        
        Returns:
            True se sucesso
        """
        return self.backend.set_secret(secret_name, secret_value)
    
    def delete(self, secret_name: str) -> bool:
        """
        Deleta um secret
        
        Args:
            secret_name: Nome do secret
        
        Returns:
            True se sucesso
        """
        return self.backend.delete_secret(secret_name)
    
    def verify(self) -> bool:
        """
        Verifica se backend está conectado
        
        Returns:
            True se conectado
        """
        return self.backend.verify_connection()


# ========================================
# Instância Global
# ========================================

# Criar instância global do manager
secrets_manager = SecretsManager()


# ========================================
# Helpers para uso rápido
# ========================================

def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """Shortcut para secrets_manager.get()"""
    return secrets_manager.get(name, default)


def get_required(name: str) -> str:
    """Shortcut para secrets_manager.get_required()"""
    return secrets_manager.get_required(name)


def set_secret(name: str, value: str) -> bool:
    """Shortcut para secrets_manager.set()"""
    return secrets_manager.set(name, value)


# ========================================
# Validação de Secrets
# ========================================

def validate_required_secrets(*secret_names) -> bool:
    """
    Valida se todos os secrets obrigatórios estão configurados
    
    Args:
        *secret_names: Nomes dos secrets a validar
    
    Returns:
        True se todos presentes
    
    Raises:
        ValueError: Se algum secret estiver faltando
    """
    missing = []
    for name in secret_names:
        if not get_secret(name):
            missing.append(name)
    
    if missing:
        raise ValueError(f"Secrets obrigatórios faltando: {', '.join(missing)}")
    
    return True
