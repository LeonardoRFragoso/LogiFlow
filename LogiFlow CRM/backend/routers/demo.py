"""
LogiFlow CRM - Demo Data Router
===============================
Endpoints para dados de demonstração compartilhados entre apps
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime
import random

router = APIRouter(prefix="/demo", tags=["Demo Data"])

# Importar dados de seed
from seed_data import (
    motoristas_db, veiculos_db, clientes_db,
    pedidos_db, entregas_db, cotacoes_db,
    seed_all
)


# ========================================
# Endpoints - Motoristas
# ========================================

@router.get("/motoristas")
async def listar_motoristas(ativo: bool = True):
    """Lista motoristas para App Motorista e App Web"""
    result = [m for m in motoristas_db.values() if m.get("ativo", True) == ativo]
    return {"success": True, "data": result, "count": len(result)}


@router.get("/motoristas/{motorista_id}")
async def obter_motorista(motorista_id: str):
    """Obtém dados de um motorista específico"""
    motorista = motoristas_db.get(motorista_id)
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return {"success": True, "data": motorista}


@router.get("/motoristas/{motorista_id}/entregas")
async def entregas_do_motorista(motorista_id: str, status: Optional[str] = None):
    """Lista entregas de um motorista - usado pelo App Motorista"""
    entregas = [e for e in entregas_db.values() if e.get("motorista_id") == motorista_id]
    if status:
        entregas = [e for e in entregas if e.get("status") == status]
    return {"success": True, "data": entregas, "count": len(entregas)}


# ========================================
# Endpoints - Entregas
# ========================================

@router.get("/entregas")
async def listar_entregas(
    status: Optional[str] = None,
    motorista_id: Optional[str] = None
):
    """Lista entregas - usado por todos os apps"""
    result = list(entregas_db.values())
    
    if status:
        result = [e for e in result if e.get("status") == status]
    if motorista_id:
        result = [e for e in result if e.get("motorista_id") == motorista_id]
    
    return {"success": True, "data": result, "count": len(result)}


@router.get("/entregas/{entrega_id}")
async def obter_entrega(entrega_id: str):
    """Obtém dados de uma entrega - usado por todos os apps"""
    entrega = entregas_db.get(entrega_id)
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return {"success": True, "data": entrega}


@router.get("/entregas/codigo/{codigo}")
async def obter_entrega_por_codigo(codigo: str):
    """Obtém entrega pelo código - usado pelo Portal Cliente"""
    for entrega in entregas_db.values():
        if entrega.get("codigo", "").upper() == codigo.upper():
            return {"success": True, "data": entrega}
    raise HTTPException(status_code=404, detail="Entrega não encontrada")


@router.patch("/entregas/{entrega_id}/status")
async def atualizar_status_entrega(entrega_id: str, novo_status: str, observacao: Optional[str] = None):
    """Atualiza status de entrega - usado pelo App Motorista"""
    entrega = entregas_db.get(entrega_id)
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    
    status_progresso = {
        "aguardando_coleta": 10,
        "coletado": 30,
        "em_transito": 60,
        "saiu_para_entrega": 85,
        "entregue": 100
    }
    
    entrega["status"] = novo_status
    entrega["progresso"] = status_progresso.get(novo_status, 50)
    
    if novo_status == "entregue":
        entrega["data_entrega"] = datetime.now().isoformat()
    
    if observacao:
        entrega["observacoes"] = observacao
    
    return {"success": True, "data": entrega, "message": f"Status atualizado para {novo_status}"}


# ========================================
# Endpoints - Pedidos
# ========================================

@router.get("/pedidos")
async def listar_pedidos(status: Optional[str] = None):
    """Lista pedidos - usado pelo App Web"""
    result = list(pedidos_db.values())
    if status:
        result = [p for p in result if p.get("status") == status]
    return {"success": True, "data": result, "count": len(result)}


@router.get("/pedidos/{pedido_id}")
async def obter_pedido(pedido_id: str):
    """Obtém dados de um pedido"""
    pedido = pedidos_db.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"success": True, "data": pedido}


# ========================================
# Endpoints - Clientes
# ========================================

@router.get("/clientes")
async def listar_clientes():
    """Lista clientes - usado pelo App Web"""
    result = list(clientes_db.values())
    return {"success": True, "data": result, "count": len(result)}


@router.get("/clientes/{cliente_id}")
async def obter_cliente(cliente_id: str):
    """Obtém dados de um cliente"""
    cliente = clientes_db.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"success": True, "data": cliente}


# ========================================
# Endpoints - Veículos
# ========================================

@router.get("/veiculos")
async def listar_veiculos(status: Optional[str] = None):
    """Lista veículos - usado pelo App Web"""
    result = list(veiculos_db.values())
    if status:
        result = [v for v in result if v.get("status") == status]
    return {"success": True, "data": result, "count": len(result)}


# ========================================
# Endpoints - Cotações
# ========================================

@router.get("/cotacoes")
async def listar_cotacoes(status: Optional[str] = None):
    """Lista cotações - usado pelo App Web"""
    result = list(cotacoes_db.values())
    if status:
        result = [c for c in result if c.get("status") == status]
    return {"success": True, "data": result, "count": len(result)}


# ========================================
# Endpoints - Rastreamento (Portal Cliente)
# ========================================

@router.get("/rastreamento/{codigo}")
async def rastrear_entrega(codigo: str):
    """
    Rastreia entrega pelo código - usado pelo Portal Cliente
    Retorna dados públicos da entrega para o cliente
    """
    for entrega in entregas_db.values():
        if entrega.get("codigo", "").upper() == codigo.upper():
            # Retornar apenas dados públicos
            return {
                "success": True,
                "data": {
                    "codigo": entrega["codigo"],
                    "status": entrega["status"],
                    "progresso": entrega["progresso"],
                    "previsao_entrega": entrega["previsao_entrega"],
                    "endereco_cidade": entrega["endereco_cidade"],
                    "endereco_uf": entrega["endereco_uf"],
                    "motorista_nome": entrega.get("motorista_nome"),
                    "data_coleta": entrega.get("data_coleta"),
                    "data_entrega": entrega.get("data_entrega"),
                    "eventos": [
                        {"data": entrega["criado_em"], "descricao": "Pedido criado", "tipo": "info"},
                        {"data": entrega.get("data_coleta"), "descricao": "Mercadoria coletada", "tipo": "coleta"} if entrega.get("data_coleta") else None,
                        {"data": datetime.now().isoformat(), "descricao": f"Status atual: {entrega['status'].replace('_', ' ').title()}", "tipo": "status"},
                    ]
                }
            }
    
    raise HTTPException(status_code=404, detail="Código de rastreamento não encontrado")


# ========================================
# Endpoints - Dashboard Stats
# ========================================

@router.get("/dashboard/stats")
async def obter_stats_dashboard():
    """Estatísticas para o Dashboard - usado pelo App Web"""
    entregas = list(entregas_db.values())
    pedidos = list(pedidos_db.values())
    
    return {
        "success": True,
        "data": {
            "entregas": {
                "total": len(entregas),
                "em_transito": len([e for e in entregas if e["status"] in ["em_transito", "saiu_para_entrega"]]),
                "entregues_hoje": len([e for e in entregas if e["status"] == "entregue"]),
                "atrasadas": len([e for e in entregas if e.get("atrasada")])
            },
            "pedidos": {
                "total": len(pedidos),
                "aguardando": len([p for p in pedidos if p["status"] == "aguardando"]),
                "em_transito": len([p for p in pedidos if p["status"] == "em_transito"]),
                "entregues": len([p for p in pedidos if p["status"] == "entregue"])
            },
            "motoristas": {
                "total": len(motoristas_db),
                "disponiveis": len([m for m in motoristas_db.values() if m["status"] == "disponivel"]),
                "em_rota": len([m for m in motoristas_db.values() if m["status"] == "em_rota"])
            },
            "veiculos": {
                "total": len(veiculos_db),
                "disponiveis": len([v for v in veiculos_db.values() if v["status"] == "disponivel"])
            },
            "cotacoes": {
                "total": len(cotacoes_db),
                "pendentes": len([c for c in cotacoes_db.values() if c["status"] == "pendente"])
            }
        }
    }


# ========================================
# Endpoint - Reset/Seed
# ========================================

@router.post("/seed")
async def executar_seed():
    """Re-executa o seed de dados"""
    # Limpar dados existentes
    motoristas_db.clear()
    veiculos_db.clear()
    clientes_db.clear()
    pedidos_db.clear()
    entregas_db.clear()
    cotacoes_db.clear()
    
    # Executar seed
    data = seed_all()
    
    return {
        "success": True,
        "message": "Dados de demonstração recriados",
        "counts": {
            "motoristas": len(data["motoristas"]),
            "veiculos": len(data["veiculos"]),
            "clientes": len(data["clientes"]),
            "pedidos": len(data["pedidos"]),
            "entregas": len(data["entregas"]),
            "cotacoes": len(data["cotacoes"])
        }
    }
