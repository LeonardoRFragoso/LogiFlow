"""
LogiFlow CRM - Router Fiscal
Endpoints para emissão de CT-e e MDF-e
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import logging

from integrations.fiscal.focusnfe import FocusNFeClient
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Schemas
# ========================================

class EnderecoFiscal(BaseModel):
    documento: str = Field(..., description="CPF ou CNPJ")
    ie: Optional[str] = Field(None, description="Inscrição Estadual")
    nome: str
    endereco: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    uf: str
    cep: str
    telefone: Optional[str] = None
    email: Optional[str] = None


class ValoresCTe(BaseModel):
    valor_total: float
    valor_receber: float
    valor_carga: Optional[float] = None
    produto_predominante: Optional[str] = "MERCADORIA"
    peso_kg: float


class VeiculoCTe(BaseModel):
    placa: str
    renavam: Optional[str] = None
    uf: str
    tipo: Optional[str] = "02"


class EmitirCTeRequest(BaseModel):
    pedido_id: str = Field(..., description="ID do pedido no SuiteCRM")
    numero: Optional[int] = None
    serie: Optional[str] = "1"
    natureza_operacao: Optional[str] = "PRESTACAO DE SERVICO DE TRANSPORTE"
    modal: Optional[str] = "01"
    
    tomador: EnderecoFiscal
    remetente: EnderecoFiscal
    destinatario: EnderecoFiscal
    valores: ValoresCTe
    veiculo: VeiculoCTe
    
    rntrc: Optional[str] = None
    ciot: Optional[str] = None
    icms_situacao: Optional[str] = "00"
    icms_aliquota: Optional[str] = "0.00"
    icms_valor: Optional[str] = "0.00"


class CancelarCTeRequest(BaseModel):
    justificativa: str = Field(..., min_length=15, description="Motivo do cancelamento")


class EmitirMDFeRequest(BaseModel):
    numero: Optional[int] = None
    serie: Optional[str] = "1"
    modal: Optional[str] = "1"
    percurso: List[str] = Field(..., description="Lista de UFs do percurso")
    documentos: List[Dict] = Field(..., description="Lista de CT-es vinculados")
    veiculo: VeiculoCTe
    condutores: List[Dict]


class EncerrarMDFeRequest(BaseModel):
    uf: str
    cidade_codigo: str = Field(..., description="Código IBGE da cidade")


# ========================================
# Dependency
# ========================================

def get_focusnfe_client() -> FocusNFeClient:
    """Retorna cliente Focus NFe configurado"""
    token = settings.FOCUSNFE_TOKEN
    if not token:
        raise HTTPException(
            status_code=500,
            detail="Token Focus NFe não configurado. Configure FOCUSNFE_TOKEN no .env"
        )
    
    ambiente = "homologacao" if settings.DEBUG else "producao"
    return FocusNFeClient(token=token, ambiente=ambiente)


# ========================================
# Endpoints CT-e
# ========================================

@router.post("/cte/emitir")
async def emitir_cte(
    request: EmitirCTeRequest,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Emite CT-e via Focus NFe"""
    try:
        logger.info(f"Emitindo CT-e para pedido {request.pedido_id}")
        
        dados = {
            "numero": request.numero,
            "serie": request.serie,
            "natureza_operacao": request.natureza_operacao,
            "modal": request.modal,
            "tomador": request.tomador.dict(),
            "remetente": request.remetente.dict(),
            "destinatario": request.destinatario.dict(),
            "valores": request.valores.dict(),
            "veiculo": request.veiculo.dict(),
            "rntrc": request.rntrc,
            "ciot": request.ciot,
            "icms_situacao": request.icms_situacao,
            "icms_aliquota": request.icms_aliquota,
            "icms_valor": request.icms_valor
        }
        
        result = client.emitir_cte(dados)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Erro ao emitir CT-e")
            )
        
        return {
            "success": True,
            "message": "CT-e emitido com sucesso",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao emitir CT-e: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cte/{ref}")
async def consultar_cte(
    ref: str,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Consulta status de um CT-e pela referência"""
    try:
        result = client.consultar_cte(ref)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail="CT-e não encontrado")
        
        return result["data"]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao consultar CT-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/cte/{ref}")
async def cancelar_cte(
    ref: str,
    request: CancelarCTeRequest,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Cancela um CT-e"""
    try:
        result = client.cancelar_cte(ref, request.justificativa)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Erro ao cancelar CT-e")
            )
        
        return {
            "success": True,
            "message": "CT-e cancelado com sucesso",
            "data": result["data"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao cancelar CT-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cte/{ref}/pdf")
async def download_cte_pdf(
    ref: str,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Baixa PDF do DACTE"""
    try:
        from fastapi.responses import Response
        
        pdf_bytes = client.download_pdf(ref, tipo="cte")
        
        if not pdf_bytes:
            raise HTTPException(status_code=404, detail="PDF não encontrado")
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=DACTE_{ref}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao baixar PDF do CT-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cte/{ref}/xml")
async def download_cte_xml(
    ref: str,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Baixa XML do CT-e"""
    try:
        from fastapi.responses import Response
        
        xml_content = client.download_xml(ref, tipo="cte")
        
        if not xml_content:
            raise HTTPException(status_code=404, detail="XML não encontrado")
        
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={
                "Content-Disposition": f"attachment; filename=CTE_{ref}.xml"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao baixar XML do CT-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints MDF-e
# ========================================

@router.post("/mdfe/emitir")
async def emitir_mdfe(
    request: EmitirMDFeRequest,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Emite MDF-e (Manifesto de Documentos Fiscais)"""
    try:
        logger.info("Emitindo MDF-e")
        
        dados = request.dict()
        result = client.emitir_mdfe(dados)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Erro ao emitir MDF-e")
            )
        
        return {
            "success": True,
            "message": "MDF-e emitido com sucesso",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao emitir MDF-e: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/mdfe/{ref}/encerrar")
async def encerrar_mdfe(
    ref: str,
    request: EncerrarMDFeRequest,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Encerra um MDF-e"""
    try:
        result = client.encerrar_mdfe(
            ref,
            request.uf,
            request.cidade_codigo
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Erro ao encerrar MDF-e")
            )
        
        return {
            "success": True,
            "message": "MDF-e encerrado com sucesso",
            "data": result["data"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao encerrar MDF-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mdfe/{ref}/pdf")
async def download_mdfe_pdf(
    ref: str,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Baixa PDF do DAMDFE"""
    try:
        from fastapi.responses import Response
        
        pdf_bytes = client.download_pdf(ref, tipo="mdfe")
        
        if not pdf_bytes:
            raise HTTPException(status_code=404, detail="PDF não encontrado")
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=DAMDFE_{ref}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao baixar PDF do MDF-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
