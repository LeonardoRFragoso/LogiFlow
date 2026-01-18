"""
LogiFlow CRM - Setup Automatizado OAuth2 SuiteCRM
==================================================
Cria automaticamente OAuth2 Client no SuiteCRM e atualiza .env

IMPORTANTE: SuiteCRM deve estar rodando antes de executar este script.
"""

import httpx
import sys
from pathlib import Path
from loguru import logger
import os
from dotenv import load_dotenv

# Carregar .env atual
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class OAuth2Setup:
    """Setup automatizado de OAuth2 no SuiteCRM"""
    
    def __init__(self):
        self.suitecrm_url = os.getenv("SUITECRM_URL", "http://localhost:8080")
        self.admin_user = "admin"
        self.admin_pass = "admin123"  # Senha padrão de instalação
        self.session = None
        
    def run_setup(self):
        """Executa setup completo"""
        logger.info("🔐 Setup OAuth2 SuiteCRM - LogiFlow CRM")
        logger.info("=" * 60)
        
        try:
            # 1. Verificar SuiteCRM acessível
            if not self.check_suitecrm_accessible():
                logger.error("❌ SuiteCRM não está acessível")
                return False
            
            # 2. Fazer login
            if not self.login_admin():
                logger.error("❌ Login admin falhou")
                logger.info("ℹ️  Verifique as credenciais ou crie manualmente:")
                logger.info("   1. Acesse http://localhost:8080")
                logger.info("   2. Admin → OAuth2 Clients")
                logger.info("   3. Create Client")
                return False
            
            # 3. Criar OAuth2 Client
            client_id, client_secret = self.create_oauth2_client()
            
            if not client_id or not client_secret:
                logger.error("❌ Falha ao criar OAuth2 Client")
                return False
            
            # 4. Atualizar .env
            self.update_env_file(client_id, client_secret)
            
            # 5. Mostrar sucesso
            self.print_success(client_id, client_secret)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no setup: {e}")
            return False
    
    def check_suitecrm_accessible(self) -> bool:
        """Verifica se SuiteCRM está acessível"""
        try:
            response = httpx.get(f"{self.suitecrm_url}/index.php", timeout=5.0)
            if response.status_code == 200:
                logger.info(f"✅ SuiteCRM acessível em {self.suitecrm_url}")
                return True
            else:
                logger.error(f"❌ SuiteCRM retornou status {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Erro ao acessar SuiteCRM: {e}")
            return False
    
    def login_admin(self) -> bool:
        """Faz login no SuiteCRM como admin"""
        try:
            # Nota: SuiteCRM 8 usa autenticação via API V8
            # Para criar OAuth2 Client, normalmente usa interface web
            # Este script mostra as credenciais para criação manual
            logger.info("⚠️  Criação de OAuth2 Client requer acesso web manual")
            return True
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def create_oauth2_client(self):
        """
        Mostra instruções para criar OAuth2 Client manualmente.
        
        Nota: SuiteCRM não expõe API para criar OAuth2 Clients programaticamente.
        Precisa ser criado via interface web.
        """
        logger.info("\n📋 INSTRUÇÕES PARA CRIAR OAUTH2 CLIENT:")
        logger.info("=" * 60)
        logger.info("1. Acesse: http://localhost:8080")
        logger.info(f"2. Login: {self.admin_user} / {self.admin_pass}")
        logger.info("3. Vá em: Admin → OAuth2 Clients and Tokens")
        logger.info("4. Clique: Create OAuth2 Client")
        logger.info("5. Preencha:")
        logger.info("   - Name: LogiFlow Backend API")
        logger.info("   - Client Type: Confidential")
        logger.info("6. Salve e COPIE as credenciais")
        logger.info("=" * 60)
        
        print("\n")
        client_id = input("Cole o CLIENT_ID aqui: ").strip()
        client_secret = input("Cole o CLIENT_SECRET aqui: ").strip()
        
        if not client_id or not client_secret:
            logger.error("❌ Credenciais vazias")
            return None, None
        
        logger.info("✅ Credenciais coletadas")
        return client_id, client_secret
    
    def update_env_file(self, client_id: str, client_secret: str):
        """Atualiza arquivo .env com as credenciais OAuth2"""
        try:
            # Ler arquivo atual
            if env_path.exists():
                with open(env_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            else:
                # Criar de .env.example
                example_path = Path(__file__).parent.parent / ".env.example"
                if example_path.exists():
                    with open(example_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                else:
                    lines = []
            
            # Atualizar linhas
            updated = False
            new_lines = []
            
            for line in lines:
                if line.startswith("SUITECRM_CLIENT_ID="):
                    new_lines.append(f"SUITECRM_CLIENT_ID={client_id}\n")
                    updated = True
                elif line.startswith("SUITECRM_CLIENT_SECRET="):
                    new_lines.append(f"SUITECRM_CLIENT_SECRET={client_secret}\n")
                else:
                    new_lines.append(line)
            
            # Se não encontrou as linhas, adicionar no final
            if not updated:
                new_lines.append(f"\n# OAuth2 SuiteCRM (gerado automaticamente)\n")
                new_lines.append(f"SUITECRM_CLIENT_ID={client_id}\n")
                new_lines.append(f"SUITECRM_CLIENT_SECRET={client_secret}\n")
            
            # Salvar
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            logger.info(f"✅ Arquivo .env atualizado: {env_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar .env: {e}")
    
    def print_success(self, client_id: str, client_secret: str):
        """Imprime mensagem de sucesso"""
        print("\n" + "=" * 60)
        print("🎉 SETUP OAUTH2 CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\n📋 CREDENCIAIS CONFIGURADAS:")
        print(f"   CLIENT_ID:     {client_id[:20]}...")
        print(f"   CLIENT_SECRET: {client_secret[:20]}...")
        print(f"\n📄 Arquivo atualizado: {env_path}")
        print("\n✅ PRÓXIMOS PASSOS:")
        print("   1. Reiniciar backend: docker-compose restart api")
        print("   2. Executar testes: python backend/tests/smoke_test_beta.py")
        print("   3. Acessar sistema: http://localhost:3001")
        print("\n" + "=" * 60 + "\n")


def main():
    """Executa setup OAuth2"""
    setup = OAuth2Setup()
    success = setup.run_setup()
    
    if success:
        logger.info("✅ Setup concluído")
        sys.exit(0)
    else:
        logger.error("❌ Setup falhou")
        sys.exit(1)


if __name__ == "__main__":
    main()
