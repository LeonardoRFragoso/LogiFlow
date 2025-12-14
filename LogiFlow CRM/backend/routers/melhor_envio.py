"""
LogiFlow CRM - Router Melhor Envio
Endpoints para cotação automática de frete
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
import logging

from integrations.frete.melhor_envio import MelhorEnvioClient
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Schemas
# ========================================

class CotacaoFreteRequest(BaseModel):
    origem_cep: str = Field(..., description="CEP de origem")
    destino_cep: str = Field(..., description="CEP de destino")
    peso_kg: float = Field(..., gt=0, description="Peso em kg")
    altura_cm: Optional[float] = Field(None, gt=0, description="Altura em cm")
    largura_cm: Optional[float] = Field(None, gt=0, description="Largura em cm")
    comprimento_cm: Optional[float] = Field(None, gt=0, description="Comprimento em cm")
    valor_mercadoria: Optional[float] = Field(None, ge=0, description="Valor da mercadoria")
    servicos: Optional[List[int]] = Field(None, description="IDs dos serviços específicos")
    
    @validator('origem_cep', 'destino_cep')
    def validar_cep(cls, v):
        cep_limpo = v.replace("-", "").replace(".", "")
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            raise ValueError("CEP deve conter 8 dígitos")
        return cep_limpo


class CotacaoSimplesRequest(BaseModel):
    origem_cep: str = Field(..., description="CEP de origem")
    destino_cep: str = Field(..., description="CEP de destino")
    peso_kg: float = Field(..., gt=0, description="Peso em kg")
    valor_mercadoria: Optional[float] = Field(None, ge=0, description="Valor da mercadoria")
    
    @validator('origem_cep', 'destino_cep')
    def validar_cep(cls, v):
        cep_limpo = v.replace("-", "").replace(".", "")
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            raise ValueError("CEP deve conter 8 dígitos")
        return cep_limpo


class MelhorCotacaoRequest(BaseModel):
    origem_cep: str
    destino_cep: str
    peso_kg: float = Field(..., gt=0)
    valor_mercadoria: Optional[float] = None
    prioridade: str = Field("preco", description="'preco' ou 'prazo'")
    
    @validator('origem_cep', 'destino_cep')
    def validar_cep(cls, v):
        cep_limpo = v.replace("-", "").replace(".", "")
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            raise ValueError("CEP deve conter 8 dígitos")
        return cep_limpo
    
    @validator('prioridade')
    def validar_prioridade(cls, v):
        if v not in ['preco', 'prazo']:
            raise ValueError("Prioridade deve ser 'preco' ou 'prazo'")
        return v


class ComparacaoTabelaRequest(BaseModel):
    origem_cep: str
    destino_cep: str
    peso_kg: float = Field(..., gt=0)
    valor_tabela_propria: float = Field(..., gt=0, description="Valor da tabela própria")
    valor_mercadoria: Optional[float] = None
    
    @validator('origem_cep', 'destino_cep')
    def validar_cep(cls, v):
        cep_limpo = v.replace("-", "").replace(".", "")
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            raise ValueError("CEP deve conter 8 dígitos")
        return cep_limpo


class RastreamentoRequest(BaseModel):
    tracking_code: str = Field(..., description="Código de rastreamento")


# ========================================
# Dependencies
# ========================================

def get_melhor_envio_client() -> MelhorEnvioClient:
    """Retorna cliente Melhor Envio configurado"""
    token = settings.MELHOR_ENVIO_TOKEN if hasattr(settings, 'MELHOR_ENVIO_TOKEN') else None
    sandbox = settings.MELHOR_ENVIO_SANDBOX if hasattr(settings, 'MELHOR_ENVIO_SANDBOX') else True
    
    if not token:
        raise HTTPException(
            status_code=500,
            detail="Token Melhor Envio não configurado. Configure MELHOR_ENVIO_TOKEN no .env"
        )
    
    return MelhorEnvioClient(token=token, sandbox=sandbox)


# ========================================
# Endpoints de Cotação
# ========================================

@router.post("/calcular")
async def calcular_frete(
    request: CotacaoFreteRequest,
    client: MelhorEnvioClient = Depends(get_melhor_envio_client)
):
    """
    Calcula frete para múltiplas transportadoras
    
    Retorna cotações de Correios, Jadlog, Azul Cargo e outras transportadoras
    """
    try:
        logger.info(f"Calculando frete: {request.origem_cep} -> {request.destino_cep}, {request.peso_kg}kg")
        
        # Se não informou dimensões, usar cálculo simplificado
        if not all([request.altura_cm, request.largura_cm, request.comprimento_cm]):
            result = client.calcular_frete_simples(
                origem_cep=request.origem_cep,
                destino_cep=request.destino_cep,
                peso_kg=request.peso_kg,
                valor_mercadoria=request.valor_mercadoria
            )
        else:
            result = client.calcular_frete(
                origem_cep=request.origem_cep,
                destino_cep=request.destino_cep,
                peso=request.peso_kg,
                altura=request.altura_cm,
                largura=request.largura_cm,
                comprimento=request.comprimento_cm,
                valor_declarado=request.valor_mercadoria,
                servicos=request.servicos
            )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        # Formatar resposta
        formatted = client.formatar_cotacao_para_logiflow(result)
        
        return formatted
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao calcular frete: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calcular-simples")
async def calcular_frete_simples(
    request: CotacaoSimplesRequest,
    client: MelhorEnvioClient = Depends(get_melhor_envio_client)
):
    """
    Calcula frete de forma simplificada (dimensões automáticas)
    
    Ideal para cotações rápidas onde não se conhece as dimensões exatas
    """
    try:
        logger.info(f"Cotação simples: {request.origem_cep} -> {request.destino_cep}, {request.peso_kg}kg")
        
        result = client.calcular_frete_simples(
            origem_cep=request.origem_cep,
            destino_cep=request.destino_cep,
            peso_kg=request.peso_kg,
            valor_mercadoria=request.valor_mercadoria
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        formatted = client.formatar_cotacao_para_logiflow(result)
        
        return formatted
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao calcular frete simples: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/melhor-cotacao")
async def obter_melhor_cotacao(
    request: MelhorCotacaoRequest,
    client: MelhorEnvioClient = Depends(get_melhor_envio_client)
):
    """
    Retorna a melhor cotação baseada em critério (preço ou prazo)
    
    Útil para sugestão automática ao cliente
    """
    try:
        logger.info(f"Buscando melhor cotação por {request.prioridade}")
        
        result = client.obter_melhor_cotacao(
            origem_cep=request.origem_cep,
            destino_cep=request.destino_cep,
            peso_kg=request.peso_kg,
            valor_mercadoria=request.valor_mercadoria,
            prioridade=request.prioridade
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter melhor cotação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/comparar-tabela")
async def comparar_com_tabela_propria(
    request: ComparacaoTabelaRequest,
    client: MelhorEnvioClient = Depends(get_melhor_envio_client)
):
    """
    Compara cotações do mercado com tabela própria
    
    Ajuda a decidir se vale a pena terceirizar ou usar frota própria
    """
    try:
        logger.info(f"Comparando com tabela própria: R$ {request.valor_tabela_propria}")
        
        result = client.comparar_com_tabela_propria(
            origem_cep=request.origem_cep,
            destino_cep=request.destino_cep,
            peso_kg=request.peso_kg,
            valor_tabela_propria=request.valor_tabela_propria,
            valor_mercadoria=request.valor_mercadoria
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao comparar com tabela: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints de Rastreamento
# ========================================

@router.get("/rastrear/{tracking_code}")
async def rastrear_envio(
    tracking_code: str,
    client: MelhorEnvioClient = Depends(get_melhor_envio_client)
):
    """
    Rastreia envio pelo código de rastreamento
    """
    try:
        result = client.rastrear_envio(tracking_code)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail="Envio não encontrado")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao rastrear envio {tracking_code}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints de Agências
# ========================================

@router.get("/agencias")
async def buscar_agencias(
    cep: str = Query(..., description="CEP para busca"),
    transportadora_id: Optional[int] = Query(None, description="ID da transportadora"),
    client: MelhorEnvioClient = Depends(get_melhor_envio_client)
):
    """
    Busca agências próximas a um CEP
    """
    try:
        cep_limpo = cep.replace("-", "").replace(".", "")
        
        result = client.buscar_agencias(cep_limpo, transportadora_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar agências: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints de Informação
# ========================================

@router.get("/servicos")
async def listar_servicos():
    """
    Lista serviços disponíveis no Melhor Envio
    """
    servicos = [
        {"id": 1, "nome": "Correios PAC", "tipo": "econômico"},
        {"id": 2, "nome": "Correios SEDEX", "tipo": "expresso"},
        {"id": 3, "nome": "Jadlog Package", "tipo": "econômico"},
        {"id": 4, "nome": "Azul Cargo Express", "tipo": "expresso"},
        {"id": 17, "nome": "Jadlog Econômico", "tipo": "econômico"},
        {"id": 23, "nome": "Loggi", "tipo": "econômico"},
        {"id": 24, "nome": "Loggi Express", "tipo": "expresso"}
    ]
    
    return {
        "success": True,
        "data": servicos
    }


@router.get("/status")
async def verificar_status():
    """
    Verifica status da integração com Melhor Envio
    """
    configurado = hasattr(settings, 'MELHOR_ENVIO_TOKEN') and settings.MELHOR_ENVIO_TOKEN is not None
    sandbox = settings.MELHOR_ENVIO_SANDBOX if hasattr(settings, 'MELHOR_ENVIO_SANDBOX') else True
    
    status = {
        "configurado": configurado,
        "ambiente": "sandbox" if sandbox else "producao",
        "ativo": False
    }
    
    # Testar conexão
    if configurado:
        try:
            client = get_melhor_envio_client()
            # Fazer uma cotação teste simples
            result = client.calcular_frete_simples(
                origem_cep="01310100",
                destino_cep="04101300",
                peso_kg=1.0
            )
            status["ativo"] = result.get("success", False)
        except:
            pass
    
    return {
        "success": True,
        "data": status
    }
