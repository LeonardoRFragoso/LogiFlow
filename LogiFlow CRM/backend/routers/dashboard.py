"""
Router para dashboard principal
"""
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


@router.get("/stats")
async def obter_estatisticas_dashboard(db: Session = Depends(get_db)):
    """
    Obtém estatísticas para o dashboard principal
    """
    # TODO: Implementar consultas reais ao banco de dados
    
    # Mock de dados para desenvolvimento
    stats = {
        "em_transito": random.randint(15, 45),
        "entregas_hoje": random.randint(8, 25),
        "atrasados": random.randint(0, 5),
        "cotacoes_abertas": random.randint(5, 20),
        "sla": {
            "verde": random.randint(60, 80),  # No prazo
            "amarelo": random.randint(10, 25),  # Atenção
            "vermelho": random.randint(0, 10)  # Atrasado
        },
        "entregas_recentes": [
            {
                "id": 1,
                "codigo": "ENT-2024-001",
                "cliente": "Alpha Trans",
                "destino": "São Paulo/SP",
                "status": "em_transito",
                "previsao": (datetime.now() + timedelta(hours=4)).isoformat(),
                "motorista": "João Silva",
                "placa": "ABC-1234"
            },
            {
                "id": 2,
                "codigo": "ENT-2024-002",
                "cliente": "Beta Log",
                "destino": "Rio de Janeiro/RJ",
                "status": "saiu_para_entrega",
                "previsao": (datetime.now() + timedelta(hours=2)).isoformat(),
                "motorista": "Maria Santos",
                "placa": "DEF-5678"
            },
            {
                "id": 3,
                "codigo": "ENT-2024-003",
                "cliente": "Gamma Cargo",
                "destino": "Belo Horizonte/MG",
                "status": "em_transito",
                "previsao": (datetime.now() + timedelta(hours=6)).isoformat(),
                "motorista": "Pedro Costa",
                "placa": "GHI-9012"
            }
        ],
        "ocorrencias_abertas": [
            {
                "id": 1,
                "tipo": "atraso",
                "descricao": "Veículo retido em fiscalização",
                "entrega_codigo": "ENT-2024-015",
                "status": "aberta",
                "criado_em": (datetime.now() - timedelta(hours=3)).isoformat()
            },
            {
                "id": 2,
                "tipo": "avaria",
                "descricao": "Embalagem danificada na carga",
                "entrega_codigo": "ENT-2024-012",
                "status": "em_analise",
                "criado_em": (datetime.now() - timedelta(hours=5)).isoformat()
            }
        ],
        "motoristas_disponiveis": random.randint(5, 15),
        "veiculos_disponiveis": random.randint(8, 20),
        "faturamento_mes": {
            "valor": random.randint(150000, 500000),
            "crescimento": random.uniform(-5.0, 15.0)
        },
        "alertas": [
            {
                "tipo": "cnh_vencendo",
                "motorista": "João Silva",
                "dias": 15,
                "prioridade": "media"
            },
            {
                "tipo": "manutencao",
                "veiculo": "ABC-1234",
                "km": 95000,
                "prioridade": "alta"
            }
        ]
    }
    
    return {"data": stats}


@router.get("/graficos/entregas-mes")
async def obter_grafico_entregas_mes(db: Session = Depends(get_db)):
    """
    Obtém dados para gráfico de entregas do mês
    """
    # Mock de dados
    dados = []
    for i in range(1, 31):
        dados.append({
            "dia": i,
            "entregas": random.randint(5, 25),
            "atrasadas": random.randint(0, 3)
        })
    
    return {"data": dados}


@router.get("/graficos/faturamento-trimestre")
async def obter_grafico_faturamento_trimestre(db: Session = Depends(get_db)):
    """
    Obtém dados para gráfico de faturamento do trimestre
    """
    meses = ["Janeiro", "Fevereiro", "Março"]
    dados = []
    
    for mes in meses:
        dados.append({
            "mes": mes,
            "faturamento": random.randint(100000, 500000),
            "meta": 300000
        })
    
    return {"data": dados}


@router.get("/graficos/status-entregas")
async def obter_grafico_status_entregas(db: Session = Depends(get_db)):
    """
    Obtém distribuição de status das entregas
    """
    dados = {
        "aguardando_coleta": random.randint(5, 15),
        "coletado": random.randint(3, 10),
        "em_transito": random.randint(10, 30),
        "saiu_para_entrega": random.randint(5, 15),
        "entregue": random.randint(50, 100),
        "atrasado": random.randint(0, 5)
    }
    
    return {"data": dados}

