# LogiFlow CRM - Router Google Maps
# Endpoints para geocodificação, rotas e rastreamento

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from datetime import datetime
from loguru import logger

import sys
sys.path.append('..')
from services.maps_service import maps_service

router = APIRouter()


# ===========================================
# Schemas
# ===========================================

class EnderecoGeocode(BaseModel):
    endereco: str = Field(..., description="Endereço completo para geocodificar")


class CoordenadasReverso(BaseModel):
    latitude: float
    longitude: float


class CalcularRota(BaseModel):
    origem: str = Field(..., description="Endereço ou coordenadas de origem")
    destino: str = Field(..., description="Endereço ou coordenadas de destino")
    paradas: Optional[List[str]] = Field(default=None, description="Paradas intermediárias")
    evitar: Optional[List[str]] = Field(default=None, description="Evitar: tolls, highways, ferries")


class CalcularDistancia(BaseModel):
    origem: str
    destino: str


class MatrizDistancias(BaseModel):
    origens: List[str] = Field(..., description="Lista de endereços de origem")
    destinos: List[str] = Field(..., description="Lista de endereços de destino")


class CalcularETA(BaseModel):
    latitude: float = Field(..., description="Latitude atual do motorista")
    longitude: float = Field(..., description="Longitude atual do motorista")
    destino: str = Field(..., description="Endereço de destino")


class OtimizarRota(BaseModel):
    origem: str = Field(..., description="Ponto de partida")
    destinos: List[str] = Field(..., description="Lista de destinos a visitar")
    retornar_origem: bool = Field(default=False, description="Retornar ao ponto de partida")


# ===========================================
# Endpoints - Geocodificação
# ===========================================

@router.post("/geocode")
async def geocodificar_endereco(dados: EnderecoGeocode):
    """
    Converte endereço em coordenadas (latitude/longitude)
    
    Exemplo: "Av. Paulista, 1000, São Paulo, SP"
    """
    resultado = await maps_service.geocodificar(dados.endereco)
    
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado.get("error", "Erro na geocodificação"))
    
    return {
        "success": True,
        "data": resultado,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/geocode/reverso")
async def geocodificar_reverso(dados: CoordenadasReverso):
    """
    Converte coordenadas em endereço
    """
    resultado = await maps_service.geocodificar_reverso(dados.latitude, dados.longitude)
    
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado.get("error", "Erro na geocodificação reversa"))
    
    return {
        "success": True,
        "data": resultado,
        "timestamp": datetime.now().isoformat()
    }


# ===========================================
# Endpoints - Rotas e Distâncias
# ===========================================

@router.post("/rota")
async def calcular_rota(dados: CalcularRota):
    """
    Calcula rota entre origem e destino com paradas opcionais
    
    Retorna:
    - Distância total
    - Tempo estimado
    - Instruções de navegação
    - Polyline para desenhar no mapa
    """
    resultado = await maps_service.calcular_rota(
        origem=dados.origem,
        destino=dados.destino,
        waypoints=dados.paradas,
        evitar=dados.evitar
    )
    
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado.get("error", "Erro ao calcular rota"))
    
    return {
        "success": True,
        "data": resultado,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/distancia")
async def calcular_distancia(dados: CalcularDistancia):
    """
    Calcula distância e tempo entre dois pontos (simplificado)
    """
    resultado = await maps_service.calcular_distancia(dados.origem, dados.destino)
    
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado.get("error", "Erro ao calcular distância"))
    
    return {
        "success": True,
        "data": resultado,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/matriz")
async def matriz_distancias(dados: MatrizDistancias):
    """
    Calcula matriz de distâncias entre múltiplas origens e destinos
    
    Útil para:
    - Otimização de rotas
    - Escolha do motorista mais próximo
    - Planejamento de entregas
    """
    if len(dados.origens) > 10 or len(dados.destinos) > 10:
        raise HTTPException(
            status_code=400, 
            detail="Máximo de 10 origens e 10 destinos por requisição"
        )
    
    resultado = await maps_service.matriz_distancias(dados.origens, dados.destinos)
    
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado.get("error", "Erro na matriz de distâncias"))
    
    return {
        "success": True,
        "data": resultado,
        "timestamp": datetime.now().isoformat()
    }


# ===========================================
# Endpoints - ETA e Rastreamento
# ===========================================

@router.post("/eta")
async def calcular_eta(dados: CalcularETA):
    """
    Calcula ETA (Estimated Time of Arrival) baseado na posição atual
    
    Retorna:
    - Distância restante
    - Tempo restante
    - Horário previsto de chegada
    """
    resultado = await maps_service.calcular_eta(
        posicao_atual=(dados.latitude, dados.longitude),
        destino=dados.destino
    )
    
    if not resultado.get("success"):
        raise HTTPException(status_code=400, detail=resultado.get("error", "Erro ao calcular ETA"))
    
    return {
        "success": True,
        "data": resultado,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/eta/{entrega_id}")
async def obter_eta_entrega(entrega_id: str):
    """
    Obtém ETA de uma entrega específica baseado na última posição do motorista
    """
    # Em produção, buscar dados do banco
    # Por enquanto, retorna dados simulados
    
    return {
        "success": True,
        "data": {
            "entrega_id": entrega_id,
            "motorista": "João Silva",
            "posicao_atual": {
                "latitude": -23.5505,
                "longitude": -46.6333,
                "atualizado_em": datetime.now().isoformat()
            },
            "destino": "Av. Brasil, 1500, Campinas, SP",
            "distancia_restante_km": 85.3,
            "tempo_restante_minutos": 72,
            "horario_chegada_previsto": "14:30",
            "status": "em_transito"
        },
        "timestamp": datetime.now().isoformat()
    }


# ===========================================
# Endpoints - Otimização de Rotas
# ===========================================

@router.post("/otimizar")
async def otimizar_rota(dados: OtimizarRota):
    """
    Otimiza a ordem de visita dos destinos para menor distância total
    
    Usa algoritmo do vizinho mais próximo (simplificado)
    Em produção, considerar usar OR-Tools do Google para otimização avançada
    """
    if len(dados.destinos) > 10:
        raise HTTPException(status_code=400, detail="Máximo de 10 destinos para otimização")
    
    # Calcula matriz de distâncias
    todos_pontos = [dados.origem] + dados.destinos
    matriz = await maps_service.matriz_distancias(todos_pontos, todos_pontos)
    
    if not matriz.get("success"):
        raise HTTPException(status_code=400, detail="Erro ao calcular matriz de distâncias")
    
    # Algoritmo do vizinho mais próximo
    visitados = [0]  # Começa pela origem
    nao_visitados = list(range(1, len(todos_pontos)))
    distancia_total = 0
    
    while nao_visitados:
        atual = visitados[-1]
        mais_proximo = None
        menor_dist = float('inf')
        
        for dest in nao_visitados:
            dist = matriz["matriz"][atual][dest].get("distancia_metros", float('inf'))
            if dist < menor_dist:
                menor_dist = dist
                mais_proximo = dest
        
        if mais_proximo is not None:
            visitados.append(mais_proximo)
            nao_visitados.remove(mais_proximo)
            distancia_total += menor_dist
    
    # Se deve retornar à origem
    if dados.retornar_origem:
        dist_retorno = matriz["matriz"][visitados[-1]][0].get("distancia_metros", 0)
        distancia_total += dist_retorno
        visitados.append(0)
    
    # Monta resultado
    rota_otimizada = [todos_pontos[i] for i in visitados]
    
    return {
        "success": True,
        "data": {
            "rota_original": [dados.origem] + dados.destinos,
            "rota_otimizada": rota_otimizada,
            "ordem_visita": visitados,
            "distancia_total_km": round(distancia_total / 1000, 1),
            "economia_estimada": "Calculada com base na ordem otimizada"
        },
        "timestamp": datetime.now().isoformat()
    }


# ===========================================
# Endpoints - Utilitários
# ===========================================

@router.get("/validar-endereco")
async def validar_endereco(endereco: str = Query(..., description="Endereço para validar")):
    """
    Valida se um endereço existe e retorna o endereço formatado
    """
    resultado = await maps_service.geocodificar(endereco)
    
    return {
        "success": resultado.get("success", False),
        "valido": resultado.get("success", False),
        "endereco_original": endereco,
        "endereco_formatado": resultado.get("endereco_formatado"),
        "componentes": resultado.get("componentes"),
        "coordenadas": {
            "latitude": resultado.get("latitude"),
            "longitude": resultado.get("longitude")
        } if resultado.get("success") else None
    }


@router.get("/cep/{cep}")
async def buscar_por_cep(cep: str):
    """
    Busca endereço por CEP
    """
    # Remove caracteres não numéricos
    cep_limpo = ''.join(filter(str.isdigit, cep))
    
    if len(cep_limpo) != 8:
        raise HTTPException(status_code=400, detail="CEP inválido. Deve ter 8 dígitos.")
    
    resultado = await maps_service.geocodificar(f"{cep_limpo}, Brasil")
    
    if not resultado.get("success"):
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    
    return {
        "success": True,
        "cep": cep_limpo,
        "data": resultado
    }
