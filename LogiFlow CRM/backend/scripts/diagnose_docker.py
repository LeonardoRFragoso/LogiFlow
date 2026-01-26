"""
Script de diagnóstico para validar configurações Docker
Execute: python scripts/diagnose_docker.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import redis
import psycopg2
from loguru import logger
import requests


def test_redis_connection():
    """Testa conexão com Redis"""
    logger.info("🧪 Testando conexão Redis...")
    
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_password = os.getenv("REDIS_PASSWORD", "redis123")
    
    try:
        client = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True,
            socket_connect_timeout=5
        )
        
        # Testar ping
        client.ping()
        
        # Testar set/get
        test_key = "logiflow:test"
        test_value = "diagnose_ok"
        client.set(test_key, test_value, ex=60)
        retrieved = client.get(test_key)
        
        if retrieved == test_value:
            logger.success(f"✅ Redis OK em {redis_host}:{redis_port}")
            return True
        else:
            logger.error(f"❌ Redis: Valor recuperado não corresponde")
            return False
            
    except redis.exceptions.ConnectionError as e:
        logger.error(f"❌ Redis: Não foi possível conectar em {redis_host}:{redis_port}")
        logger.error(f"   Erro: {str(e)}")
        logger.info("   Verifique se REDIS_HOST está correto no .env (deve ser 'redis' em Docker)")
        return False
    except Exception as e:
        logger.error(f"❌ Redis: Erro inesperado: {str(e)}")
        return False


def test_database_connection():
    """Testa conexão com PostgreSQL"""
    logger.info("🧪 Testando conexão Database...")
    
    db_host = os.getenv("DB_HOST", "db")
    db_port = int(os.getenv("DB_PORT", "5432"))
    db_user = os.getenv("DB_USER", "logiflow")
    db_password = os.getenv("DB_PASSWORD", "logiflow123")
    db_name = os.getenv("DB_NAME", "logiflow")
    
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            dbname=db_name,
            connect_timeout=5,
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()

        connection.close()
        
        logger.success(f"✅ Database OK em {db_host}:{db_port}")
        logger.info(f"   Versão: {version[0]}")
        return True
        
    except psycopg2.OperationalError as e:
        logger.error(f"❌ Database: Não foi possível conectar em {db_host}:{db_port}")
        logger.error(f"   Erro: {str(e)}")
        logger.info("   Verifique se DB_HOST está correto no .env (deve ser 'db' em Docker)")
        return False
    except Exception as e:
        logger.error(f"❌ Database: Erro inesperado: {str(e)}")
        return False


def test_celery_imports():
    """Testa se módulos do Celery podem ser importados"""
    logger.info("🧪 Testando imports do Celery...")
    
    try:
        from celery_app import celery
        logger.success("✅ celery_app.py encontrado")
        
        try:
            from tasks import send_email_async
            logger.success("✅ tasks.py encontrado e tasks importadas")
            return True
        except ImportError as e:
            logger.error(f"❌ Erro ao importar tasks: {str(e)}")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Erro ao importar celery_app: {str(e)}")
        logger.info("   Execute: python scripts/diagnose_docker.py do diretório backend/")
        return False


def test_email_validator():
    """Testa se email-validator está instalado"""
    logger.info("🧪 Testando email-validator...")
    
    try:
        import email_validator
        from pydantic import EmailStr
        
        # Testar validação
        test_email = "teste@exemplo.com"
        validated = EmailStr._validate(test_email)
        
        logger.success("✅ email-validator instalado e funcionando")
        return True
    except ImportError:
        logger.error("❌ email-validator não instalado")
        logger.info("   Execute: pip install 'pydantic[email]'")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao testar email-validator: {str(e)}")
        return False


def check_environment_variables():
    """Verifica se variáveis de ambiente essenciais estão configuradas"""
    logger.info("🧪 Verificando variáveis de ambiente...")
    
    required_vars = {
        "DB_HOST": "db",
        "DB_NAME": "logiflow",
        "DB_USER": "logiflow",
        "REDIS_HOST": "redis",
        "REDIS_PORT": "6379",
    }
    
    optional_vars = {
        "SMTP_HOST": None,
        "SMTP_USER": None,
        "MERCADOPAGO_ACCESS_TOKEN": None,
        "FOCUSNFE_TOKEN": None,
    }
    
    all_ok = True
    
    # Verificar obrigatórias
    for var, expected in required_vars.items():
        value = os.getenv(var)
        if not value:
            logger.error(f"❌ {var} não configurado!")
            all_ok = False
        elif expected and value != expected:
            logger.warning(f"⚠️  {var}={value} (esperado: {expected} para Docker)")
            all_ok = False
        else:
            logger.success(f"✅ {var}={value}")
    
    # Verificar opcionais
    logger.info("\n📋 Variáveis opcionais:")
    for var, _ in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:10] + "..." if len(value) > 10 else value
            logger.info(f"   ✓ {var}={masked}")
        else:
            logger.info(f"   ✗ {var} não configurado (opcional)")
    
    return all_ok


def main():
    """Executa todos os testes de diagnóstico"""
    logger.info("=" * 70)
    logger.info("🔍 DIAGNÓSTICO DO DOCKER - LogiFlow CRM")
    logger.info("=" * 70)
    print()
    
    results = {}
    
    # Teste 1: Variáveis de ambiente
    results["env_vars"] = check_environment_variables()
    print()
    
    # Teste 2: Redis
    results["redis"] = test_redis_connection()
    print()
    
    # Teste 3: Database
    results["database"] = test_database_connection()
    print()
    
    # Teste 4: Celery
    results["celery"] = test_celery_imports()
    print()
    
    # Teste 6: Email validator
    results["email_validator"] = test_email_validator()
    print()
    
    # Resumo
    print("=" * 70)
    logger.info("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        logger.info(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print()
    
    # Verificar se todos passaram
    failed = [name for name, result in results.items() if result is False]
    
    if not failed:
        logger.success("🎉 Todos os testes passaram!")
        logger.info("\nSistema pronto para uso. Execute:")
        logger.info("  docker-compose restart")
    else:
        logger.warning(f"\n⚠️  {len(failed)} teste(s) falharam:")
        for name in failed:
            logger.warning(f"   - {name.replace('_', ' ').title()}")
        
        logger.info("\n📝 Ações recomendadas:")
        if "env_vars" in failed or "redis" in failed or "database" in failed:
            logger.info("1. Copie backend/.env.example para backend/.env")
            logger.info("2. Verifique se as variáveis usam nomes dos serviços Docker:")
            logger.info("   - DB_HOST=db")
            logger.info("   - REDIS_HOST=redis")
        
        if "celery" in failed:
            logger.info("3. Certifique-se de que celery_app.py e tasks.py existem")
        
        if "email_validator" in failed:
            logger.info("4. Instale: pip install 'pydantic[email]'")
        
        logger.info("\n5. Após corrigir, execute:")
        logger.info("   docker-compose down")
        logger.info("   docker-compose up --build -d")
    
    print("=" * 70)
    
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
