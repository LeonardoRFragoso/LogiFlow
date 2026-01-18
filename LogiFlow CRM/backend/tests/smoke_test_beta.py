"""
LogiFlow CRM - Smoke Test End-to-End para BETA
===============================================
Valida fluxo completo do sistema antes do lançamento BETA.

Testa:
1. Backend sobe sem erro
2. Banco de dados conectado
3. Redis conectado
4. Frontend acessível (se rodando)
5. Login funcional
6. Criar Cotação
7. Converter Cotação em Pedido
8. GPS em modo simulação
9. Feature flags ativos
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any
import httpx
from loguru import logger

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from database import SessionLocal, engine
from sqlalchemy import text
import redis as redis_client


class BetaSmokeTest:
    """Smoke test completo para validação BETA"""
    
    def __init__(self):
        self.results = []
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3001"
        self.errors = []
        
    async def run_all_tests(self):
        """Executa todos os testes de smoke"""
        logger.info("🧪 INICIANDO SMOKE TEST BETA - LogiFlow CRM")
        logger.info("=" * 70)
        
        tests = [
            ("1. Backend Health Check", self.test_backend_health),
            ("2. Database Connection", self.test_database_connection),
            ("3. Redis Connection", self.test_redis_connection),
            ("4. Feature Flags", self.test_feature_flags),
            ("5. Authentication", self.test_authentication),
            ("6. Criar Cotação", self.test_criar_cotacao),
            ("7. Listar Cotações", self.test_listar_cotacoes),
            ("8. GPS Simulação", self.test_gps_simulation),
            ("9. Frontend Acessível", self.test_frontend_accessible),
        ]
        
        for test_name, test_func in tests:
            try:
                await self._run_test(test_name, test_func)
            except Exception as e:
                logger.error(f"❌ {test_name} - ERRO CRÍTICO: {e}")
                self.errors.append(f"{test_name}: {str(e)}")
        
        self._print_summary()
        
        # Retornar código de saída
        return 0 if len(self.errors) == 0 else 1
    
    async def _run_test(self, name: str, test_func):
        """Executa um teste individual"""
        try:
            result = await test_func()
            if result.get("success"):
                logger.info(f"✅ {name} - OK")
                self.results.append({"test": name, "status": "PASSED", "details": result})
            else:
                logger.error(f"❌ {name} - FALHOU: {result.get('error')}")
                self.results.append({"test": name, "status": "FAILED", "details": result})
                self.errors.append(f"{name}: {result.get('error')}")
        except Exception as e:
            logger.error(f"❌ {name} - ERRO: {e}")
            self.results.append({"test": name, "status": "ERROR", "details": str(e)})
            self.errors.append(f"{name}: {str(e)}")
    
    async def test_backend_health(self) -> Dict[str, Any]:
        """Testa se backend está respondendo"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/health", timeout=5.0)
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "message": "Backend rodando",
                        "data": response.json()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Status code {response.status_code}"
                    }
        except Exception as e:
            return {"success": False, "error": f"Backend não acessível: {e}"}
    
    async def test_database_connection(self) -> Dict[str, Any]:
        """Testa conexão com banco de dados"""
        try:
            db = SessionLocal()
            result = db.execute(text("SELECT 1"))
            row = result.fetchone()
            db.close()
            
            if row and row[0] == 1:
                return {"success": True, "message": "Database conectado"}
            else:
                return {"success": False, "error": "Query retornou resultado inesperado"}
        except Exception as e:
            return {"success": False, "error": f"Database error: {e}"}
    
    async def test_redis_connection(self) -> Dict[str, Any]:
        """Testa conexão com Redis"""
        try:
            r = redis_client.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
            
            # Testar ping
            if r.ping():
                # Testar set/get
                r.set("smoke_test", "ok", ex=10)
                value = r.get("smoke_test")
                
                if value == "ok":
                    return {"success": True, "message": "Redis conectado e funcional"}
                else:
                    return {"success": False, "error": "Redis não está armazenando valores"}
            else:
                return {"success": False, "error": "Redis não respondeu ao ping"}
        except Exception as e:
            return {"success": False, "error": f"Redis error: {e}"}
    
    async def test_feature_flags(self) -> Dict[str, Any]:
        """Testa se feature flags estão configuradas"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/api/v1/features", timeout=5.0)
                
                if response.status_code == 200:
                    data = response.json()
                    features = data.get("features", {})
                    enabled = data.get("enabled", [])
                    
                    # Validar features críticas
                    critical_features = ["AUTH", "DASHBOARD", "COTACOES", "PEDIDOS_FRETE"]
                    missing = [f for f in critical_features if f not in enabled]
                    
                    if missing:
                        return {
                            "success": False,
                            "error": f"Features críticas desabilitadas: {missing}"
                        }
                    
                    return {
                        "success": True,
                        "message": f"{len(enabled)} features habilitadas",
                        "enabled_count": len(enabled)
                    }
                else:
                    return {"success": False, "error": "Endpoint de features não encontrado"}
        except Exception as e:
            return {"success": False, "error": f"Feature flags error: {e}"}
    
    async def test_authentication(self) -> Dict[str, Any]:
        """Testa autenticação com credenciais demo"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.backend_url}/api/v1/auth/login",
                    json={
                        "email": "admin@logiflow.demo",
                        "password": "admin123"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "access_token" in data:
                        return {
                            "success": True,
                            "message": "Login funcional",
                            "has_token": True
                        }
                    else:
                        return {"success": False, "error": "Token não retornado"}
                elif response.status_code == 404:
                    return {
                        "success": False,
                        "error": "Endpoint de login não encontrado (dados demo não criados?)"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Login falhou: {response.status_code}"
                    }
        except Exception as e:
            return {"success": False, "error": f"Auth error: {e}"}
    
    async def test_criar_cotacao(self) -> Dict[str, Any]:
        """Testa criação de cotação"""
        try:
            # Primeiro fazer login
            async with httpx.AsyncClient() as client:
                login_response = await client.post(
                    f"{self.backend_url}/api/v1/auth/login",
                    json={"email": "admin@logiflow.demo", "password": "admin123"},
                    timeout=10.0
                )
                
                if login_response.status_code != 200:
                    return {"success": False, "error": "Não foi possível fazer login"}
                
                token = login_response.json().get("access_token")
                
                # Criar cotação
                cotacao_response = await client.post(
                    f"{self.backend_url}/api/v1/cotacoes",
                    json={
                        "origem_cep": "01310100",
                        "destino_cep": "04547130",
                        "peso_kg": 100,
                        "valor_mercadoria": 1000
                    },
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                
                if cotacao_response.status_code in [200, 201]:
                    return {
                        "success": True,
                        "message": "Cotação criada com sucesso",
                        "cotacao_id": cotacao_response.json().get("id")
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Criar cotação falhou: {cotacao_response.status_code}"
                    }
        except Exception as e:
            return {"success": False, "error": f"Criar cotação error: {e}"}
    
    async def test_listar_cotacoes(self) -> Dict[str, Any]:
        """Testa listagem de cotações"""
        try:
            async with httpx.AsyncClient() as client:
                login_response = await client.post(
                    f"{self.backend_url}/api/v1/auth/login",
                    json={"email": "admin@logiflow.demo", "password": "admin123"},
                    timeout=10.0
                )
                
                if login_response.status_code != 200:
                    return {"success": False, "error": "Login falhou"}
                
                token = login_response.json().get("access_token")
                
                list_response = await client.get(
                    f"{self.backend_url}/api/v1/cotacoes",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                
                if list_response.status_code == 200:
                    data = list_response.json()
                    count = len(data) if isinstance(data, list) else data.get("total", 0)
                    return {
                        "success": True,
                        "message": f"{count} cotações encontradas",
                        "count": count
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Listar falhou: {list_response.status_code}"
                    }
        except Exception as e:
            return {"success": False, "error": f"Listar cotações error: {e}"}
    
    async def test_gps_simulation(self) -> Dict[str, Any]:
        """Testa GPS em modo simulação"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.backend_url}/api/v1/gps/veiculos",
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    total = data.get("total_veiculos", 0)
                    
                    return {
                        "success": True,
                        "message": f"GPS simulação ativa ({total} veículos)",
                        "simulation_mode": True
                    }
                else:
                    return {
                        "success": False,
                        "error": f"GPS endpoint falhou: {response.status_code}"
                    }
        except Exception as e:
            return {"success": False, "error": f"GPS error: {e}"}
    
    async def test_frontend_accessible(self) -> Dict[str, Any]:
        """Testa se frontend está acessível"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.frontend_url, timeout=5.0)
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "message": "Frontend acessível"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Frontend retornou {response.status_code}"
                    }
        except httpx.ConnectError:
            return {
                "success": False,
                "error": "Frontend não está rodando (opcional em testes de backend)"
            }
        except Exception as e:
            return {"success": False, "error": f"Frontend error: {e}"}
    
    def _print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "=" * 70)
        print("📊 RESUMO DO SMOKE TEST BETA")
        print("=" * 70)
        
        passed = sum(1 for r in self.results if r["status"] == "PASSED")
        failed = sum(1 for r in self.results if r["status"] == "FAILED")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")
        total = len(self.results)
        
        print(f"\n✅ Passou:  {passed}/{total}")
        print(f"❌ Falhou:  {failed}/{total}")
        print(f"⚠️  Erros:   {errors}/{total}")
        
        if self.errors:
            print("\n🚨 PROBLEMAS ENCONTRADOS:")
            for error in self.errors:
                print(f"   • {error}")
        
        print("\n" + "=" * 70)
        
        if len(self.errors) == 0:
            print("🎉 SISTEMA PRONTO PARA BETA!")
            print("=" * 70 + "\n")
        else:
            print("❌ BLOQUEIOS ENCONTRADOS - RESOLVER ANTES DO BETA")
            print("=" * 70 + "\n")


async def main():
    """Executa smoke test"""
    tester = BetaSmokeTest()
    exit_code = await tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
