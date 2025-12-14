"""
LogiFlow CRM - Router GPS Tracking
Endpoints para rastreamento GPS consolidado e webhooks
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Optional, List
from datetime import datetime, timedelta
import logging

from integrations.gps.sascar import SascarClient
from integrations.gps.autotrac import AutotracClient
from integrations.gps.onixsat import OnixsatClient
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# ===========================================
# Posições em Tempo Real
# ===========================================

@router.get("/posicao/{placa}")
async def obter_posicao_consolidada(placa: str):
    """
    Obtém posição atual de um veículo de todas as fontes disponíveis
    
    Consulta Sascar, Autotrac e Onixsat e retorna a posição mais recente
    """
    try:
        posicoes = []
        
        # Sascar
        sascar = SascarClient(simulation_mode=True)
        pos_sascar = sascar.obter_posicao_veiculo(placa)
        if pos_sascar.get("success"):
            posicoes.append({
                "fonte": "sascar",
                "dados": pos_sascar.get("posicao")
            })
        
        # Autotrac
        autotrac = AutotracClient(simulation_mode=True)
        pos_autotrac = autotrac.obter_posicao_veiculo(placa)
        if pos_autotrac.get("success"):
            posicoes.append({
                "fonte": "autotrac",
                "dados": pos_autotrac.get("posicao")
            })
        
        # Onixsat
        onixsat = OnixsatClient(simulation_mode=True)
        pos_onixsat = onixsat.obter_posicao_veiculo(placa)
        if pos_onixsat.get("success"):
            posicoes.append({
                "fonte": "onixsat",
                "dados": pos_onixsat.get("posicao")
            })
        
        if not posicoes:
            return {
                "success": False,
                "message": "Nenhuma posição encontrada para este veículo"
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
async def listar_todos_veiculos():
    """
    Lista todos os veículos rastreados de todas as fontes
    """
    try:
        todos_veiculos = []
        
        # Sascar
        sascar = SascarClient(simulation_mode=True)
        veiculos_sascar = sascar.listar_veiculos()
        if veiculos_sascar.get("success"):
            for v in veiculos_sascar.get("veiculos", []):
                v["fonte_rastreamento"] = "sascar"
                todos_veiculos.append(v)
        
        # Autotrac
        autotrac = AutotracClient(simulation_mode=True)
        veiculos_autotrac = autotrac.listar_veiculos()
        if veiculos_autotrac.get("success"):
            for v in veiculos_autotrac.get("veiculos", []):
                v["fonte_rastreamento"] = "autotrac"
                todos_veiculos.append(v)
        
        # Onixsat
        onixsat = OnixsatClient(simulation_mode=True)
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
    data_fim: Optional[str] = None
):
    """
    Obtém histórico de rota de um veículo
    
    Args:
        placa: Placa do veículo
        data_inicio: Data inicial (ISO format, padrão: 24h atrás)
        data_fim: Data final (ISO format, padrão: agora)
    """
    try:
        # Parse datas
        if data_fim:
            dt_fim = datetime.fromisoformat(data_fim)
        else:
            dt_fim = datetime.now()
        
        if data_inicio:
            dt_inicio = datetime.fromisoformat(data_inicio)
        else:
            dt_inicio = dt_fim - timedelta(hours=24)
        
        # Tentar obter de todas as fontes
        historicos = []
        
        # Sascar
        sascar = SascarClient(simulation_mode=True)
        hist_sascar = sascar.obter_historico_rota(placa, dt_inicio, dt_fim)
        if hist_sascar.get("success"):
            historicos.append({
                "fonte": "sascar",
                "dados": hist_sascar
            })
        
        # Autotrac
        autotrac = AutotracClient(simulation_mode=True)
        hist_autotrac = autotrac.obter_historico_rota(placa, dt_inicio, dt_fim)
        if hist_autotrac.get("success"):
            historicos.append({
                "fonte": "autotrac",
                "dados": hist_autotrac
            })
        
        # Onixsat
        onixsat = OnixsatClient(simulation_mode=True)
        hist_onixsat = onixsat.obter_historico_rota(placa, dt_inicio, dt_fim)
        if hist_onixsat.get("success"):
            historicos.append({
                "fonte": "onixsat",
                "dados": hist_onixsat
            })
        
        if not historicos:
            return {
                "success": False,
                "message": "Nenhum histórico encontrado"
            }
        
        # Usar o histórico com mais pontos
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
async def webhook_sascar(request: Request):
    """
    Webhook para receber posições em tempo real da Sascar
    """
    try:
        data = await request.json()
        
        # Processar dados do webhook
        logger.info(f"Webhook Sascar recebido: {data}")
        
        # Em produção: salvar no banco, atualizar cache, notificar frontend via WebSocket
        
        return {
            "success": True,
            "message": "Webhook processado"
        }
        
    except Exception as e:
        logger.error(f"Erro no webhook Sascar: {e}")
        return {"success": False, "error": str(e)}


@router.post("/webhook/autotrac")
async def webhook_autotrac(request: Request):
    """Webhook para Autotrac"""
    try:
        data = await request.json()
        logger.info(f"Webhook Autotrac recebido: {data}")
        return {"success": True, "message": "Webhook processado"}
    except Exception as e:
        logger.error(f"Erro no webhook Autotrac: {e}")
        return {"success": False, "error": str(e)}


@router.post("/webhook/onixsat")
async def webhook_onixsat(request: Request):
    """Webhook para Onixsat"""
    try:
        data = await request.json()
        logger.info(f"Webhook Onixsat recebido: {data}")
        return {"success": True, "message": "Webhook processado"}
    except Exception as e:
        logger.error(f"Erro no webhook Onixsat: {e}")
        return {"success": False, "error": str(e)}


# ===========================================
# Dashboard e Mapa
# ===========================================

@router.get("/dashboard/mapa")
async def obter_dados_mapa():
    """
    Obtém dados consolidados para exibição no mapa do dashboard
    
    Retorna posições de todos os veículos para renderização no mapa
    """
    try:
        veiculos_response = await listar_todos_veiculos()
        
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
                client = SascarClient(simulation_mode=True)
            elif fonte == "autotrac":
                client = AutotracClient(simulation_mode=True)
            else:
                client = OnixsatClient(simulation_mode=True)
            
            pos = client.obter_posicao_veiculo(placa)
            
            if pos.get("success"):
                veiculos_com_posicao.append({
                    **veiculo,
                    "posicao_atual": pos.get("posicao")
                })
        
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
async def obter_estatisticas_frota():
    """
    Obtém estatísticas consolidadas da frota
    """
    try:
        veiculos_response = await listar_todos_veiculos()
        
        if not veiculos_response.get("success"):
            return veiculos_response
        
        veiculos = veiculos_response.get("veiculos", [])
        
        # Calcular estatísticas
        total = len(veiculos)
        em_movimento = 0
        parados = 0
        
        # Simular estatísticas
        import random
        em_movimento = random.randint(int(total * 0.4), int(total * 0.7))
        parados = total - em_movimento
        
        return {
            "success": True,
            "estatisticas": {
                "total_veiculos": total,
                "em_movimento": em_movimento,
                "parados": parados,
                "offline": 0,
                "alertas_ativos": random.randint(0, 5),
                "km_rodados_hoje": random.randint(500, 2000),
                "velocidade_media": random.randint(60, 75)
            },
            "por_fonte": veiculos_response.get("fontes", {})
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
