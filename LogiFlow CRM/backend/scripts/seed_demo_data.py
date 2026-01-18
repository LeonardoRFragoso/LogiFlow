"""
LogiFlow CRM - Script de Dados Demo para BETA
==============================================
Cria dados iniciais para ambiente BETA (empresa, usuários, motoristas, etc).
NÃO EXECUTA em produção - apenas desenvolvimento/beta.
"""

import asyncio
import sys
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import (
    Tenant, User, Cliente, Motorista, Veiculo, 
    Cotacao, Pedido, Entrega, Ocorrencia
)
from datetime import datetime, timedelta
from loguru import logger

# Hash pré-gerado de "admin123" e "operador123" usando bcrypt
# Para evitar problemas de compatibilidade em runtime
ADMIN_PASSWORD_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGq0hm7I2"  # admin123
OPERADOR_PASSWORD_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGq0hm7I2"  # operador123


class DemoDataSeeder:
    """Cria dados demo para ambiente BETA"""
    
    def __init__(self, db: Session):
        self.db = db
        
    def seed_all(self):
        """Executa todos os seeders"""
        logger.info("🌱 Iniciando seed de dados demo...")
        
        try:
            # 1. Tenant Demo
            tenant = self.seed_tenant()
            
            # 2. Usuários
            admin = self.seed_admin_user(tenant)
            operador = self.seed_operador_user(tenant)
            
            # 3. Clientes
            clientes = self.seed_clientes(tenant)
            
            # 4. Motoristas
            motoristas = self.seed_motoristas(tenant)
            
            # 5. Veículos
            veiculos = self.seed_veiculos(tenant, motoristas)
            
            # 6. Cotação Demo
            cotacao = self.seed_cotacao_demo(tenant, clientes[0], admin)
            
            # 7. Pedido Demo
            pedido = self.seed_pedido_demo(tenant, cotacao, motoristas[0], veiculos[0])
            
            # 8. Entrega Demo
            entrega = self.seed_entrega_demo(tenant, pedido)
            
            # 9. Ocorrência Demo (opcional)
            # ocorrencia = self.seed_ocorrencia_demo(tenant, pedido)
            
            self.db.commit()
            
            logger.info("✅ Seed concluído com sucesso!")
            self.print_summary(admin, operador, motoristas)
            
        except Exception as e:
            logger.error(f"❌ Erro no seed: {e}")
            self.db.rollback()
            raise
    
    def seed_tenant(self) -> Tenant:
        """Cria empresa demo"""
        tenant = self.db.query(Tenant).filter_by(subdomain="demo-beta").first()
        
        if not tenant:
            tenant = Tenant(
                subdomain="demo-beta",
                company_name="LogiFlow Demo BETA",
                contact_name="Administrador Demo",
                contact_email="demo@logiflow.com.br",
                contact_phone="(11) 98765-4321",
                db_name="logiflow_demo_beta",
                db_user="demo_user",
                db_password="demo_pass_123",
                status="active",
                plan="professional",
                max_users=10,
                max_vehicles=20,
                max_orders_per_month=1000
            )
            self.db.add(tenant)
            self.db.flush()
            logger.info(f"✅ Tenant criado: {tenant.company_name}")
        else:
            logger.info(f"ℹ️ Tenant já existe: {tenant.company_name}")
        
        return tenant
    
    def seed_admin_user(self, tenant: Tenant) -> User:
        """Cria usuário admin demo"""
        admin = self.db.query(User).filter_by(email="admin@logiflow.demo").first()
        
        if not admin:
            admin = User(
                email="admin@logiflow.demo",
                senha_hash=ADMIN_PASSWORD_HASH,
                nome="Administrador Demo",
                tipo="admin",
                status="ativo"
            )
            self.db.add(admin)
            self.db.flush()
            logger.info(f"✅ Admin criado: {admin.email}")
        else:
            logger.info(f"ℹ️ Admin já existe: {admin.email}")
        
        return admin
    
    def seed_operador_user(self, tenant: Tenant) -> User:
        """Cria usuário operador demo"""
        operador = self.db.query(User).filter_by(email="operador@logiflow.demo").first()
        
        if not operador:
            operador = User(
                email="operador@logiflow.demo",
                senha_hash=OPERADOR_PASSWORD_HASH,
                nome="Operador Demo",
                tipo="operador",
                status="ativo"
            )
            self.db.add(operador)
            self.db.flush()
            logger.info(f"✅ Operador criado: {operador.email}")
        else:
            logger.info(f"ℹ️ Operador já existe: {operador.email}")
        
        return operador
    
    def seed_clientes(self, tenant: Tenant) -> list:
        """Cria clientes demo"""
        clientes_data = [
            {
                "nome": "Empresa Alpha Ltda",
                "cnpj": "11.222.333/0001-44",
                "email": "contato@alpha.com.br",
                "telefone": "(11) 3333-4444"
            },
            {
                "nome": "Beta Transportes S.A.",
                "cnpj": "22.333.444/0001-55",
                "email": "comercial@beta.com.br",
                "telefone": "(11) 4444-5555"
            },
            {
                "nome": "Gamma Logística",
                "cnpj": "33.444.555/0001-66",
                "email": "vendas@gamma.com.br",
                "telefone": "(11) 5555-6666"
            }
        ]
        
        clientes = []
        for data in clientes_data:
            cliente = self.db.query(Cliente).filter_by(
                tenant_id=tenant.id,
                cnpj=data["cnpj"]
            ).first()
            
            if not cliente:
                cliente = Cliente(
                    tenant_id=tenant.id,
                    nome=data["nome"],
                    cnpj=data["cnpj"],
                    email=data["email"],
                    telefone=data["telefone"],
                    is_active=True
                )
                self.db.add(cliente)
                self.db.flush()
                logger.info(f"✅ Cliente criado: {cliente.nome}")
            else:
                logger.info(f"ℹ️ Cliente já existe: {cliente.nome}")
            
            clientes.append(cliente)
        
        return clientes
    
    def seed_motoristas(self, tenant: Tenant) -> list:
        """Cria motoristas demo"""
        motoristas_data = [
            {
                "nome": "João da Silva",
                "cpf": "111.222.333-44",
                "cnh": "12345678901",
                "telefone": "(11) 98888-7777",
                "email": "joao.silva@logiflow.demo"
            },
            {
                "nome": "Pedro Santos",
                "cpf": "222.333.444-55",
                "cnh": "23456789012",
                "telefone": "(11) 97777-6666",
                "email": "pedro.santos@logiflow.demo"
            },
            {
                "nome": "Carlos Oliveira",
                "cpf": "333.444.555-66",
                "cnh": "34567890123",
                "telefone": "(11) 96666-5555",
                "email": "carlos.oliveira@logiflow.demo"
            }
        ]
        
        motoristas = []
        for data in motoristas_data:
            motorista = self.db.query(Motorista).filter_by(
                tenant_id=tenant.id,
                cpf=data["cpf"]
            ).first()
            
            if not motorista:
                motorista = Motorista(
                    tenant_id=tenant.id,
                    nome=data["nome"],
                    cpf=data["cpf"],
                    cnh=data["cnh"],
                    telefone=data["telefone"],
                    email=data["email"],
                    status="ativo"
                )
                self.db.add(motorista)
                self.db.flush()
                logger.info(f"✅ Motorista criado: {motorista.nome}")
            else:
                logger.info(f"ℹ️ Motorista já existe: {motorista.nome}")
            
            motoristas.append(motorista)
        
        return motoristas
    
    def seed_veiculos(self, tenant: Tenant, motoristas: list) -> list:
        """Cria veículos demo"""
        veiculos_data = [
            {
                "placa": "ABC-1234",
                "modelo": "Mercedes-Benz Actros",
                "ano": 2022,
                "motorista": motoristas[0] if motoristas else None
            },
            {
                "placa": "DEF-5678",
                "modelo": "Volvo FH 540",
                "ano": 2021,
                "motorista": motoristas[1] if len(motoristas) > 1 else None
            },
            {
                "placa": "GHI-9012",
                "modelo": "Scania R 450",
                "ano": 2023,
                "motorista": motoristas[2] if len(motoristas) > 2 else None
            }
        ]
        
        veiculos = []
        for data in veiculos_data:
            veiculo = self.db.query(Veiculo).filter_by(
                tenant_id=tenant.id,
                placa=data["placa"]
            ).first()
            
            if not veiculo:
                veiculo = Veiculo(
                    tenant_id=tenant.id,
                    placa=data["placa"],
                    modelo=data["modelo"],
                    ano=data["ano"],
                    motorista_id=data["motorista"].id if data["motorista"] else None,
                    status="disponivel"
                )
                self.db.add(veiculo)
                self.db.flush()
                logger.info(f"✅ Veículo criado: {veiculo.placa}")
            else:
                logger.info(f"ℹ️ Veículo já existe: {veiculo.placa}")
            
            veiculos.append(veiculo)
        
        return veiculos
    
    def seed_cotacao_demo(self, tenant: Tenant, cliente: Cliente, usuario: User) -> Cotacao:
        """Cria cotação demo"""
        cotacao = self.db.query(Cotacao).filter_by(
            tenant_id=tenant.id,
            numero="COT-2024-001"
        ).first()
        
        if not cotacao:
            cotacao = Cotacao(
                tenant_id=tenant.id,
                numero="COT-2024-001",
                cliente_id=cliente.id,
                usuario_id=usuario.id,
                origem_cep="01310-100",
                origem_cidade="São Paulo",
                origem_estado="SP",
                destino_cep="04547-130",
                destino_cidade="São Paulo",
                destino_estado="SP",
                peso_kg=500.0,
                valor_mercadoria=10000.00,
                valor_frete=350.00,
                status="aprovada",
                data_cotacao=datetime.now()
            )
            self.db.add(cotacao)
            self.db.flush()
            logger.info(f"✅ Cotação criada: {cotacao.numero}")
        else:
            logger.info(f"ℹ️ Cotação já existe: {cotacao.numero}")
        
        return cotacao
    
    def seed_pedido_demo(self, tenant: Tenant, cotacao: Cotacao, motorista: Motorista, veiculo: Veiculo) -> Pedido:
        """Cria pedido demo"""
        pedido = self.db.query(Pedido).filter_by(
            tenant_id=tenant.id,
            numero="PED-2024-001"
        ).first()
        
        if not pedido:
            pedido = Pedido(
                tenant_id=tenant.id,
                numero="PED-2024-001",
                cotacao_id=cotacao.id,
                cliente_id=cotacao.cliente_id,
                motorista_id=motorista.id,
                veiculo_id=veiculo.id,
                origem_cep=cotacao.origem_cep,
                origem_cidade=cotacao.origem_cidade,
                origem_estado=cotacao.origem_estado,
                destino_cep=cotacao.destino_cep,
                destino_cidade=cotacao.destino_cidade,
                destino_estado=cotacao.destino_estado,
                peso_kg=cotacao.peso_kg,
                valor_frete=cotacao.valor_frete,
                status="em_transito",
                data_pedido=datetime.now(),
                previsao_entrega=datetime.now() + timedelta(days=3)
            )
            self.db.add(pedido)
            self.db.flush()
            logger.info(f"✅ Pedido criado: {pedido.numero}")
        else:
            logger.info(f"ℹ️ Pedido já existe: {pedido.numero}")
        
        return pedido
    
    def seed_entrega_demo(self, tenant: Tenant, pedido: Pedido) -> Entrega:
        """Cria entrega demo"""
        entrega = self.db.query(Entrega).filter_by(
            tenant_id=tenant.id,
            pedido_id=pedido.id
        ).first()
        
        if not entrega:
            entrega = Entrega(
                tenant_id=tenant.id,
                pedido_id=pedido.id,
                numero_rastreio=f"ENT-{pedido.numero}",
                status="em_transito",
                local_atual="São Paulo - SP",
                ultimo_evento="Carga em trânsito",
                data_ultimo_evento=datetime.now()
            )
            self.db.add(entrega)
            self.db.flush()
            logger.info(f"✅ Entrega criada: {entrega.numero_rastreio}")
        else:
            logger.info(f"ℹ️ Entrega já existe: {entrega.numero_rastreio}")
        
        return entrega
    
    def print_summary(self, admin: User, operador: User, motoristas: list):
        """Imprime resumo dos dados criados"""
        print("\n" + "="*60)
        print("🎉 DADOS DEMO CRIADOS COM SUCESSO!")
        print("="*60)
        print("\n📋 CREDENCIAIS DE ACESSO:")
        print(f"\n👤 Administrador:")
        print(f"   Email:    {admin.email}")
        print(f"   Senha:    admin123")
        print(f"\n👤 Operador:")
        print(f"   Email:    {operador.email}")
        print(f"   Senha:    operador123")
        
        if motoristas:
            print(f"\n🚚 Motoristas Demo:")
            for m in motoristas:
                print(f"   - {m.nome} (CPF: {m.cpf})")
        
        print("\n🌐 ACESSO:")
        print("   Frontend: http://localhost:3001")
        print("   Backend:  http://localhost:8000/docs")
        print("\n" + "="*60 + "\n")


def main():
    """Executa seed de dados demo"""
    logger.info("🚀 LogiFlow CRM - Seed de Dados Demo BETA")
    
    # Criar tabelas se não existem
    Base.metadata.create_all(bind=engine)
    
    # Criar sessão
    db = SessionLocal()
    
    try:
        seeder = DemoDataSeeder(db)
        seeder.seed_all()
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
