"""
LogiFlow CRM - Database API Router
===================================
Endpoints usando banco de dados real (SQLite/PostgreSQL)
NOTA: Requer SQLAlchemy instalado
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from datetime import datetime

# Importações opcionais do SQLAlchemy
try:
    from sqlalchemy.orm import Session
    from database import get_db
    from models import Cliente, Motorista, Veiculo, Pedido, Entrega, Cotacao, Ocorrencia
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    Session = None
    get_db = None

router = APIRouter(prefix="/api", tags=["Database API"])


# ========================================
# Clientes
# ========================================

@router.get("/clientes")
def listar_clientes(
    skip: int = 0,
    limit: int = 100,
    ativo: bool = True,
    db: Session = Depends(get_db) if SQLALCHEMY_AVAILABLE else None
):
    """Lista clientes do banco de dados"""
    if not SQLALCHEMY_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Database API não disponível. SQLAlchemy não está instalado."
        )
    query = db.query(Cliente).filter(Cliente.ativo == ativo)
    total = query.count()
    clientes = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": [_cliente_to_dict(c) for c in clientes],
        "total": total
    }


@router.get("/clientes/{cliente_id}")
def obter_cliente(cliente_id: str, db: Session = Depends(get_db)):
    """Obtém um cliente específico"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"success": True, "data": _cliente_to_dict(cliente)}


# ========================================
# Motoristas
# ========================================

@router.get("/motoristas")
def listar_motoristas(
    ativo: bool = True,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista motoristas do banco de dados"""
    query = db.query(Motorista).filter(Motorista.ativo == ativo)
    if status:
        query = query.filter(Motorista.status == status)
    
    motoristas = query.all()
    return {
        "success": True,
        "data": [_motorista_to_dict(m) for m in motoristas],
        "count": len(motoristas)
    }


@router.get("/motoristas/{motorista_id}")
def obter_motorista(motorista_id: str, db: Session = Depends(get_db)):
    """Obtém um motorista específico"""
    motorista = db.query(Motorista).filter(Motorista.id == motorista_id).first()
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return {"success": True, "data": _motorista_to_dict(motorista)}


@router.get("/motoristas/{motorista_id}/entregas")
def entregas_do_motorista(
    motorista_id: str,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista entregas de um motorista"""
    query = db.query(Entrega).filter(Entrega.motorista_id == motorista_id)
    if status:
        query = query.filter(Entrega.status == status)
    
    entregas = query.all()
    return {
        "success": True,
        "data": [_entrega_to_dict(e) for e in entregas],
        "count": len(entregas)
    }


# ========================================
# Veículos
# ========================================

@router.get("/veiculos")
def listar_veiculos(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista veículos do banco de dados"""
    query = db.query(Veiculo).filter(Veiculo.ativo == True)
    if status:
        query = query.filter(Veiculo.status == status)
    
    veiculos = query.all()
    return {
        "success": True,
        "data": [_veiculo_to_dict(v) for v in veiculos],
        "count": len(veiculos)
    }


# ========================================
# Pedidos
# ========================================

@router.get("/pedidos")
def listar_pedidos(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista pedidos do banco de dados"""
    query = db.query(Pedido)
    if status:
        query = query.filter(Pedido.status == status)
    
    total = query.count()
    pedidos = query.order_by(Pedido.criado_em.desc()).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "data": [_pedido_to_dict(p, db) for p in pedidos],
        "total": total
    }


@router.get("/pedidos/{pedido_id}")
def obter_pedido(pedido_id: str, db: Session = Depends(get_db)):
    """Obtém um pedido específico"""
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"success": True, "data": _pedido_to_dict(pedido, db)}


# ========================================
# Entregas
# ========================================

@router.get("/entregas")
def listar_entregas(
    status: Optional[str] = None,
    motorista_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista entregas do banco de dados"""
    query = db.query(Entrega)
    if status:
        query = query.filter(Entrega.status == status)
    if motorista_id:
        query = query.filter(Entrega.motorista_id == motorista_id)
    
    entregas = query.order_by(Entrega.criado_em.desc()).all()
    return {
        "success": True,
        "data": [_entrega_to_dict(e) for e in entregas],
        "count": len(entregas)
    }


@router.get("/entregas/{entrega_id}")
def obter_entrega(entrega_id: str, db: Session = Depends(get_db)):
    """Obtém uma entrega específica"""
    entrega = db.query(Entrega).filter(Entrega.id == entrega_id).first()
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return {"success": True, "data": _entrega_to_dict(entrega)}


@router.get("/entregas/codigo/{codigo}")
def obter_entrega_por_codigo(codigo: str, db: Session = Depends(get_db)):
    """Obtém entrega pelo código - usado pelo Portal Cliente"""
    entrega = db.query(Entrega).filter(Entrega.codigo == codigo.upper()).first()
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return {"success": True, "data": _entrega_to_dict(entrega)}


@router.patch("/entregas/{entrega_id}/status")
def atualizar_status_entrega(
    entrega_id: str,
    novo_status: str,
    observacao: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Atualiza status de entrega"""
    entrega = db.query(Entrega).filter(Entrega.id == entrega_id).first()
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    
    progresso_map = {
        "aguardando_coleta": 10,
        "coletado": 30,
        "em_transito": 60,
        "saiu_para_entrega": 85,
        "entregue": 100
    }
    
    entrega.status = novo_status
    entrega.progresso = progresso_map.get(novo_status, 50)
    entrega.atualizado_em = datetime.utcnow()
    
    if novo_status == "entregue":
        entrega.data_entrega = datetime.utcnow()
    
    if observacao:
        entrega.observacoes = observacao
    
    db.commit()
    db.refresh(entrega)
    
    return {
        "success": True,
        "data": _entrega_to_dict(entrega),
        "message": f"Status atualizado para {novo_status}"
    }


# ========================================
# Rastreamento (Portal Cliente)
# ========================================

@router.get("/rastreamento/{codigo}")
def rastrear_entrega(codigo: str, db: Session = Depends(get_db)):
    """Rastreia entrega pelo código - Portal Cliente"""
    entrega = db.query(Entrega).filter(Entrega.codigo == codigo.upper()).first()
    if not entrega:
        raise HTTPException(status_code=404, detail="Código não encontrado")
    
    # Buscar pedido relacionado
    pedido = db.query(Pedido).filter(Pedido.id == entrega.pedido_id).first()
    
    return {
        "success": True,
        "data": {
            "codigo": entrega.codigo,
            "status": entrega.status,
            "progresso": entrega.progresso,
            "previsao_entrega": entrega.previsao_entrega.isoformat() if entrega.previsao_entrega else None,
            "endereco_cidade": entrega.endereco_cidade,
            "endereco_uf": entrega.endereco_uf,
            "motorista_nome": None,
            "data_coleta": entrega.data_coleta.isoformat() if entrega.data_coleta else None,
            "data_entrega": entrega.data_entrega.isoformat() if entrega.data_entrega else None,
            "eventos": [
                {"data": entrega.criado_em.isoformat(), "descricao": "Pedido criado", "tipo": "info"},
                {"data": entrega.data_coleta.isoformat() if entrega.data_coleta else None, "descricao": "Mercadoria coletada", "tipo": "coleta"} if entrega.data_coleta else None,
                {"data": datetime.utcnow().isoformat(), "descricao": f"Status: {entrega.status.replace('_', ' ').title()}", "tipo": "status"},
            ]
        }
    }


# ========================================
# Cotações
# ========================================

@router.get("/cotacoes")
def listar_cotacoes(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista cotações do banco de dados"""
    query = db.query(Cotacao)
    if status:
        query = query.filter(Cotacao.status == status)
    
    cotacoes = query.order_by(Cotacao.criado_em.desc()).all()
    return {
        "success": True,
        "data": [_cotacao_to_dict(c, db) for c in cotacoes],
        "count": len(cotacoes)
    }


# ========================================
# Dashboard Stats
# ========================================

@router.get("/dashboard/stats")
def obter_stats_dashboard(db: Session = Depends(get_db)):
    """Estatísticas para o Dashboard"""
    
    # Entregas
    total_entregas = db.query(Entrega).count()
    entregas_transito = db.query(Entrega).filter(Entrega.status.in_(["em_transito", "saiu_para_entrega"])).count()
    entregas_entregues = db.query(Entrega).filter(Entrega.status == "entregue").count()
    entregas_atrasadas = db.query(Entrega).filter(Entrega.atrasada == True).count()
    
    # Pedidos
    total_pedidos = db.query(Pedido).count()
    pedidos_aguardando = db.query(Pedido).filter(Pedido.status == "aguardando").count()
    pedidos_transito = db.query(Pedido).filter(Pedido.status == "em_transito").count()
    pedidos_entregues = db.query(Pedido).filter(Pedido.status == "entregue").count()
    
    # Motoristas
    total_motoristas = db.query(Motorista).filter(Motorista.ativo == True).count()
    motoristas_disponiveis = db.query(Motorista).filter(Motorista.status == "disponivel").count()
    motoristas_rota = db.query(Motorista).filter(Motorista.status == "em_rota").count()
    
    # Veículos
    total_veiculos = db.query(Veiculo).filter(Veiculo.ativo == True).count()
    veiculos_disponiveis = db.query(Veiculo).filter(Veiculo.status == "disponivel").count()
    
    # Cotações
    total_cotacoes = db.query(Cotacao).count()
    cotacoes_pendentes = db.query(Cotacao).filter(Cotacao.status == "pendente").count()
    
    return {
        "success": True,
        "data": {
            "entregas": {
                "total": total_entregas,
                "em_transito": entregas_transito,
                "entregues_hoje": entregas_entregues,
                "atrasadas": entregas_atrasadas
            },
            "pedidos": {
                "total": total_pedidos,
                "aguardando": pedidos_aguardando,
                "em_transito": pedidos_transito,
                "entregues": pedidos_entregues
            },
            "motoristas": {
                "total": total_motoristas,
                "disponiveis": motoristas_disponiveis,
                "em_rota": motoristas_rota
            },
            "veiculos": {
                "total": total_veiculos,
                "disponiveis": veiculos_disponiveis
            },
            "cotacoes": {
                "total": total_cotacoes,
                "pendentes": cotacoes_pendentes
            }
        }
    }


# ========================================
# Helpers - Serialização
# ========================================

def _cliente_to_dict(c: Cliente) -> dict:
    return {
        "id": c.id,
        "razao_social": c.razao_social,
        "nome_fantasia": c.nome_fantasia,
        "cnpj": c.cnpj,
        "email": c.email,
        "telefone": c.telefone,
        "celular": c.celular,
        "endereco": c.endereco,
        "bairro": c.bairro,
        "cidade": c.cidade,
        "uf": c.uf,
        "cep": c.cep,
        "contato_nome": c.contato_nome,
        "ativo": c.ativo,
        "criado_em": c.criado_em.isoformat() if c.criado_em else None
    }


def _motorista_to_dict(m: Motorista) -> dict:
    return {
        "id": m.id,
        "nome": m.nome,
        "cpf": m.cpf,
        "telefone": m.telefone,
        "email": m.email,
        "cnh_numero": m.cnh_numero,
        "cnh_categoria": m.cnh_categoria,
        "cnh_validade": m.cnh_validade,
        "status": m.status,
        "veiculo_id": m.veiculo_id,
        "entregas_hoje": m.entregas_hoje,
        "avaliacao": m.avaliacao,
        "ativo": m.ativo,
        "criado_em": m.criado_em.isoformat() if m.criado_em else None
    }


def _veiculo_to_dict(v: Veiculo) -> dict:
    return {
        "id": v.id,
        "placa": v.placa,
        "tipo": v.tipo,
        "marca": v.marca,
        "modelo": v.modelo,
        "ano": v.ano,
        "capacidade_kg": v.capacidade_kg,
        "capacidade_m3": v.capacidade_m3,
        "status": v.status,
        "km_atual": v.km_atual,
        "ativo": v.ativo
    }


def _pedido_to_dict(p: Pedido, db: Session) -> dict:
    cliente = db.query(Cliente).filter(Cliente.id == p.cliente_id).first()
    motorista = db.query(Motorista).filter(Motorista.id == p.motorista_id).first() if p.motorista_id else None
    
    return {
        "id": p.id,
        "numero": p.numero,
        "cliente_id": p.cliente_id,
        "cliente_nome": cliente.nome_fantasia if cliente else None,
        "motorista_id": p.motorista_id,
        "motorista_nome": motorista.nome if motorista else None,
        "origem_endereco": p.origem_endereco,
        "origem_cidade": p.origem_cidade,
        "origem_uf": p.origem_uf,
        "destino_endereco": p.destino_endereco,
        "destino_cidade": p.destino_cidade,
        "destino_uf": p.destino_uf,
        "peso_kg": p.peso_kg,
        "volumes": p.volumes,
        "valor_mercadoria": p.valor_mercadoria,
        "valor_frete": p.valor_frete,
        "status": p.status,
        "sla_status": p.sla_status,
        "previsao_entrega": p.previsao_entrega.isoformat() if p.previsao_entrega else None,
        "criado_em": p.criado_em.isoformat() if p.criado_em else None
    }


def _entrega_to_dict(e: Entrega) -> dict:
    return {
        "id": e.id,
        "codigo": e.codigo,
        "pedido_id": e.pedido_id,
        "motorista_id": e.motorista_id,
        "cliente_nome": e.cliente_nome,
        "cliente_telefone": e.cliente_telefone,
        "endereco_rua": e.endereco_rua,
        "endereco_bairro": e.endereco_bairro,
        "endereco_cidade": e.endereco_cidade,
        "endereco_uf": e.endereco_uf,
        "endereco_cep": e.endereco_cep,
        "latitude": e.latitude,
        "longitude": e.longitude,
        "volumes": e.volumes,
        "peso": e.peso,
        "valor_mercadoria": e.valor_mercadoria,
        "valor_frete": e.valor_frete,
        "status": e.status,
        "progresso": e.progresso,
        "previsao_entrega": e.previsao_entrega.isoformat() if e.previsao_entrega else None,
        "data_coleta": e.data_coleta.isoformat() if e.data_coleta else None,
        "data_entrega": e.data_entrega.isoformat() if e.data_entrega else None,
        "atrasada": e.atrasada,
        "criado_em": e.criado_em.isoformat() if e.criado_em else None
    }


def _cotacao_to_dict(c: Cotacao, db: Session) -> dict:
    cliente = db.query(Cliente).filter(Cliente.id == c.cliente_id).first()
    
    return {
        "id": c.id,
        "numero": c.numero,
        "cliente_id": c.cliente_id,
        "cliente_nome": cliente.nome_fantasia if cliente else None,
        "origem_cidade": c.origem_cidade,
        "origem_uf": c.origem_uf,
        "destino_cidade": c.destino_cidade,
        "destino_uf": c.destino_uf,
        "peso_kg": c.peso_kg,
        "valor_mercadoria": c.valor_mercadoria,
        "valor_frete": c.valor_frete,
        "prazo_dias": c.prazo_dias,
        "status": c.status,
        "validade": c.validade.isoformat() if c.validade else None,
        "criado_em": c.criado_em.isoformat() if c.criado_em else None
    }
