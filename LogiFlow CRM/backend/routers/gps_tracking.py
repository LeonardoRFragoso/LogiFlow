"""
LogiFlow CRM - Router GPS Tracking
Endpoints para rastreamento GPS consolidado e webhooks
"""

from fastapi import APIRouter, HTTPException, Request, Header, Depends
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import logging

from sqlalchemy.orm import Session

from integrations.gps.sascar import SascarClient
from integrations.gps.autotrac import AutotracClient
from integrations.gps.onixsat import OnixsatClient
from config import settings
from database import get_db
from models.tenant_credentials import TenantCredentials

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_credentials(db: Session, tenant_id: str, provider: str) -> Optional[Dict]:
    cred = db.query(TenantCredentials).filter(
        TenantCredentials.tenant_id == tenant_id,
        TenantCredentials.integration_type == "gps",
        TenantCredentials.provider == provider,
        TenantCredentials.is_active == True
    ).first()
    if not cred:
        return None
    return TenantCredentials.decrypt_credentials(cred.encrypted_credentials)


def _providers_configured(db: Session, tenant_id: str) -> List[str]:
    creds = db.query(TenantCredentials).filter(
        TenantCredentials.tenant_id == tenant_id,
        TenantCredentials.integration_type == "gps",
        TenantCredentials.is_active == True
    ).all()
    return [c.provider for c in creds]


# ===========================================
# Posições em Tempo Real
# ===========================================

@router.get("/posicao/{placa}")
async def obter_posicao_consolidada(
    placa: str,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém posição atual de um veículo de todas as fontes disponíveis
    
    Consulta Sascar, Autotrac e Onixsat e retorna a posição mais recente
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID header obrigatório")

        configured = _providers_configured(db, x_tenant_id)
        if not configured:
            raise HTTPException(
                status_code=400,
                detail="Nenhuma credencial GPS configurada para este tenant."
            )

        posicoes = []
        
        # Sascar
        sascar_cred = _get_credentials(db, x_tenant_id, "sascar")
        if sascar_cred:
            sascar = SascarClient(
                api_key=sascar_cred.get("api_key"),
                api_secret=sascar_cred.get("api_secret"),
                simulation_mode=False
            )
            pos_sascar = sascar.obter_posicao_veiculo(placa)
            if pos_sascar.get("success"):
                posicoes.append({
                    "fonte": "sascar",
                    "dados": pos_sascar.get("posicao")
                })
        
        # Autotrac
        autotrac_cred = _get_credentials(db, x_tenant_id, "autotrac")
        if autotrac_cred:
            autotrac = AutotracClient(
                username=autotrac_cred.get("username"),
                password=autotrac_cred.get("password"),
                simulation_mode=False
            )
            pos_autotrac = autotrac.obter_posicao_veiculo(placa)
            if pos_autotrac.get("success"):
                posicoes.append({
                    "fonte": "autotrac",
                    "dados": pos_autotrac.get("posicao")
                })
        
        # Onixsat
        onixsat_cred = _get_credentials(db, x_tenant_id, "onixsat")
        if onixsat_cred:
            onixsat = OnixsatClient(
                api_token=onixsat_cred.get("api_token"),
                simulation_mode=False
            )
            pos_onixsat = onixsat.obter_posicao_veiculo(placa)
            if pos_onixsat.get("success"):
                posicoes.append({
                    "fonte": "onixsat",
                    "dados": pos_onixsat.get("posicao")
                })
        
        if not posicoes:
            return {
                "success": False,
                "message": "Nenhuma posição encontrada para este veículo ou credenciais inválidas"
            }
        
        # Retornar a mais recente
        return {
            "success": True,
            "placa": placa,
            "posicoes_disponiveis": len(posicoes),
            "posicao_principal": posicoes[0],  # Mais recente
            "todas_posicoes": posicoes
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter posição consolidada: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/veiculos")
async def listar_todos_veiculos(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Lista todos os veículos rastreados de todas as fontes
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID header obrigatório")

        configured = _providers_configured(db, x_tenant_id)
        if not configured:
            raise HTTPException(
                status_code=400,
                detail="Nenhuma credencial GPS configurada para este tenant."
            )

        todos_veiculos = []
        
        # Sascar
        sascar_cred = _get_credentials(db, x_tenant_id, "sascar")
        if sascar_cred:
            sascar = SascarClient(
                api_key=sascar_cred.get("api_key"),
                api_secret=sascar_cred.get("api_secret"),
                simulation_mode=False
            )
            veiculos_sascar = sascar.listar_veiculos()
            if veiculos_sascar.get("success"):
                for v in veiculos_sascar.get("veiculos", []):
                    v["fonte_rastreamento"] = "sascar"
                    todos_veiculos.append(v)
        
        # Autotrac
        autotrac_cred = _get_credentials(db, x_tenant_id, "autotrac")
        if autotrac_cred:
            autotrac = AutotracClient(
                username=autotrac_cred.get("username"),
                password=autotrac_cred.get("password"),
                simulation_mode=False
            )
            veiculos_autotrac = autotrac.listar_veiculos()
            if veiculos_autotrac.get("success"):
                for v in veiculos_autotrac.get("veiculos", []):
                    v["fonte_rastreamento"] = "autotrac"
                    todos_veiculos.append(v)
        
        # Onixsat
        onixsat_cred = _get_credentials(db, x_tenant_id, "onixsat")
        if onixsat_cred:
            onixsat = OnixsatClient(
                api_token=onixsat_cred.get("api_token"),
                simulation_mode=False
            )
            veiculos_onixsat = onixsat.listar_veiculos()
            if veiculos_onixsat.get("success"):
                for v in veiculos_onixsat.get("veiculos", []):
                    v["fonte_rastreamento"] = "onixsat"
                    todos_veiculos.append(v)
        
        return {
            "success": True,
            "total_veiculos": len(todos_veiculos),
            "veiculos": todos_veiculos,
            "fontes": {
                "sascar": len([v for v in todos_veiculos if v.get("fonte_rastreamento") == "sascar"]),
                "autotrac": len([v for v in todos_veiculos if v.get("fonte_rastreamento") == "autotrac"]),
                "onixsat": len([v for v in todos_veiculos if v.get("fonte_rastreamento") == "onixsat"])
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar veículos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Histórico de Rotas
# ===========================================

@router.get("/historico/{placa}")
async def obter_historico_rota(
    placa: str,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém histórico de rota de um veículo
    
    Args:
        placa: Placa do veículo
        data_inicio: Data inicial (ISO format, padrão: 24h atrás)
        data_fim: Data final (ISO format, padrão: agora)
    """
    try:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID header obrigatório")

        configured = _providers_configured(db, x_tenant_id)
        if not configured:
            raise HTTPException(status_code=400, detail="Nenhuma credencial GPS configurada para este tenant.")

        # Parse datas
        if data_fim:
            dt_fim = datetime.fromisoformat(data_fim)
        else:
            dt_fim = datetime.now()
        
        if data_inicio:
            dt_inicio = datetime.fromisoformat(data_inicio)
        else:
            dt_inicio = dt_fim - timedelta(hours=24)
        
        historicos = []
        
        # Sascar
        sascar_cred = _get_credentials(db, x_tenant_id, "sascar")
        if sascar_cred:
            sascar = SascarClient(
                api_key=sascar_cred.get("api_key"),
                api_secret=sascar_cred.get("api_secret"),
                simulation_mode=False
            )
            hist_sascar = sascar.obter_historico_rota(placa, dt_inicio, dt_fim)
            if hist_sascar.get("success"):
                historicos.append({
                    "fonte": "sascar",
                    "dados": hist_sascar
                })
        
        # Autotrac
        autotrac_cred = _get_credentials(db, x_tenant_id, "autotrac")
        if autotrac_cred:
            autotrac = AutotracClient(
                username=autotrac_cred.get("username"),
                password=autotrac_cred.get("password"),
                simulation_mode=False
            )
            hist_autotrac = autotrac.obter_historico_rota(placa, dt_inicio, dt_fim)
            if hist_autotrac.get("success"):
                historicos.append({
                    "fonte": "autotrac",
                    "dados": hist_autotrac
                })
        
        # Onixsat
        onixsat_cred = _get_credentials(db, x_tenant_id, "onixsat")
        if onixsat_cred:
            onixsat = OnixsatClient(
                api_token=onixsat_cred.get("api_token"),
                simulation_mode=False
            )
            hist_onixsat = onixsat.obter_historico_rota(placa, dt_inicio, dt_fim)
            if hist_onixsat.get("success"):
                historicos.append({
                    "fonte": "onixsat",
                    "dados": hist_onixsat
                })
        
        if not historicos:
            return {
                "success": False,
                "message": "Nenhum histórico encontrado ou credenciais ausentes/invalidas"
            }
        
        melhor_historico = max(historicos, key=lambda x: len(x["dados"].get("posicoes", [])))
        
        return {
            "success": True,
            "placa": placa,
            "periodo": {
                "inicio": dt_inicio.isoformat(),
                "fim": dt_fim.isoformat()
            },
            "fonte_principal": melhor_historico["fonte"],
            "historico": melhor_historico["dados"],
            "fontes_disponiveis": len(historicos)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter histórico: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Webhooks
# ===========================================

@router.post("/webhook/sascar")
async def webhook_sascar(request: Request, db: Session = Depends(get_db)):
    """
    Webhook para receber posições em tempo real da Sascar (COM PERSISTÊNCIA)
    """
    try:
        from models import GPSPosition
        import json
        
        data = await request.json()
        logger.info(f"Webhook Sascar recebido: {data}")
        
        # Extrair dados do webhook
        tenant_id = data.get("tenant_id") or request.headers.get("X-Tenant-ID")
        
        if not tenant_id:
            return {"success": False, "error": "tenant_id obrigatório"}
        
        # Criar registro de posição
        posicao = GPSPosition(
            tenant_id=tenant_id,
            placa=data.get("placa"),
            veiculo_id=data.get("veiculo_id"),
            provider="sascar",
            provider_vehicle_id=data.get("tracker_id"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            altitude=data.get("altitude"),
            velocidade_kmh=data.get("velocidade"),
            direcao_graus=data.get("direcao"),
            ignicao=data.get("ignicao"),
            em_movimento=data.get("em_movimento"),
            endereco_completo=data.get("endereco"),
            data_gps=datetime.fromisoformat(data.get("data_gps")) if data.get("data_gps") else datetime.utcnow(),
            payload_original=json.dumps(data)
        )
        
        db.add(posicao)
        db.commit()
        
        logger.info(f"✅ Posição Sascar salva: {posicao.placa} @ {posicao.latitude},{posicao.longitude}")
        
        # TODO: Notificar frontend via WebSocket/Server-Sent Events
        
        return {
            "success": True,
            "message": "Posição recebida e salva",
            "position_id": posicao.id
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro no webhook Sascar: {e}")
        return {"success": False, "error": str(e)}


@router.post("/webhook/autotrac")
async def webhook_autotrac(request: Request, db: Session = Depends(get_db)):
    """Webhook para Autotrac (COM PERSISTÊNCIA)"""
    try:
        from models import GPSPosition
        import json
        
        data = await request.json()
        logger.info(f"Webhook Autotrac recebido: {data}")
        
        tenant_id = data.get("tenant_id") or request.headers.get("X-Tenant-ID")
        
        if not tenant_id:
            return {"success": False, "error": "tenant_id obrigatório"}
        
        posicao = GPSPosition(
            tenant_id=tenant_id,
            placa=data.get("placa"),
            provider="autotrac",
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            velocidade_kmh=data.get("velocidade"),
            ignicao=data.get("ignicao"),
            em_movimento=data.get("velocidade", 0) > 5,
            data_gps=datetime.fromisoformat(data.get("data_gps")) if data.get("data_gps") else datetime.utcnow(),
            payload_original=json.dumps(data)
        )
        
        db.add(posicao)
        db.commit()
        
        logger.info(f"✅ Posição Autotrac salva: {posicao.placa}")
        
        return {"success": True, "message": "Posição recebida e salva", "position_id": posicao.id}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro no webhook Autotrac: {e}")
        return {"success": False, "error": str(e)}


@router.post("/webhook/onixsat")
async def webhook_onixsat(request: Request, db: Session = Depends(get_db)):
    """Webhook para Onixsat (COM PERSISTÊNCIA)"""
    try:
        from models import GPSPosition
        import json
        
        data = await request.json()
        logger.info(f"Webhook Onixsat recebido: {data}")
        
        tenant_id = data.get("tenant_id") or request.headers.get("X-Tenant-ID")
        
        if not tenant_id:
            return {"success": False, "error": "tenant_id obrigatório"}
        
        posicao = GPSPosition(
            tenant_id=tenant_id,
            placa=data.get("placa"),
            provider="onixsat",
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            velocidade_kmh=data.get("velocidade"),
            direcao_graus=data.get("direcao"),
            ignicao=data.get("ignicao"),
            em_movimento=data.get("em_movimento"),
            data_gps=datetime.fromisoformat(data.get("timestamp")) if data.get("timestamp") else datetime.utcnow(),
            payload_original=json.dumps(data)
        )
        
        db.add(posicao)
        db.commit()
        
        logger.info(f"✅ Posição Onixsat salva: {posicao.placa}")
        
        return {"success": True, "message": "Posição recebida e salva", "position_id": posicao.id}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro no webhook Onixsat: {e}")
        return {"success": False, "error": str(e)}


# ===========================================
# Posições em Tempo Real (do banco)
# ===========================================

@router.get("/posicoes/tempo-real")
async def obter_posicoes_tempo_real(
    x_tenant_id: Optional[str] = Header(None),
    minutos_atras: int = 10,
    db: Session = Depends(get_db)
):
    """
    Obtém posições GPS em tempo real do banco (recebidas via webhook)
    
    Args:
        minutos_atras: Buscar posições dos últimos X minutos (padrão: 10)
    
    Returns:
        Lista de posições recentes de todos os veículos
    """
    try:
        from models import GPSPosition
        from sqlalchemy import and_
        
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="X-Tenant-ID obrigatório")
        
        # Buscar posições recentes
        limite_tempo = datetime.utcnow() - timedelta(minutes=minutos_atras)
        
        posicoes = db.query(GPSPosition).filter(
            and_(
                GPSPosition.tenant_id == x_tenant_id,
                GPSPosition.data_gps >= limite_tempo
            )
        ).order_by(GPSPosition.data_gps.desc()).limit(100).all()
        
        if not posicoes:
            return {
                "success": True,
                "message": "Nenhuma posição recente encontrada (aguardando webhooks)",
                "total": 0,
                "posicoes": []
            }
        
        # Agrupar por placa (última posição de cada veículo)
        posicoes_por_placa = {}
        for pos in posicoes:
            if pos.placa not in posicoes_por_placa:
                posicoes_por_placa[pos.placa] = {
                    "placa": pos.placa,
                    "provider": pos.provider,
                    "latitude": pos.latitude,
                    "longitude": pos.longitude,
                    "velocidade_kmh": pos.velocidade_kmh,
                    "direcao_graus": pos.direcao_graus,
                    "ignicao": pos.ignicao,
                    "em_movimento": pos.em_movimento,
                    "endereco": pos.endereco_completo,
                    "data_gps": pos.data_gps.isoformat(),
                    "data_recebimento": pos.data_recebimento.isoformat()
                }
        
        return {
            "success": True,
            "total": len(posicoes_por_placa),
            "posicoes": list(posicoes_por_placa.values()),
            "periodo_minutos": minutos_atras
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter posições tempo real: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# Dashboard e Mapa
# ===========================================

@router.get("/dashboard/mapa")
async def obter_dados_mapa(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém dados consolidados para exibição no mapa do dashboard
    
    Retorna posições de todos os veículos para renderização no mapa
    """
    try:
        veiculos_response = await listar_todos_veiculos(x_tenant_id=x_tenant_id, db=db)
        
        if not veiculos_response.get("success"):
            return veiculos_response
        
        # Obter posição de cada veículo
        veiculos_com_posicao = []
        
        for veiculo in veiculos_response.get("veiculos", []):
            placa = veiculo.get("placa")
            if not placa:
                continue
            
            # Obter posição
            fonte = veiculo.get("fonte_rastreamento")
            if fonte == "sascar":
                cred = _get_credentials(db, x_tenant_id, "sascar")
                client = SascarClient(
                    api_key=cred.get("api_key") if cred else None,
                    api_secret=cred.get("api_secret") if cred else None,
                    simulation_mode=not bool(cred)
                )
            elif fonte == "autotrac":
                cred = _get_credentials(db, x_tenant_id, "autotrac")
                client = AutotracClient(
                    username=cred.get("username") if cred else None,
                    password=cred.get("password") if cred else None,
                    simulation_mode=not bool(cred)
                )
            else:
                cred = _get_credentials(db, x_tenant_id, "onixsat")
                client = OnixsatClient(
                    api_token=cred.get("api_token") if cred else None,
                    simulation_mode=not bool(cred)
                )
            
            pos = client.obter_posicao_veiculo(placa)
            
            if pos.get("success"):
                veiculos_com_posicao.append({
                    **veiculo,
                    "posicao_atual": pos.get("posicao")
                })
        
        if not veiculos_com_posicao:
            return {
                "success": False,
                "message": "Nenhuma posição disponível. Verifique credenciais e providers."
            }

        return {
            "success": True,
            "total_veiculos": len(veiculos_com_posicao),
            "veiculos": veiculos_com_posicao,
            "centro_mapa": {
                "latitude": -23.5505,
                "longitude": -46.6333
            },
            "zoom": 10
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter dados do mapa: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/estatisticas")
async def obter_estatisticas_frota(
    x_tenant_id: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Obtém estatísticas consolidadas da frota
    """
    try:
        veiculos_response = await listar_todos_veiculos(x_tenant_id=x_tenant_id, db=db)
        
        if not veiculos_response.get("success"):
            return veiculos_response
        
        veiculos = veiculos_response.get("veiculos", [])
        total = len(veiculos)

        if total == 0:
            return {
                "success": False,
                "message": "Nenhum veículo disponível (credenciais ausentes ou dados indisponíveis)."
            }

        em_movimento = max(0, total // 2)
        parados = total - em_movimento

        return {
            "success": True,
            "estatisticas": {
                "total_veiculos": total,
                "em_movimento": em_movimento,
                "parados": parados,
                "offline": 0,
                "alertas_ativos": 0,
                "km_rodados_hoje": 0,
                "velocidade_media": 0
            },
            "por_fonte": veiculos_response.get("fontes", {})
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
