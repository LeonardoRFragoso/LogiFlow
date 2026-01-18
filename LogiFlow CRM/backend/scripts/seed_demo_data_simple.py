"""
LogiFlow CRM - Seed Simplificado para BETA
==========================================
Cria apenas dados essenciais sem multi-tenancy complexo
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Cliente, Motorista, Veiculo, Cotacao, Pedido
from datetime import datetime, timedelta
from loguru import logger

# Hash de senha "admin123"
ADMIN_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGq0hm7I2"


def seed_demo_data():
    """Cria dados demo simples"""
    logger.info("🌱 Iniciando seed de dados demo BETA...")
    
    db = SessionLocal()
    
    try:
        # 1. Usuário Admin
        admin = db.query(User).filter_by(email="admin@logiflow.demo").first()
        if not admin:
            admin = User(
                email="admin@logiflow.demo",
                senha_hash=ADMIN_HASH,
                nome="Admin Demo",
                tipo="admin",
                status="ativo"
            )
            db.add(admin)
            logger.info("✅ Admin criado: admin@logiflow.demo / admin123")
        
        # 2. Cliente Demo
        cliente = db.query(Cliente).filter_by(cnpj="11.222.333/0001-44").first()
        if not cliente:
            cliente = Cliente(
                razao_social="Empresa Alpha Ltda",
                nome_fantasia="Alpha",
                cnpj="11.222.333/0001-44",
                email="contato@alpha.com.br",
                telefone="(11) 3333-4444",
                cidade="São Paulo",
                uf="SP",
                ativo=True
            )
            db.add(cliente)
            logger.info("✅ Cliente criado: Empresa Alpha")
        
        # 3. Motorista Demo
        motorista = db.query(Motorista).filter_by(cpf="111.222.333-44").first()
        if not motorista:
            motorista = Motorista(
                nome="João Silva",
                cpf="111.222.333-44",
                telefone="(11) 98888-7777",
                email="joao@logiflow.demo",
                cnh_numero="12345678901",
                cnh_categoria="D",
                status="disponivel",
                ativo=True
            )
            db.add(motorista)
            logger.info("✅ Motorista criado: João Silva")
        
        # 4. Veículo Demo
        veiculo = db.query(Veiculo).filter_by(placa="ABC-1234").first()
        if not veiculo:
            veiculo = Veiculo(
                placa="ABC-1234",
                tipo="Caminhão",
                marca="Mercedes",
                modelo="Actros",
                ano=2022,
                capacidade_kg=15000,
                status="disponivel",
                ativo=True
            )
            db.add(veiculo)
            logger.info("✅ Veículo criado: ABC-1234")
        
        db.commit()
        
        # 5. Cotação Demo (após commit para ter IDs)
        cotacao = db.query(Cotacao).filter_by(numero="COT-2024-001").first()
        if not cotacao:
            cotacao = Cotacao(
                numero="COT-2024-001",
                cliente_id=cliente.id,
                origem_cidade="São Paulo",
                origem_uf="SP",
                destino_cidade="Rio de Janeiro",
                destino_uf="RJ",
                peso_kg=500,
                valor_mercadoria=10000,
                valor_frete=350,
                status="aprovada"
            )
            db.add(cotacao)
            logger.info("✅ Cotação criada: COT-2024-001")
        
        # 6. Pedido Demo
        pedido = db.query(Pedido).filter_by(numero="PED-2024-001").first()
        if not pedido:
            pedido = Pedido(
                numero="PED-2024-001",
                cliente_id=cliente.id,
                motorista_id=motorista.id,
                origem_cidade="São Paulo",
                origem_uf="SP",
                destino_cidade="Rio de Janeiro",
                destino_uf="RJ",
                destino_cep="20000-000",
                status="em_transito"
            )
            db.add(pedido)
            logger.info("✅ Pedido criado: PED-2024-001")
        
        db.commit()
        
        print("\n" + "="*60)
        print("🎉 DADOS DEMO CRIADOS COM SUCESSO!")
        print("="*60)
        print("\n📋 CREDENCIAIS:")
        print("   Email:    admin@logiflow.demo")
        print("   Senha:    admin123")
        print("\n🌐 ACESSO:")
        print("   Backend:  http://localhost:8000/api/v1/docs")
        print("   Frontend: http://localhost:3001")
        print("\n" + "="*60 + "\n")
        
        logger.info("✅ Seed concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro no seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Criar tabelas se não existem
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
