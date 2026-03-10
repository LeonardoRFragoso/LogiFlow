"""
Serviço de Criptografia para Dados Sensíveis
Usado para criptografar chaves de API e tokens
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
from loguru import logger


class EncryptionService:
    """Serviço para criptografar/descriptografar dados sensíveis"""
    
    def __init__(self):
        encryption_key = os.getenv("ENCRYPTION_KEY", "")
        
        if not encryption_key:
            logger.warning("⚠️ ENCRYPTION_KEY não definida - usando chave padrão (INSEGURO!)")
            encryption_key = "dev-insecure-key-change-in-production"
        
        self.cipher = self._create_cipher(encryption_key)
    
    def _create_cipher(self, password: str) -> Fernet:
        """Cria cipher Fernet a partir de uma senha"""
        salt = b'logiflow-salt-v1'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Criptografa string
        
        Args:
            data: String a criptografar
            
        Returns:
            String criptografada (base64)
        """
        if not data:
            return ""
        
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"❌ Erro ao criptografar dados: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Descriptografa string
        
        Args:
            encrypted_data: String criptografada
            
        Returns:
            String descriptografada
        """
        if not encrypted_data:
            return ""
        
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"❌ Erro ao descriptografar dados: {e}")
            raise


# Instância global
encryption_service = EncryptionService()


def encrypt_api_key(api_key: str) -> str:
    """Helper para criptografar API key"""
    return encryption_service.encrypt(api_key)


def decrypt_api_key(encrypted_key: str) -> str:
    """Helper para descriptografar API key"""
    return encryption_service.decrypt(encrypted_key)
