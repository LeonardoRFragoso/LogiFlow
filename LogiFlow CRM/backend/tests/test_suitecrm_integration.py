"""
LogiFlow CRM - Testes de Integração com SuiteCRM
Execute após configurar OAuth2 no .env
"""

import asyncio
import sys
from pathlib import Path

# Adicionar path do backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.suitecrm_service import suitecrm_service
from loguru import logger
import json

# Configurar logger
logger.remove()
logger.add(sys.stdout, level="INFO")


class TesteSuiteCRMIntegration:
    """Suite de testes para integração com SuiteCRM"""
    
    def __init__(self):
        self.resultados = []
        self.sucesso_total = 0
        self.falha_total = 0
    
    def registrar_resultado(self, nome_teste: str, sucesso: bool, mensagem: str = "", dados: dict = None):
        """Registra resultado de um teste"""
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        self.resultados.append({
            "teste": nome_teste,
            "status": status,
            "sucesso": sucesso,
            "mensagem": mensagem,
            "dados": dados
        })
        
        if sucesso:
            self.sucesso_total += 1
            logger.success(f"{status} | {nome_teste} - {mensagem}")
        else:
            self.falha_total += 1
            logger.error(f"{status} | {nome_teste} - {mensagem}")
    
    async def teste_01_conexao(self):
        """Teste 1: Verificar conexão com SuiteCRM"""
        try:
            resultado = await suitecrm_service.test_connection()
            
            if resultado.get("success"):
                self.registrar_resultado(
                    "Teste 01 - Conexão",
                    True,
                    f"Conectado em {resultado.get('base_url')}",
                    resultado
                )
            else:
                self.registrar_resultado(
                    "Teste 01 - Conexão",
                    False,
                    resultado.get("message", "Erro desconhecido"),
                    resultado
                )
        except Exception as e:
            self.registrar_resultado(
                "Teste 01 - Conexão",
                False,
                f"Exceção: {str(e)}"
            )
    
    async def teste_02_listar_accounts(self):
        """Teste 2: Listar Accounts"""
        try:
            resultado = await suitecrm_service.get_module_records("Accounts", page_size=10)
            accounts = resultado.get("data", [])
            
            self.registrar_resultado(
                "Teste 02 - Listar Accounts",
                True,
                f"Encontrados {len(accounts)} accounts",
                {"total": len(accounts)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 02 - Listar Accounts",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_03_criar_contact(self):
        """Teste 3: Criar Contact de teste"""
        try:
            dados_contact = {
                "first_name": "João",
                "last_name": "Silva Teste",
                "email1": "joao.teste@logiflow.com"
            }
            
            resultado = await suitecrm_service.create_module_record("Contacts", dados_contact)
            
            if resultado.get("data"):
                contact_id = resultado["data"].get("id")
                self.registrar_resultado(
                    "Teste 03 - Criar Contact",
                    True,
                    f"Contact criado com ID: {contact_id}",
                    {"id": contact_id}
                )
                return contact_id
            else:
                self.registrar_resultado(
                    "Teste 03 - Criar Contact",
                    False,
                    "Nenhum dado retornado"
                )
                return None
        except Exception as e:
            self.registrar_resultado(
                "Teste 03 - Criar Contact",
                False,
                f"Erro: {str(e)}"
            )
            return None
    
    async def teste_04_listar_pedidos(self):
        """Teste 4: Listar pedidos"""
        try:
            pedidos = await suitecrm_service.get_pedidos()
            
            self.registrar_resultado(
                "Teste 04 - Listar Pedidos",
                True,
                f"Encontrados {len(pedidos)} pedidos",
                {"total": len(pedidos)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 04 - Listar Pedidos",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_05_listar_motoristas(self):
        """Teste 5: Listar motoristas"""
        try:
            motoristas = await suitecrm_service.get_motoristas()
            
            self.registrar_resultado(
                "Teste 05 - Listar Motoristas",
                True,
                f"Encontrados {len(motoristas)} motoristas",
                {"total": len(motoristas)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 05 - Listar Motoristas",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_06_listar_veiculos(self):
        """Teste 6: Listar veículos"""
        try:
            veiculos = await suitecrm_service.get_veiculos()
            
            self.registrar_resultado(
                "Teste 06 - Listar Veiculos",
                True,
                f"Encontrados {len(veiculos)} veículos",
                {"total": len(veiculos)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 06 - Listar Veiculos",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_07_listar_entregas(self):
        """Teste 7: Listar entregas"""
        try:
            entregas = await suitecrm_service.get_entregas()
            
            self.registrar_resultado(
                "Teste 07 - Listar Entregas",
                True,
                f"Encontradas {len(entregas)} entregas",
                {"total": len(entregas)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 07 - Listar Entregas",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_08_modulos_genericos(self):
        """Teste 8: Listar módulos via método genérico"""
        # Usar módulos nativos do SuiteCRM que existem
        modulos = ["Accounts", "Contacts", "Leads", "Opportunities", "Cases", "Notes"]
        
        for modulo in modulos:
            try:
                resultado = await suitecrm_service.get_module_records(modulo, page_size=5)
                total = len(resultado.get("data", []))
                
                self.registrar_resultado(
                    f"Teste 08.{modulo} - Acesso Genérico",
                    True,
                    f"{total} registros",
                    {"modulo": modulo, "total": total}
                )
            except Exception as e:
                self.registrar_resultado(
                    f"Teste 08.{modulo} - Acesso Genérico",
                    False,
                    f"Erro: {str(e)}"
                )
    
    async def executar_todos_testes(self):
        """Executa toda a suite de testes"""
        logger.info("=" * 80)
        logger.info("🧪 INICIANDO TESTES DE INTEGRAÇÃO SUITECRM")
        logger.info("=" * 80)
        
        # Testes de conexão
        await self.teste_01_conexao()
        
        # Testes de listagem
        await self.teste_02_listar_accounts()
        await self.teste_04_listar_contacts()
        await self.teste_05_listar_leads()
        await self.teste_06_listar_opportunities()
        await self.teste_07_listar_cases()
        
        # Teste de criação
        await self.teste_03_criar_contact()
        
        # Testes genéricos
        await self.teste_08_modulos_genericos()
        
        # Relatório final
        self.gerar_relatorio()
    
    def gerar_relatorio(self):
        """Gera relatório final dos testes"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 RELATÓRIO FINAL DE TESTES")
        logger.info("=" * 80)
        
        total_testes = self.sucesso_total + self.falha_total
        percentual = (self.sucesso_total / total_testes * 100) if total_testes > 0 else 0
        
        logger.info(f"Total de Testes: {total_testes}")
        logger.info(f"✅ Sucessos: {self.sucesso_total}")
        logger.info(f"❌ Falhas: {self.falha_total}")
        logger.info(f"📈 Taxa de Sucesso: {percentual:.1f}%")
        logger.info("=" * 80)
        
        # Status final
        if self.falha_total == 0:
            logger.success("\n🎉 TODOS OS TESTES PASSARAM! Integração 100% funcional!")
        elif self.sucesso_total > 0:
            logger.warning(f"\n⚠️ Integração parcial: {self.falha_total} testes falharam")
            logger.info("\nTestes que falharam:")
            for resultado in self.resultados:
                if not resultado["sucesso"]:
                    logger.error(f"  - {resultado['teste']}: {resultado['mensagem']}")
        else:
            logger.error("\n❌ INTEGRAÇÃO NÃO FUNCIONAL - Verifique configurações OAuth2")
        
        # Salvar relatório JSON
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump({
                "total": total_testes,
                "sucessos": self.sucesso_total,
                "falhas": self.falha_total,
                "percentual": percentual,
                "testes": self.resultados
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n📄 Relatório detalhado salvo em: test_results.json")


async def main():
    """Função principal"""
    logger.info("LogiFlow CRM - Teste de Integração SuiteCRM\n")
    
    # Verificar configuração
    from config import settings
    
    if not settings.SUITECRM_CLIENT_ID or not settings.SUITECRM_CLIENT_SECRET:
        logger.error("❌ ERRO: Credenciais OAuth2 não configuradas!")
        logger.info("\nPara configurar:")
        logger.info("1. Acesse SuiteCRM Admin → OAuth2 Clients and Tokens")
        logger.info("2. Crie um novo OAuth2 Client")
        logger.info("3. Adicione as credenciais no arquivo .env:")
        logger.info("   SUITECRM_CLIENT_ID=seu_client_id")
        logger.info("   SUITECRM_CLIENT_SECRET=seu_client_secret")
        logger.info("4. Execute este teste novamente\n")
        return
    
    logger.success(f"✅ Credenciais OAuth2 configuradas")
    logger.info(f"📍 URL SuiteCRM: {settings.SUITECRM_URL}\n")
    
    # Executar testes
    tester = TesteSuiteCRMIntegration()
    await tester.executar_todos_testes()


if __name__ == "__main__":
    asyncio.run(main())
