"""
Script de teste da integração com Focus NFe
Execute: python scripts/test_focusnfe.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
from loguru import logger


def test_credentials():
    """Testa se o token Focus NFe está configurado"""
    logger.info("🧪 Testando credenciais Focus NFe...")
    
    token = os.getenv("FOCUSNFE_TOKEN")
    environment = os.getenv("FOCUSNFE_ENVIRONMENT", "homologacao")
    
    if not token:
        logger.error("❌ Token não configurado!")
        logger.info("Configure a variável: FOCUSNFE_TOKEN")
        logger.info("Veja: docs/FOCUSNFE_SETUP.md")
        return False
    
    if token.startswith("homologacao_"):
        logger.warning("⚠️  Usando token de HOMOLOGAÇÃO")
    elif token.startswith("producao_"):
        logger.success("✅ Usando token de PRODUÇÃO")
    else:
        logger.error("❌ Formato de token inválido!")
        return False
    
    logger.success(f"✅ Token configurado: {token[:20]}...")
    logger.info(f"   Ambiente: {environment}")
    
    return True


def test_api_connection():
    """Testa conexão com API Focus NFe"""
    logger.info("🧪 Testando conexão com API Focus NFe...")
    
    token = os.getenv("FOCUSNFE_TOKEN")
    
    if not token:
        logger.error("❌ Token não configurado")
        return False
    
    try:
        # Testar endpoint de consulta de empresas
        url = "https://api.focusnfe.com.br/v2/empresas"
        headers = {
            "Authorization": token
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            logger.success("✅ Conexão OK!")
            
            if isinstance(data, list) and len(data) > 0:
                empresa = data[0]
                logger.info(f"   Empresa: {empresa.get('nome_fantasia', 'N/A')}")
                logger.info(f"   CNPJ: {empresa.get('cnpj', 'N/A')}")
            else:
                logger.warning("⚠️  Nenhuma empresa cadastrada")
                logger.info("   Configure pelo painel: https://focusnfe.com.br")
            
            return True
        elif response.status_code == 401:
            logger.error("❌ Token inválido ou expirado")
            return False
        else:
            logger.error(f"❌ Erro na API: {response.status_code}")
            logger.error(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {str(e)}")
        return False


def test_certificate():
    """Verifica se certificado digital está configurado"""
    logger.info("🧪 Verificando certificado digital...")
    
    token = os.getenv("FOCUSNFE_TOKEN")
    
    if not token:
        return False
    
    try:
        url = "https://api.focusnfe.com.br/v2/certificados"
        headers = {
            "Authorization": token
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                cert = data[0]
                logger.success("✅ Certificado digital configurado!")
                logger.info(f"   Válido até: {cert.get('data_vencimento', 'N/A')}")
                logger.info(f"   CNPJ: {cert.get('cnpj', 'N/A')}")
                return True
            else:
                logger.warning("⚠️  Nenhum certificado digital configurado")
                logger.info("   Faça upload no painel: https://focusnfe.com.br")
                return False
        else:
            logger.error(f"❌ Erro ao consultar certificados: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro: {str(e)}")
        return False


def main():
    """Executa todos os testes"""
    logger.info("=" * 70)
    logger.info("🚀 TESTE DE INTEGRAÇÃO - FOCUS NFE")
    logger.info("=" * 70)
    print()
    
    results = {}
    
    # Teste 1: Credenciais
    results["credentials"] = test_credentials()
    print()
    
    if not results["credentials"]:
        logger.error("❌ Configure o token antes de continuar")
        logger.info("Veja: docs/FOCUSNFE_SETUP.md")
        return
    
    # Teste 2: Conexão com API
    results["api_connection"] = test_api_connection()
    print()
    
    # Teste 3: Certificado digital
    results["certificate"] = test_certificate()
    print()
    
    # Resumo
    print("=" * 70)
    logger.info("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        logger.info(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print()
    
    # Verificar se todos passaram
    failed = [name for name, result in results.items() if result is False]
    
    if not failed:
        logger.success("🎉 Todos os testes passaram!")
        logger.info("\n📝 Próximos passos:")
        logger.info("1. Teste emitir CT-e de homologação")
        logger.info("2. Valide XML gerado")
        logger.info("3. Solicite credenciamento na SEFAZ para produção")
    else:
        logger.warning(f"\n⚠️  {len(failed)} teste(s) falharam:")
        for name in failed:
            logger.warning(f"   - {name.replace('_', ' ').title()}")
        logger.info("\nVeja a documentação: docs/FOCUSNFE_SETUP.md")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
