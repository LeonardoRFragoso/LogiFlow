"""
CORS Security Configuration
===========================
Middleware de CORS seguro e restritivo para produção
"""
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from config import settings
import logging

logger = logging.getLogger(__name__)


def setup_cors(app, allowed_origins: List[str] = None):
    """
    Configura CORS de forma segura para produção
    
    Args:
        app: Aplicação FastAPI
        allowed_origins: Lista de origens permitidas (padrão: do settings)
    """
    
    # Se não fornecido, usar do settings
    if allowed_origins is None:
        allowed_origins = settings.ALLOWED_ORIGINS
    
    # Validar que não é allow_origins=["*"] em produção
    if not settings.DEBUG and "*" in allowed_origins:
        logger.warning(
            "CORS com allow_origins=['*'] detectado em PRODUCTION! "
            "Configurando apenas origins explícitas."
        )
        # Usar origins específicas
        allowed_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080",
        ]
    
    # Aplicar middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Accept",
            "Accept-Language",
            "Content-Type",
            "Authorization",
            "X-Tenant-ID",
            "X-Correlation-ID",
            "X-Requested-With"
        ],
        expose_headers=[
            "Content-Length",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
            "X-Correlation-ID"
        ],
        max_age=3600  # 1 hora de cache para preflight
    )
    
    logger.info(
        f"CORS configurado para origins: {allowed_origins}",
        extra={
            "allowed_origins": allowed_origins,
            "environment": "production" if not settings.DEBUG else "development"
        }
    )


# ========================================
# Validação de CORS
# ========================================

def validate_cors_origin(origin: str, allowed_origins: List[str]) -> bool:
    """
    Valida se origin é permitida
    """
    if "*" in allowed_origins:
        return True
    
    return origin in allowed_origins


# ========================================
# Recomendações de CORS para Produção
# ========================================

CORS_SECURITY_GUIDELINES = {
    "never_use_wildcard": {
        "description": "Nunca usar allow_origins=['*'] em produção",
        "impact": "Vulnerabilidade CSRF, qualquer site pode acessar API",
        "fix": "Especificar exatamente quais origins são permitidas"
    },
    
    "restrict_methods": {
        "description": "Permitir apenas métodos necessários",
        "impact": "DELETE, PATCH mal configurados podem causar danos",
        "fix": "Listar explicitamente: GET, POST, PUT, DELETE conforme necessário"
    },
    
    "restrict_headers": {
        "description": "Permitir apenas headers necessários",
        "impact": "Headers customizados podem ser vetores de ataque",
        "fix": "Listar explicitamente headers como Authorization, X-Tenant-ID"
    },
    
    "credentials": {
        "description": "allow_credentials=True requer origins específicas",
        "impact": "Combine com wildcard é vulnerabilidade crítica",
        "fix": "Se allow_credentials=True, nunca usar wildcard"
    },
    
    "preflight_cache": {
        "description": "Cachear respostas preflight reduz requisições",
        "impact": "Sem cache: 2 requisições por operação (preflight + real)",
        "fix": "Configurar max_age apropriado (ex: 3600s)"
    }
}


# ========================================
# Configurações por Ambiente
# ========================================

CORS_CONFIG_DEVELOPMENT = {
    "allow_origins": [
        "http://localhost:3000",      # Frontend local Vue
        "http://localhost:5173",      # Vite dev
        "http://localhost:8080",      # Porta alternativa
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
    ],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

CORS_CONFIG_STAGING = {
    "allow_origins": [
        "https://beta.logiflow.com",
        "https://admin-beta.logiflow.com",
        "https://motorista-beta.logiflow.com",
        "http://localhost:3000",  # Para testes locais
    ],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    "allow_headers": [
        "Accept",
        "Content-Type", 
        "Authorization",
        "X-Tenant-ID",
        "X-Correlation-ID",
    ],
    "max_age": 3600,
}

CORS_CONFIG_PRODUCTION = {
    "allow_origins": [
        "https://logiflow.com",
        "https://www.logiflow.com",
        "https://app.logiflow.com",
        "https://admin.logiflow.com",
        "https://motorista.logiflow.com",
        "https://portal-cliente.logiflow.com",
    ],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
    "allow_headers": [
        "Accept",
        "Content-Type",
        "Authorization",
        "X-Tenant-ID",
        "X-Correlation-ID",
        "X-Requested-With",
    ],
    "expose_headers": [
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
        "X-RateLimit-Reset",
    ],
    "max_age": 7200,  # 2 horas
}


def get_cors_config():
    """
    Retorna configuração CORS apropriada baseada no ambiente
    """
    if settings.DEBUG:
        return CORS_CONFIG_DEVELOPMENT
    
    environment = getattr(settings, "ENVIRONMENT", "production").lower()
    
    if environment == "staging":
        return CORS_CONFIG_STAGING
    elif environment == "production":
        return CORS_CONFIG_PRODUCTION
    else:
        # Default para segurança
        return CORS_CONFIG_PRODUCTION


# ========================================
# Helpers
# ========================================

def print_cors_security_checklist():
    """
    Printa checklist de segurança CORS
    """
    print("\n" + "="*60)
    print("CORS SECURITY CHECKLIST")
    print("="*60)
    
    for key, info in CORS_SECURITY_GUIDELINES.items():
        print(f"\n✓ {key.upper().replace('_', ' ')}")
        print(f"  Description: {info['description']}")
        print(f"  Impact: {info['impact']}")
        print(f"  Recomendação: {info['fix']}")
    
    print("\n" + "="*60 + "\n")
