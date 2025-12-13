"""
LogiFlow CRM - Seed Data
========================
Dados de demonstração para compartilhar entre os apps:
- App Web (localhost:3000)
- App Motorista (localhost:5174)
- Portal Cliente (localhost:5173)

Execute: python seed_data.py
"""

from datetime import datetime, timedelta
import random
import uuid

# ========================================
# Storage Global (compartilhado)
# ========================================

# Motoristas
motoristas_db = {}

# Veículos
veiculos_db = {}

# Clientes
clientes_db = {}

# Pedidos
pedidos_db = {}

# Entregas
entregas_db = {}

# Cotações
cotacoes_db = {}

# Ocorrências
ocorrencias_db = {}


def gerar_id():
    return str(uuid.uuid4())[:8].upper()


def seed_motoristas():
    """Cria motoristas de demonstração"""
    motoristas = [
        {
            "id": gerar_id(),
            "nome": "Carlos Santos",
            "cpf": "123.456.789-00",
            "telefone": "(21) 99999-1111",
            "email": "carlos@logiflow.com",
            "cnh_numero": "12345678901",
            "cnh_categoria": "E",
            "cnh_validade": "2026-12-31",
            "status": "disponivel",
            "foto_url": None,
            "veiculo_id": None,
            "entregas_hoje": 5,
            "avaliacao": 4.8,
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
        {
            "id": gerar_id(),
            "nome": "Pedro Lima",
            "cpf": "987.654.321-00",
            "telefone": "(21) 99999-2222",
            "email": "pedro@logiflow.com",
            "cnh_numero": "98765432109",
            "cnh_categoria": "D",
            "cnh_validade": "2025-08-15",
            "status": "em_rota",
            "foto_url": None,
            "veiculo_id": None,
            "entregas_hoje": 3,
            "avaliacao": 4.5,
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
        {
            "id": gerar_id(),
            "nome": "João Oliveira",
            "cpf": "456.789.123-00",
            "telefone": "(21) 99999-3333",
            "email": "joao@logiflow.com",
            "cnh_numero": "45678912345",
            "cnh_categoria": "E",
            "cnh_validade": "2027-03-20",
            "status": "disponivel",
            "foto_url": None,
            "veiculo_id": None,
            "entregas_hoje": 8,
            "avaliacao": 4.9,
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
    ]
    
    for m in motoristas:
        motoristas_db[m["id"]] = m
    
    print(f"✅ {len(motoristas)} motoristas criados")
    return motoristas


def seed_veiculos():
    """Cria veículos de demonstração"""
    veiculos = [
        {
            "id": gerar_id(),
            "placa": "ABC-1234",
            "tipo": "VUC",
            "marca": "Mercedes-Benz",
            "modelo": "Accelo 815",
            "ano": 2022,
            "capacidade_kg": 3500,
            "capacidade_m3": 18,
            "status": "disponivel",
            "km_atual": 45230,
            "ultima_manutencao": "2025-11-15",
            "proxima_manutencao": "2026-02-15",
            "motorista_id": None,
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
        {
            "id": gerar_id(),
            "placa": "XYZ-5678",
            "tipo": "Truck",
            "marca": "Volvo",
            "modelo": "VM 270",
            "ano": 2021,
            "capacidade_kg": 14000,
            "capacidade_m3": 45,
            "status": "em_uso",
            "km_atual": 89450,
            "ultima_manutencao": "2025-10-20",
            "proxima_manutencao": "2026-01-20",
            "motorista_id": None,
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
        {
            "id": gerar_id(),
            "placa": "QWE-9012",
            "tipo": "Carreta",
            "marca": "Scania",
            "modelo": "R450",
            "ano": 2023,
            "capacidade_kg": 28000,
            "capacidade_m3": 90,
            "status": "disponivel",
            "km_atual": 23100,
            "ultima_manutencao": "2025-12-01",
            "proxima_manutencao": "2026-03-01",
            "motorista_id": None,
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
    ]
    
    for v in veiculos:
        veiculos_db[v["id"]] = v
    
    print(f"✅ {len(veiculos)} veículos criados")
    return veiculos


def seed_clientes():
    """Cria clientes de demonstração"""
    clientes = [
        {
            "id": gerar_id(),
            "razao_social": "Tech Solutions LTDA",
            "nome_fantasia": "TechSol",
            "cnpj": "12.345.678/0001-90",
            "inscricao_estadual": "123456789",
            "email": "contato@techsol.com.br",
            "telefone": "(21) 3333-1111",
            "celular": "(21) 99999-4444",
            "endereco": "Av. Rio Branco, 100",
            "bairro": "Centro",
            "cidade": "Rio de Janeiro",
            "uf": "RJ",
            "cep": "20040-001",
            "contato_nome": "Maria Silva",
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
        {
            "id": gerar_id(),
            "razao_social": "Comércio Express LTDA",
            "nome_fantasia": "Express",
            "cnpj": "98.765.432/0001-10",
            "inscricao_estadual": "987654321",
            "email": "vendas@express.com.br",
            "telefone": "(21) 3333-2222",
            "celular": "(21) 99999-5555",
            "endereco": "Rua das Flores, 200",
            "bairro": "Botafogo",
            "cidade": "Rio de Janeiro",
            "uf": "RJ",
            "cep": "22250-040",
            "contato_nome": "João Pereira",
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
        {
            "id": gerar_id(),
            "razao_social": "Distribuidora Nacional SA",
            "nome_fantasia": "DistriNac",
            "cnpj": "11.222.333/0001-44",
            "inscricao_estadual": "112233445",
            "email": "pedidos@distrinac.com.br",
            "telefone": "(21) 3333-3333",
            "celular": "(21) 99999-6666",
            "endereco": "Av. Brasil, 5000",
            "bairro": "Bonsucesso",
            "cidade": "Rio de Janeiro",
            "uf": "RJ",
            "cep": "21041-000",
            "contato_nome": "Ana Costa",
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        },
    ]
    
    for c in clientes:
        clientes_db[c["id"]] = c
    
    print(f"✅ {len(clientes)} clientes criados")
    return clientes


def seed_pedidos(clientes, motoristas):
    """Cria pedidos de demonstração"""
    status_list = ["aguardando", "em_separacao", "coletado", "em_transito", "entregue"]
    
    pedidos = []
    for i in range(10):
        cliente = random.choice(clientes)
        motorista = random.choice(motoristas) if random.random() > 0.3 else None
        status = random.choice(status_list)
        
        pedido = {
            "id": gerar_id(),
            "numero": f"PED-2024-{str(i+1).zfill(4)}",
            "cliente_id": cliente["id"],
            "cliente_nome": cliente["nome_fantasia"],
            "cliente_cnpj": cliente["cnpj"],
            "motorista_id": motorista["id"] if motorista else None,
            "motorista_nome": motorista["nome"] if motorista else None,
            "origem_endereco": "Rua da Expedição, 500, Galpão 3",
            "origem_cidade": "Rio de Janeiro",
            "origem_uf": "RJ",
            "destino_endereco": cliente["endereco"],
            "destino_cidade": cliente["cidade"],
            "destino_uf": cliente["uf"],
            "destino_cep": cliente["cep"],
            "rota": f"Rio de Janeiro/RJ → {cliente['cidade']}/{cliente['uf']}",
            "peso_kg": random.randint(50, 5000),
            "volumes": random.randint(1, 50),
            "valor_mercadoria": round(random.uniform(500, 50000), 2),
            "valor_frete": round(random.uniform(100, 2000), 2),
            "status": status,
            "sla_status": random.choice(["verde", "amarelo", "vermelho"]),
            "previsao_entrega": (datetime.now() + timedelta(days=random.randint(0, 5))).isoformat(),
            "data_coleta": datetime.now().isoformat() if status != "aguardando" else None,
            "data_entrega": datetime.now().isoformat() if status == "entregue" else None,
            "observacoes": None,
            "criado_em": (datetime.now() - timedelta(days=random.randint(0, 10))).isoformat()
        }
        pedidos.append(pedido)
        pedidos_db[pedido["id"]] = pedido
    
    print(f"✅ {len(pedidos)} pedidos criados")
    return pedidos


def seed_entregas(pedidos, motoristas):
    """Cria entregas de demonstração"""
    status_list = ["aguardando_coleta", "coletado", "em_transito", "saiu_para_entrega", "entregue"]
    
    entregas = []
    for i, pedido in enumerate(pedidos[:8]):
        motorista = random.choice(motoristas)
        status = random.choice(status_list)
        
        entrega = {
            "id": gerar_id(),
            "codigo": f"ENT-2024-{str(i+1).zfill(4)}",
            "pedido_id": pedido["id"],
            "pedido_numero": pedido["numero"],
            "cliente_id": pedido["cliente_id"],
            "cliente_nome": pedido["cliente_nome"],
            "cliente_telefone": "(21) 99999-7777",
            "motorista_id": motorista["id"],
            "motorista_nome": motorista["nome"],
            "motorista_telefone": motorista["telefone"],
            "endereco_rua": pedido["destino_endereco"],
            "endereco_bairro": "Centro",
            "endereco_cidade": pedido["destino_cidade"],
            "endereco_uf": pedido["destino_uf"],
            "endereco_cep": pedido["destino_cep"],
            "latitude": -22.9068 + random.uniform(-0.1, 0.1),
            "longitude": -43.1729 + random.uniform(-0.1, 0.1),
            "volumes": pedido["volumes"],
            "peso": pedido["peso_kg"],
            "valor_mercadoria": pedido["valor_mercadoria"],
            "valor_frete": pedido["valor_frete"],
            "status": status,
            "progresso": {"aguardando_coleta": 10, "coletado": 30, "em_transito": 60, "saiu_para_entrega": 85, "entregue": 100}[status],
            "previsao_entrega": pedido["previsao_entrega"],
            "data_coleta": datetime.now().isoformat() if status not in ["aguardando_coleta"] else None,
            "data_entrega": datetime.now().isoformat() if status == "entregue" else None,
            "assinatura_recebedor": None,
            "foto_comprovante": None,
            "observacoes": None,
            "atrasada": random.random() > 0.8,
            "criado_em": datetime.now().isoformat()
        }
        entregas.append(entrega)
        entregas_db[entrega["id"]] = entrega
    
    print(f"✅ {len(entregas)} entregas criadas")
    return entregas


def seed_cotacoes(clientes):
    """Cria cotações de demonstração"""
    status_list = ["pendente", "enviada", "aprovada", "recusada"]
    
    cotacoes = []
    for i in range(5):
        cliente = random.choice(clientes)
        status = random.choice(status_list)
        
        cotacao = {
            "id": gerar_id(),
            "numero": f"COT-2024-{str(i+1).zfill(4)}",
            "cliente_id": cliente["id"],
            "cliente_nome": cliente["nome_fantasia"],
            "origem_cidade": "Rio de Janeiro",
            "origem_uf": "RJ",
            "destino_cidade": cliente["cidade"],
            "destino_uf": cliente["uf"],
            "peso_kg": random.randint(100, 10000),
            "valor_mercadoria": round(random.uniform(1000, 100000), 2),
            "valor_frete": round(random.uniform(200, 5000), 2),
            "prazo_dias": random.randint(1, 7),
            "status": status,
            "validade": (datetime.now() + timedelta(days=7)).isoformat(),
            "observacoes": None,
            "criado_em": (datetime.now() - timedelta(days=random.randint(0, 5))).isoformat()
        }
        cotacoes.append(cotacao)
        cotacoes_db[cotacao["id"]] = cotacao
    
    print(f"✅ {len(cotacoes)} cotações criadas")
    return cotacoes


def seed_ocorrencias(pedidos):
    """Cria ocorrências de demonstração"""
    tipos = ["atraso", "avaria", "extravio", "recusa", "outros"]
    status_list = ["aberta", "em_analise", "resolvida"]
    prioridades = ["baixa", "media", "alta", "critica"]
    
    titulos = {
        "atraso": ["Atraso na entrega", "Previsão de atraso", "Entrega atrasada"],
        "avaria": ["Mercadoria avariada", "Dano na carga", "Produto danificado"],
        "extravio": ["Carga extraviada", "Mercadoria não localizada", "Perda de carga"],
        "recusa": ["Recusa de entrega", "Cliente recusou receber", "Entrega não aceita"],
        "outros": ["Problema no endereço", "Documentação incorreta", "Acesso negado"]
    }
    
    ocorrencias = []
    for i in range(12):
        pedido = random.choice(pedidos)
        tipo = random.choice(tipos)
        status = random.choice(status_list)
        prioridade = random.choice(prioridades)
        
        ocorrencia = {
            "id": gerar_id(),
            "numero": f"OCO-2024-{str(i+1001).zfill(6)}",
            "pedido_id": pedido["id"],
            "pedido_numero": pedido["numero"],
            "tipo": tipo,
            "titulo": random.choice(titulos[tipo]),
            "descricao": f"Ocorrência registrada no pedido {pedido['numero']}. Necessário acompanhamento.",
            "prioridade": prioridade,
            "status": status,
            "data_ocorrencia": (datetime.now() - timedelta(hours=random.randint(1, 72))),
            "local_ocorrencia": f"{pedido['destino_cidade']}, {pedido['destino_uf']}",
            "motorista_id": pedido.get("motorista_id"),
            "veiculo_id": None,
            "fotos": [],
            "documentos": [],
            "comentarios": [],
            "resolucao": "Problema resolvido com sucesso" if status == "resolvida" else None,
            "resolvida_em": datetime.now() if status == "resolvida" else None,
            "criado_em": (datetime.now() - timedelta(hours=random.randint(1, 72))),
            "atualizado_em": datetime.now(),
            "historico": [
                {
                    "data": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                    "status": "aberta",
                    "descricao": "Ocorrência criada"
                }
            ]
        }
        
        if status == "resolvida":
            ocorrencia["historico"].append({
                "data": datetime.now().isoformat(),
                "status": "resolvida",
                "descricao": "Ocorrência resolvida"
            })
        
        ocorrencias.append(ocorrencia)
        ocorrencias_db[ocorrencia["id"]] = ocorrencia
    
    print(f"✅ {len(ocorrencias)} ocorrências criadas")
    return ocorrencias


def seed_all():
    """Executa todos os seeds"""
    print("\n" + "="*50)
    print("🌱 LogiFlow CRM - Seed Data")
    print("="*50 + "\n")
    
    motoristas = seed_motoristas()
    veiculos = seed_veiculos()
    clientes = seed_clientes()
    pedidos = seed_pedidos(clientes, motoristas)
    entregas = seed_entregas(pedidos, motoristas)
    cotacoes = seed_cotacoes(clientes)
    ocorrencias = seed_ocorrencias(pedidos)
    
    # Vincular motoristas a veículos
    if motoristas and veiculos:
        motoristas[0]["veiculo_id"] = veiculos[0]["id"]
        veiculos[0]["motorista_id"] = motoristas[0]["id"]
        motoristas[1]["veiculo_id"] = veiculos[1]["id"]
        veiculos[1]["motorista_id"] = motoristas[1]["id"]
    
    print("\n" + "="*50)
    print("✅ Seed concluído!")
    print("="*50)
    print(f"\nTotal de registros:")
    print(f"  - Motoristas: {len(motoristas_db)}")
    print(f"  - Veículos: {len(veiculos_db)}")
    print(f"  - Clientes: {len(clientes_db)}")
    print(f"  - Pedidos: {len(pedidos_db)}")
    print(f"  - Entregas: {len(entregas_db)}")
    print(f"  - Cotações: {len(cotacoes_db)}")
    print(f"  - Ocorrências: {len(ocorrencias_db)}")
    print("\n")
    
    return {
        "motoristas": list(motoristas_db.values()),
        "veiculos": list(veiculos_db.values()),
        "clientes": list(clientes_db.values()),
        "pedidos": list(pedidos_db.values()),
        "entregas": list(entregas_db.values()),
        "cotacoes": list(cotacoes_db.values()),
        "ocorrencias": list(ocorrencias_db.values()),
    }


# Executar seed ao importar
if __name__ == "__main__":
    seed_all()
else:
    # Auto-seed ao importar como módulo
    seed_all()
