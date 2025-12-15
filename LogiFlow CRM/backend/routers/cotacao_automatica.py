"""
LogiFlow CRM - Router Cotação Automática
Endpoints para cotação consolidada com múltiplas transportadoras
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
import logging

from integrations.frete.melhor_envio import MelhorEnvioClient
from integrations.frete.frenet import FrenetClient
from integrations.maps.distance_matrix import DistanceMatrixClient
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Schemas
# ========================================

class CotacaoAutomaticaRequest(BaseModel):
    origem_cep: str = Field(..., description="CEP de origem")
    destino_cep: str = Field(..., description="CEP de destino")
    peso_kg: float = Field(..., gt=0, description="Peso em kg")
    altura_cm: Optional[float] = Field(20, gt=0, description="Altura em cm")
    largura_cm: Optional[float] = Field(20, gt=0, description="Largura em cm")
    comprimento_cm: Optional[float] = Field(20, gt=0, description="Comprimento em cm")
    valor_mercadoria: Optional[float] = Field(0, ge=0, description="Valor da mercadoria")
    incluir_melhor_envio: bool = Field(True, description="Incluir Melhor Envio")
    incluir_frenet: bool = Field(True, description="Incluir Frenet")
    incluir_tabela_propria: bool = Field(True, description="Incluir tabela própria")
    
    @validator('origem_cep', 'destino_cep')
    def validar_cep(cls, v):
        cep_limpo = v.replace("-", "").replace(".", "")
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            raise ValueError("CEP deve conter 8 dígitos")
        return cep_limpo


# ========================================
# Endpoints
# ========================================

@router.post("/cotar")
async def cotar_frete_automatico(request: CotacaoAutomaticaRequest):
    """
    Cotação automática consolidada de múltiplas transportadoras
    
    Consulta:
    - Melhor Envio (Correios, Jadlog, Azul, etc)
    - Frenet (Correios via Frenet)
    - Tabela Própria (frota própria)
    
    Returns:
        Todas as cotações ordenadas por melhor custo-benefício
    """
    try:
        todas_cotacoes = []
        erros = []

        # Garantir pelo menos uma integração habilitada
        if not any([
            request.incluir_melhor_envio and settings.MELHOR_ENVIO_TOKEN,
            request.incluir_frenet and getattr(settings, "FRENET_TOKEN", None),
            request.incluir_tabela_propria
        ]):
            raise HTTPException(
                status_code=400,
                detail="Nenhuma integração de frete disponível. Configure MELHOR_ENVIO_TOKEN/FRENET_TOKEN ou habilite tabela própria."
            )
        
        # 1. Melhor Envio
        if request.incluir_melhor_envio and settings.MELHOR_ENVIO_TOKEN:
            try:
                me_client = MelhorEnvioClient(
                    token=settings.MELHOR_ENVIO_TOKEN,
                    sandbox=settings.MELHOR_ENVIO_SANDBOX
                )
                
                resultado_me = me_client.calcular_frete_simples(
                    origem_cep=request.origem_cep,
                    destino_cep=request.destino_cep,
                    peso_kg=request.peso_kg,
                    valor_mercadoria=request.valor_mercadoria
                )
                
                if resultado_me.get("success"):
                    for cotacao in resultado_me.get("cotacoes", []):
                        cotacao["fonte"] = "melhor_envio"
                        todas_cotacoes.append(cotacao)
                else:
                    erros.append({
                        "fonte": "melhor_envio",
                        "erro": resultado_me.get("error", "Erro desconhecido")
                    })
                    
            except Exception as e:
                logger.error(f"Erro Melhor Envio: {e}")
                erros.append({"fonte": "melhor_envio", "erro": str(e)})
        
        # 2. Frenet
        if request.incluir_frenet and hasattr(settings, 'FRENET_TOKEN') and settings.FRENET_TOKEN:
            try:
                frenet_client = FrenetClient(token=settings.FRENET_TOKEN)
                
                resultado_frenet = frenet_client.calcular_frete({
                    "cep_origem": request.origem_cep,
                    "cep_destino": request.destino_cep,
                    "peso": request.peso_kg,
                    "altura": request.altura_cm,
                    "largura": request.largura_cm,
                    "comprimento": request.comprimento_cm,
                    "valor_declarado": request.valor_mercadoria
                })
                
                if resultado_frenet.get("success"):
                    for cotacao in resultado_frenet.get("cotacoes", []):
                        cotacao["fonte"] = "frenet"
                        todas_cotacoes.append(cotacao)
                else:
                    erros.append({
                        "fonte": "frenet",
                        "erro": resultado_frenet.get("error", "Erro desconhecido")
                    })
                    
            except Exception as e:
                logger.error(f"Erro Frenet: {e}")
                erros.append({"fonte": "frenet", "erro": str(e)})
        
        # 3. Tabela Própria
        if request.incluir_tabela_propria:
            try:
                cotacao_propria = calcular_tabela_propria(
                    origem_cep=request.origem_cep,
                    destino_cep=request.destino_cep,
                    peso_kg=request.peso_kg,
                    valor_mercadoria=request.valor_mercadoria
                )
                cotacao_propria["fonte"] = "tabela_propria"
                todas_cotacoes.append(cotacao_propria)
                
            except Exception as e:
                logger.error(f"Erro Tabela Própria: {e}")
                erros.append({"fonte": "tabela_propria", "erro": str(e)})
        else:
            erros.append({"fonte": "tabela_propria", "erro": "Tabela própria desabilitada"})

        # 4. Opcional: distância via Google Distance Matrix (quando chave configurada)
        distancia_info = None
        try:
            dm_client = DistanceMatrixClient.from_settings()
            dm_resp = dm_client.calcular_distancia_por_cep(request.origem_cep, request.destino_cep)
            if dm_resp.get("success"):
                distancia_info = {
                    "km": dm_resp["distancia"]["km"],
                    "texto": dm_resp["distancia"]["texto"],
                    "duracao_minutos": dm_resp["duracao"]["minutos"],
                    "duracao_texto": dm_resp["duracao"]["texto"]
                }
            else:
                erros.append({"fonte": "distance_matrix", "erro": dm_resp.get("error", "Erro Distance Matrix")})
        except ValueError as e:
            # Em produção, sem chave → bloquear; em DEBUG apenas avisa
            if not settings.DEBUG:
                raise HTTPException(status_code=400, detail=str(e))
            erros.append({"fonte": "distance_matrix", "erro": str(e)})
        except Exception as e:
            logger.error(f"Erro Distance Matrix: {e}")
            erros.append({"fonte": "distance_matrix", "erro": str(e)})
        
        # Ordenar por valor (mais barato primeiro)
        todas_cotacoes.sort(key=lambda x: x.get("valor", float('inf')))
        
        # Identificar melhor opção
        melhor_opcao = todas_cotacoes[0] if todas_cotacoes else None
        
        # Calcular economia vs mais caro
        if len(todas_cotacoes) > 1:
            mais_caro = max(todas_cotacoes, key=lambda x: x.get("valor", 0))
            economia = mais_caro["valor"] - melhor_opcao["valor"]
            economia_percentual = (economia / mais_caro["valor"]) * 100
        else:
            economia = 0
            economia_percentual = 0
        
        return {
            "success": True,
            "total_cotacoes": len(todas_cotacoes),
            "cotacoes": todas_cotacoes,
            "melhor_opcao": melhor_opcao,
            "economia": {
                "valor": round(economia, 2),
                "percentual": round(economia_percentual, 2)
            },
            "distancia": distancia_info,
            "erros": erros if erros else None,
            "parametros": {
                "origem_cep": request.origem_cep,
                "destino_cep": request.destino_cep,
                "peso_kg": request.peso_kg
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao cotar frete automático: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frenet/cotar")
async def cotar_frenet(
    origem_cep: str = Query(..., description="CEP de origem"),
    destino_cep: str = Query(..., description="CEP de destino"),
    peso_kg: float = Query(..., gt=0, description="Peso em kg"),
    valor_mercadoria: float = Query(0, ge=0, description="Valor da mercadoria")
):
    """
    Cotação via Frenet
    
    Args:
        origem_cep: CEP de origem
        destino_cep: CEP de destino
        peso_kg: Peso em kg
        valor_mercadoria: Valor da mercadoria
        
    Returns:
        Cotações Frenet
    """
    try:
        if not hasattr(settings, 'FRENET_TOKEN') or not settings.FRENET_TOKEN:
            raise HTTPException(
                status_code=400,
                detail="Token Frenet não configurado. Configure FRENET_TOKEN no .env"
            )
        
        frenet_client = FrenetClient(token=settings.FRENET_TOKEN)
        resultado = frenet_client.calcular_frete_simplificado(
            cep_origem=origem_cep,
            cep_destino=destino_cep,
            peso=peso_kg,
            valor_declarado=valor_mercadoria
        )
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao cotar Frenet: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frenet/rastrear/{codigo}")
async def rastrear_frenet(codigo: str):
    """
    Rastreia envio via Frenet
    
    Args:
        codigo: Código de rastreamento
        
    Returns:
        Status do envio
    """
    try:
        if not hasattr(settings, 'FRENET_TOKEN') or not settings.FRENET_TOKEN:
            raise HTTPException(
                status_code=400,
                detail="Token Frenet não configurado"
            )
        
        frenet_client = FrenetClient(token=settings.FRENET_TOKEN)
        resultado = frenet_client.rastrear_envio(codigo)
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao rastrear Frenet: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comparar")
async def comparar_opcoes(
    origem_cep: str = Query(..., description="CEP de origem"),
    destino_cep: str = Query(..., description="CEP de destino"),
    peso_kg: float = Query(..., gt=0, description="Peso em kg"),
    valor_mercadoria: float = Query(0, ge=0, description="Valor da mercadoria")
):
    """
    Compara todas as opções de frete disponíveis
    
    Retorna análise comparativa detalhada
    """
    try:
        # Usar endpoint de cotação automática
        request = CotacaoAutomaticaRequest(
            origem_cep=origem_cep,
            destino_cep=destino_cep,
            peso_kg=peso_kg,
            valor_mercadoria=valor_mercadoria
        )
        
        resultado = await cotar_frete_automatico(request)
        
        if not resultado.get("success") or not resultado.get("cotacoes"):
            return {
                "success": False,
                "message": "Nenhuma cotação disponível"
            }
        
        cotacoes = resultado["cotacoes"]
        
        # Análise comparativa
        analise = {
            "mais_barato": cotacoes[0],
            "mais_rapido": min(cotacoes, key=lambda x: x.get("prazo_dias", 999)),
            "melhor_custo_beneficio": calcular_melhor_custo_beneficio(cotacoes),
            "tabela_comparativa": gerar_tabela_comparativa(cotacoes),
            "recomendacao": gerar_recomendacao(cotacoes)
        }
        
        return {
            "success": True,
            "analise": analise,
            "todas_cotacoes": cotacoes
        }
        
    except Exception as e:
        logger.error(f"Erro ao comparar opções: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Funções Auxiliares
# ========================================

def calcular_tabela_propria(
    origem_cep: str,
    destino_cep: str,
    peso_kg: float,
    valor_mercadoria: float
) -> Dict:
    """
    Calcula frete baseado na tabela própria
    
    Fórmula simplificada:
    - Base: R$ 50,00
    - Por kg: R$ 2,00
    - Seguro: 1% do valor da mercadoria
    - Prazo: 3-5 dias úteis
    """
    valor_base = 50.00
    valor_por_kg = 2.00
    seguro = valor_mercadoria * 0.01 if valor_mercadoria > 0 else 0
    
    valor_total = valor_base + (peso_kg * valor_por_kg) + seguro
    prazo_dias = 4  # Prazo médio
    
    return {
        "transportadora": "Frota Própria",
        "servico": "Entrega Padrão",
        "codigo_servico": "PROPRIO",
        "valor": round(valor_total, 2),
        "prazo_dias": prazo_dias,
        "prazo_descricao": f"{prazo_dias} dias úteis",
        "observacoes": "Frota própria - Serviço personalizado",
        "origem": "tabela_propria",
        "detalhamento": {
            "valor_base": valor_base,
            "valor_peso": peso_kg * valor_por_kg,
            "seguro": seguro
        }
    }


def calcular_melhor_custo_beneficio(cotacoes: List[Dict]) -> Dict:
    """
    Calcula melhor custo-benefício considerando preço e prazo
    
    Score = (valor_normalizado * 0.6) + (prazo_normalizado * 0.4)
    Menor score = melhor
    """
    if not cotacoes:
        return None
    
    # Normalizar valores
    valores = [c.get("valor", 0) for c in cotacoes]
    prazos = [c.get("prazo_dias", 0) for c in cotacoes]
    
    min_valor = min(valores)
    max_valor = max(valores)
    min_prazo = min(prazos)
    max_prazo = max(prazos)
    
    melhor_score = float('inf')
    melhor_cotacao = None
    
    for cotacao in cotacoes:
        valor = cotacao.get("valor", 0)
        prazo = cotacao.get("prazo_dias", 0)
        
        # Normalizar (0-1)
        valor_norm = (valor - min_valor) / (max_valor - min_valor) if max_valor > min_valor else 0
        prazo_norm = (prazo - min_prazo) / (max_prazo - min_prazo) if max_prazo > min_prazo else 0
        
        # Calcular score (60% preço, 40% prazo)
        score = (valor_norm * 0.6) + (prazo_norm * 0.4)
        
        if score < melhor_score:
            melhor_score = score
            melhor_cotacao = cotacao.copy()
            melhor_cotacao["score_custo_beneficio"] = round(score, 3)
    
    return melhor_cotacao


def gerar_tabela_comparativa(cotacoes: List[Dict]) -> List[Dict]:
    """Gera tabela comparativa formatada"""
    tabela = []
    
    for cotacao in cotacoes:
        tabela.append({
            "transportadora": cotacao.get("transportadora", "N/A"),
            "servico": cotacao.get("servico", "N/A"),
            "valor": f"R$ {cotacao.get('valor', 0):.2f}",
            "prazo": f"{cotacao.get('prazo_dias', 0)} dias",
            "fonte": cotacao.get("fonte", "N/A")
        })
    
    return tabela


def gerar_recomendacao(cotacoes: List[Dict]) -> Dict:
    """Gera recomendação inteligente"""
    if not cotacoes:
        return {"tipo": "erro", "mensagem": "Nenhuma cotação disponível"}
    
    mais_barato = cotacoes[0]
    mais_rapido = min(cotacoes, key=lambda x: x.get("prazo_dias", 999))
    melhor_cb = calcular_melhor_custo_beneficio(cotacoes)
    
    # Verificar se há frota própria
    tem_propria = any(c.get("fonte") == "tabela_propria" for c in cotacoes)
    
    if tem_propria:
        propria = next(c for c in cotacoes if c.get("fonte") == "tabela_propria")
        economia_vs_propria = propria["valor"] - mais_barato["valor"]
        
        if economia_vs_propria > propria["valor"] * 0.15:  # Economia > 15%
            return {
                "tipo": "terceirizar",
                "opcao_recomendada": mais_barato,
                "motivo": f"Economia de R$ {economia_vs_propria:.2f} ({(economia_vs_propria/propria['valor']*100):.1f}%) vs frota própria",
                "economia": economia_vs_propria
            }
        else:
            return {
                "tipo": "frota_propria",
                "opcao_recomendada": propria,
                "motivo": "Diferença pequena, priorizar frota própria para manter controle",
                "diferenca": economia_vs_propria
            }
    else:
        return {
            "tipo": "melhor_opcao",
            "opcao_recomendada": melhor_cb,
            "motivo": "Melhor custo-benefício entre as opções disponíveis"
        }
