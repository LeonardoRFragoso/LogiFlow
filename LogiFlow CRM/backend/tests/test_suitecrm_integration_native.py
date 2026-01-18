"""
LogiFlow CRM - Testes de Integração com SuiteCRM (Módulos Nativos)
Execute após configurar OAuth2 no .env
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.suitecrm_service import suitecrm_service
from loguru import logger
import json

logger.remove()
logger.add(sys.stdout, level="INFO")


class TesteSuiteCRMIntegration:
    """Suite de testes para integração com SuiteCRM usando módulos nativos"""
    
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
    
    async def teste_03_listar_contacts(self):
        """Teste 3: Listar Contacts"""
        try:
            resultado = await suitecrm_service.get_module_records("Contacts", page_size=10)
            contacts = resultado.get("data", [])
            
            self.registrar_resultado(
                "Teste 03 - Listar Contacts",
                True,
                f"Encontrados {len(contacts)} contacts",
                {"total": len(contacts)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 03 - Listar Contacts",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_04_listar_leads(self):
        """Teste 4: Listar Leads"""
        try:
            resultado = await suitecrm_service.get_module_records("Leads", page_size=10)
            leads = resultado.get("data", [])
            
            self.registrar_resultado(
                "Teste 04 - Listar Leads",
                True,
                f"Encontrados {len(leads)} leads",
                {"total": len(leads)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 04 - Listar Leads",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_05_listar_opportunities(self):
        """Teste 5: Listar Opportunities"""
        try:
            resultado = await suitecrm_service.get_module_records("Opportunities", page_size=10)
            opportunities = resultado.get("data", [])
            
            self.registrar_resultado(
                "Teste 05 - Listar Opportunities",
                True,
                f"Encontradas {len(opportunities)} opportunities",
                {"total": len(opportunities)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 05 - Listar Opportunities",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_06_listar_cases(self):
        """Teste 6: Listar Cases"""
        try:
            resultado = await suitecrm_service.get_module_records("Cases", page_size=10)
            cases = resultado.get("data", [])
            
            self.registrar_resultado(
                "Teste 06 - Listar Cases",
                True,
                f"Encontrados {len(cases)} cases",
                {"total": len(cases)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 06 - Listar Cases",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_07_listar_notes(self):
        """Teste 7: Listar Notes"""
        try:
            resultado = await suitecrm_service.get_module_records("Notes", page_size=10)
            notes = resultado.get("data", [])
            
            self.registrar_resultado(
                "Teste 07 - Listar Notes",
                True,
                f"Encontradas {len(notes)} notes",
                {"total": len(notes)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 07 - Listar Notes",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_08_listar_users(self):
        """Teste 8: Listar Users"""
        try:
            resultado = await suitecrm_service.get_module_records("Users", page_size=10)
            users = resultado.get("data", [])
            
            self.registrar_resultado(
                "Teste 08 - Listar Users",
                True,
                f"Encontrados {len(users)} users",
                {"total": len(users)}
            )
        except Exception as e:
            self.registrar_resultado(
                "Teste 08 - Listar Users",
                False,
                f"Erro: {str(e)}"
            )
    
    async def teste_09_criar_account(self):
        """Teste 9: Criar Account"""
        try:
            dados = {
                "name": "Empresa Teste LogiFlow",
                "billing_address_city": "São Paulo",
                "billing_address_state": "SP"
            }
            
            resultado = await suitecrm_service.create_module_record("Accounts", dados)
            
            if resultado.get("data"):
                account_id = resultado["data"].get("id")
                self.registrar_resultado(
                    "Teste 09 - Criar Account",
                    True,
                    f"Account criado com ID: {account_id}",
                    {"id": account_id}
                )
                return account_id
            else:
                self.registrar_resultado(
                    "Teste 09 - Criar Account",
                    False,
                    "Nenhum dado retornado"
                )
                return None
        except Exception as e:
            self.registrar_resultado(
                "Teste 09 - Criar Account",
                False,
                f"Erro: {str(e)}"
            )
            return None
    
    async def teste_10_criar_contact(self):
        """Teste 10: Criar Contact"""
        try:
            dados = {
                "first_name": "João",
                "last_name": "Silva Teste",
                "email1": "joao.teste@logiflow.com"
            }
            
            resultado = await suitecrm_service.create_module_record("Contacts", dados)
            
            if resultado.get("data"):
                contact_id = resultado["data"].get("id")
                self.registrar_resultado(
                    "Teste 10 - Criar Contact",
                    True,
                    f"Contact criado com ID: {contact_id}",
                    {"id": contact_id}
                )
                return contact_id
            else:
                self.registrar_resultado(
                    "Teste 10 - Criar Contact",
                    False,
                    "Nenhum dado retornado"
                )
                return None
        except Exception as e:
            self.registrar_resultado(
                "Teste 10 - Criar Contact",
                False,
                f"Erro: {str(e)}"
            )
            return None
    
    async def teste_11_criar_lead(self):
        """Teste 11: Criar Lead"""
        try:
            dados = {
                "first_name": "Maria",
                "last_name": "Santos Lead",
                "status": "New",
                "email1": "maria.lead@logiflow.com"
            }
            
            resultado = await suitecrm_service.create_module_record("Leads", dados)
            
            if resultado.get("data"):
                lead_id = resultado["data"].get("id")
                self.registrar_resultado(
                    "Teste 11 - Criar Lead",
                    True,
                    f"Lead criado com ID: {lead_id}",
                    {"id": lead_id}
                )
                return lead_id
            else:
                self.registrar_resultado(
                    "Teste 11 - Criar Lead",
                    False,
                    "Nenhum dado retornado"
                )
                return None
        except Exception as e:
            self.registrar_resultado(
                "Teste 11 - Criar Lead",
                False,
                f"Erro: {str(e)}"
            )
            return None
    
    async def teste_12_criar_opportunity(self):
        """Teste 12: Criar Opportunity"""
        try:
            dados = {
                "name": "Oportunidade Teste LogiFlow",
                "amount": "50000.00",
                "sales_stage": "Prospecting"
            }
            
            resultado = await suitecrm_service.create_module_record("Opportunities", dados)
            
            if resultado.get("data"):
                opp_id = resultado["data"].get("id")
                self.registrar_resultado(
                    "Teste 12 - Criar Opportunity",
                    True,
                    f"Opportunity criada com ID: {opp_id}",
                    {"id": opp_id}
                )
                return opp_id
            else:
                self.registrar_resultado(
                    "Teste 12 - Criar Opportunity",
                    False,
                    "Nenhum dado retornado"
                )
                return None
        except Exception as e:
            self.registrar_resultado(
                "Teste 12 - Criar Opportunity",
                False,
                f"Erro: {str(e)}"
            )
            return None
    
    async def teste_13_criar_note(self):
        """Teste 13: Criar Note"""
        try:
            dados = {
                "name": "Nota Teste Integração",
                "description": "Esta é uma nota de teste criada pela integração LogiFlow + SuiteCRM"
            }
            
            resultado = await suitecrm_service.create_module_record("Notes", dados)
            
            if resultado.get("data"):
                note_id = resultado["data"].get("id")
                self.registrar_resultado(
                    "Teste 13 - Criar Note",
                    True,
                    f"Note criada com ID: {note_id}",
                    {"id": note_id}
                )
                return note_id
            else:
                self.registrar_resultado(
                    "Teste 13 - Criar Note",
                    False,
                    "Nenhum dado retornado"
                )
                return None
        except Exception as e:
            self.registrar_resultado(
                "Teste 13 - Criar Note",
                False,
                f"Erro: {str(e)}"
            )
            return None
    
    async def executar_todos_testes(self):
        """Executa toda a suite de testes"""
        logger.info("=" * 80)
        logger.info("🧪 INICIANDO TESTES DE INTEGRAÇÃO SUITECRM - MÓDULOS NATIVOS")
        logger.info("=" * 80)
        
        # Teste de conexão
        await self.teste_01_conexao()
        
        # Testes de listagem
        await self.teste_02_listar_accounts()
        await self.teste_03_listar_contacts()
        await self.teste_04_listar_leads()
        await self.teste_05_listar_opportunities()
        await self.teste_06_listar_cases()
        await self.teste_07_listar_notes()
        await self.teste_08_listar_users()
        
        # Testes de criação
        await self.teste_09_criar_account()
        await self.teste_10_criar_contact()
        await self.teste_11_criar_lead()
        await self.teste_12_criar_opportunity()
        await self.teste_13_criar_note()
        
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
        with open("test_results_native.json", "w", encoding="utf-8") as f:
            json.dump({
                "total": total_testes,
                "sucessos": self.sucesso_total,
                "falhas": self.falha_total,
                "percentual": percentual,
                "testes": self.resultados
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n📄 Relatório detalhado salvo em: test_results_native.json")


async def main():
    """Função principal"""
    logger.info("LogiFlow CRM - Teste de Integração SuiteCRM (Módulos Nativos)\n")
    
    from config import settings
    
    if not settings.SUITECRM_CLIENT_ID or not settings.SUITECRM_CLIENT_SECRET:
        logger.error("❌ ERRO: Credenciais OAuth2 não configuradas!")
        return
    
    logger.success(f"✅ Credenciais OAuth2 configuradas")
    logger.info(f"📍 URL SuiteCRM: {settings.SUITECRM_URL}\n")
    
    tester = TesteSuiteCRMIntegration()
    await tester.executar_todos_testes()


if __name__ == "__main__":
    asyncio.run(main())
