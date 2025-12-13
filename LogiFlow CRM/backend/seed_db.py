"""
LogiFlow CRM - Database Seed
============================
Popula o banco de dados com dados de demonstração
Execute: python seed_db.py
"""

from datetime import datetime, timedelta
import random

from database import SessionLocal, init_db
from models import Cliente, Motorista, Veiculo, Pedido, Entrega, Cotacao


def seed_database():
    """Popula o banco de dados com dados de demonstração"""
    print("\n" + "="*50)
    print("🌱 LogiFlow CRM - Seed Database")
    print("="*50 + "\n")
    
    # Inicializar banco
    init_db()
    print("✅ Tabelas criadas")
    
    db = SessionLocal()
    
    try:
        # Verificar se já tem dados
        if db.query(Cliente).count() > 0:
            print("⚠️  Banco já possui dados. Pulando seed...")
            print("   Use 'python seed_db.py --force' para recriar")
            return
        
        # ========== Clientes ==========
        clientes = [
            Cliente(
                razao_social="Tech Solutions LTDA",
                nome_fantasia="TechSol",
                cnpj="12.345.678/0001-90",
                inscricao_estadual="123456789",
                email="contato@techsol.com.br",
                telefone="(21) 3333-1111",
                celular="(21) 99999-4444",
                endereco="Av. Rio Branco, 100",
                bairro="Centro",
                cidade="Rio de Janeiro",
                uf="RJ",
                cep="20040-001",
                contato_nome="Maria Silva"
            ),
            Cliente(
                razao_social="Comércio Express LTDA",
                nome_fantasia="Express",
                cnpj="98.765.432/0001-10",
                email="vendas@express.com.br",
                telefone="(21) 3333-2222",
                endereco="Rua das Flores, 200",
                bairro="Botafogo",
                cidade="Rio de Janeiro",
                uf="RJ",
                cep="22250-040",
                contato_nome="João Pereira"
            ),
            Cliente(
                razao_social="Distribuidora Nacional SA",
                nome_fantasia="DistriNac",
                cnpj="11.222.333/0001-44",
                email="pedidos@distrinac.com.br",
                telefone="(21) 3333-3333",
                endereco="Av. Brasil, 5000",
                bairro="Bonsucesso",
                cidade="Rio de Janeiro",
                uf="RJ",
                cep="21041-000",
                contato_nome="Ana Costa"
            ),
        ]
        
        for c in clientes:
            db.add(c)
        db.commit()
        print(f"✅ {len(clientes)} clientes criados")
        
        # ========== Veículos ==========
        veiculos = [
            Veiculo(
                placa="ABC-1234",
                tipo="VUC",
                marca="Mercedes-Benz",
                modelo="Accelo 815",
                ano=2022,
                capacidade_kg=3500,
                capacidade_m3=18,
                status="disponivel",
                km_atual=45230
            ),
            Veiculo(
                placa="XYZ-5678",
                tipo="Truck",
                marca="Volvo",
                modelo="VM 270",
                ano=2021,
                capacidade_kg=14000,
                capacidade_m3=45,
                status="em_uso",
                km_atual=89450
            ),
            Veiculo(
                placa="QWE-9012",
                tipo="Carreta",
                marca="Scania",
                modelo="R450",
                ano=2023,
                capacidade_kg=28000,
                capacidade_m3=90,
                status="disponivel",
                km_atual=23100
            ),
        ]
        
        for v in veiculos:
            db.add(v)
        db.commit()
        print(f"✅ {len(veiculos)} veículos criados")
        
        # ========== Motoristas ==========
        motoristas = [
            Motorista(
                nome="Carlos Santos",
                cpf="123.456.789-00",
                telefone="(21) 99999-1111",
                email="carlos@logiflow.com",
                cnh_numero="12345678901",
                cnh_categoria="E",
                cnh_validade="2026-12-31",
                status="disponivel",
                avaliacao=4.8,
                veiculo_id=veiculos[0].id
            ),
            Motorista(
                nome="Pedro Lima",
                cpf="987.654.321-00",
                telefone="(21) 99999-2222",
                email="pedro@logiflow.com",
                cnh_numero="98765432109",
                cnh_categoria="D",
                cnh_validade="2025-08-15",
                status="em_rota",
                avaliacao=4.5,
                veiculo_id=veiculos[1].id
            ),
            Motorista(
                nome="João Oliveira",
                cpf="456.789.123-00",
                telefone="(21) 99999-3333",
                email="joao@logiflow.com",
                cnh_numero="45678912345",
                cnh_categoria="E",
                cnh_validade="2027-03-20",
                status="disponivel",
                avaliacao=4.9
            ),
        ]
        
        for m in motoristas:
            db.add(m)
        db.commit()
        print(f"✅ {len(motoristas)} motoristas criados")
        
        # ========== Pedidos ==========
        pedidos = []
        status_list = ["aguardando", "em_separacao", "coletado", "em_transito", "entregue"]
        
        for i in range(10):
            cliente = random.choice(clientes)
            motorista = random.choice(motoristas) if random.random() > 0.3 else None
            status = random.choice(status_list)
            
            pedido = Pedido(
                numero=f"PED-2024-{str(i+1).zfill(4)}",
                cliente_id=cliente.id,
                motorista_id=motorista.id if motorista else None,
                origem_endereco="Rua da Expedição, 500, Galpão 3",
                origem_cidade="Rio de Janeiro",
                origem_uf="RJ",
                destino_endereco=cliente.endereco,
                destino_cidade=cliente.cidade,
                destino_uf=cliente.uf,
                destino_cep=cliente.cep,
                peso_kg=random.randint(50, 5000),
                volumes=random.randint(1, 50),
                valor_mercadoria=round(random.uniform(500, 50000), 2),
                valor_frete=round(random.uniform(100, 2000), 2),
                status=status,
                sla_status=random.choice(["verde", "amarelo", "vermelho"]),
                previsao_entrega=datetime.now() + timedelta(days=random.randint(0, 5)),
                data_coleta=datetime.now() if status != "aguardando" else None,
                data_entrega=datetime.now() if status == "entregue" else None
            )
            pedidos.append(pedido)
            db.add(pedido)
        
        db.commit()
        print(f"✅ {len(pedidos)} pedidos criados")
        
        # ========== Entregas ==========
        entregas = []
        status_entrega = ["aguardando_coleta", "coletado", "em_transito", "saiu_para_entrega", "entregue"]
        progresso_map = {"aguardando_coleta": 10, "coletado": 30, "em_transito": 60, "saiu_para_entrega": 85, "entregue": 100}
        
        for i, pedido in enumerate(pedidos[:8]):
            motorista = random.choice(motoristas)
            status = random.choice(status_entrega)
            cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
            
            entrega = Entrega(
                codigo=f"ENT-2024-{str(i+1).zfill(4)}",
                pedido_id=pedido.id,
                motorista_id=motorista.id,
                cliente_nome=cliente.nome_fantasia,
                cliente_telefone=cliente.celular or "(21) 99999-7777",
                endereco_rua=cliente.endereco,
                endereco_bairro=cliente.bairro,
                endereco_cidade=cliente.cidade,
                endereco_uf=cliente.uf,
                endereco_cep=cliente.cep,
                latitude=-22.9068 + random.uniform(-0.1, 0.1),
                longitude=-43.1729 + random.uniform(-0.1, 0.1),
                volumes=pedido.volumes,
                peso=pedido.peso_kg,
                valor_mercadoria=pedido.valor_mercadoria,
                valor_frete=pedido.valor_frete,
                status=status,
                progresso=progresso_map.get(status, 50),
                previsao_entrega=pedido.previsao_entrega,
                data_coleta=datetime.now() if status not in ["aguardando_coleta"] else None,
                data_entrega=datetime.now() if status == "entregue" else None,
                atrasada=random.random() > 0.8
            )
            entregas.append(entrega)
            db.add(entrega)
        
        db.commit()
        print(f"✅ {len(entregas)} entregas criadas")
        
        # ========== Cotações ==========
        cotacoes = []
        status_cotacao = ["pendente", "enviada", "aprovada", "recusada"]
        
        for i in range(5):
            cliente = random.choice(clientes)
            status = random.choice(status_cotacao)
            
            cotacao = Cotacao(
                numero=f"COT-2024-{str(i+1).zfill(4)}",
                cliente_id=cliente.id,
                origem_cidade="Rio de Janeiro",
                origem_uf="RJ",
                destino_cidade=cliente.cidade,
                destino_uf=cliente.uf,
                peso_kg=random.randint(100, 10000),
                valor_mercadoria=round(random.uniform(1000, 100000), 2),
                valor_frete=round(random.uniform(200, 5000), 2),
                prazo_dias=random.randint(1, 7),
                status=status,
                validade=datetime.now() + timedelta(days=7)
            )
            cotacoes.append(cotacao)
            db.add(cotacao)
        
        db.commit()
        print(f"✅ {len(cotacoes)} cotações criadas")
        
        # ========== Resumo ==========
        print("\n" + "="*50)
        print("✅ Seed concluído!")
        print("="*50)
        print(f"\nTotal de registros:")
        print(f"  - Clientes:   {len(clientes)}")
        print(f"  - Veículos:   {len(veiculos)}")
        print(f"  - Motoristas: {len(motoristas)}")
        print(f"  - Pedidos:    {len(pedidos)}")
        print(f"  - Entregas:   {len(entregas)}")
        print(f"  - Cotações:   {len(cotacoes)}")
        print("\n📁 Banco de dados: logiflow.db")
        print("\n")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if "--force" in sys.argv:
        import os
        if os.path.exists("logiflow.db"):
            os.remove("logiflow.db")
            print("🗑️  Banco anterior removido")
    
    seed_database()
