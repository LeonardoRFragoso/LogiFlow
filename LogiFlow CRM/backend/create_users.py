"""
Script para criar usuários no banco de dados Railway
Executa diretamente no banco sem depender do startup da aplicação
"""
import os
import sys
import bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def hash_senha(senha: str) -> str:
    """Hash de senha usando bcrypt"""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def criar_usuarios():
    """Cria usuários admin e Leonardo no banco de dados"""
    
    # Obter URL do banco de dados
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não definida")
        return False
    
    try:
        # connect_timeout=5 evita bloquear o startup por minutos se o DB estiver indisponível
        engine = create_engine(database_url, connect_args={"connect_timeout": 5})
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("🔧 Conectado ao banco de dados...")
        
        # Lista de usuários a criar
        usuarios = [
            {
                'email': 'admin@logiflow.com',
                'nome': 'Administrador',
                'senha': 'admin123',
                'tipo': 'admin',
                'status': 'ativo'
            },
            {
                'email': 'leonardorfragoso@gmail.com',
                'nome': 'Leonardo Fragoso',
                'senha': 'Senha123!',
                'tipo': 'admin',
                'status': 'ativo'
            }
        ]
        
        for usuario in usuarios:
            # Verificar se usuário já existe
            result = session.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {'email': usuario['email']}
            )
            
            if result.fetchone():
                print(f"ℹ️  Usuário {usuario['email']} já existe")
                continue
            
            # Hash da senha
            senha_hash = hash_senha(usuario['senha'])
            
            # Inserir usuário
            session.execute(
                text("""
                    INSERT INTO users (email, nome, senha_hash, tipo, status, created_at, updated_at)
                    VALUES (:email, :nome, :senha_hash, :tipo, :status, NOW(), NOW())
                """),
                {
                    'email': usuario['email'],
                    'nome': usuario['nome'],
                    'senha_hash': senha_hash,
                    'tipo': usuario['tipo'],
                    'status': usuario['status']
                }
            )
            
            session.commit()
            print(f"✅ Usuário {usuario['email']} criado com sucesso!")
            print(f"   Senha: {usuario['senha']}")
        
        session.close()
        print("\n✅ Todos os usuários foram criados com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Criando usuários no banco de dados...")
    print("=" * 60)
    
    sucesso = criar_usuarios()
    
    print("=" * 60)
    
    if sucesso:
        print("\n📋 CREDENCIAIS DE ACESSO:")
        print("-" * 60)
        print("👤 Admin:")
        print("   Email: admin@logiflow.com")
        print("   Senha: admin123")
        print()
        print("👤 Leonardo Fragoso:")
        print("   Email: leonardorfragoso@gmail.com")
        print("   Senha: Senha123!")
        print("-" * 60)
        print("\n🌐 URL de acesso: https://logi-flow-blush.vercel.app/login")
        sys.exit(0)
    else:
        sys.exit(1)
