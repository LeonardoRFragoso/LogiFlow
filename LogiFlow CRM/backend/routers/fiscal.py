"""
LogiFlow CRM - Router Fiscal
Endpoints para emissão de CT-e e MDF-e
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
import logging
import uuid

from integrations.fiscal.focusnfe import FocusNFeClient
from config import settings
from database import get_db
from models.cte import CTe, StatusCTe
from models.mdfe import MDFe, StatusMDFe
from models.configuracao_fiscal import ConfiguracaoFiscal
from models import User
from auth import get_current_user
from services.integration_manager import get_focusnfe_client as get_tenant_focusnfe_client

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
    pedido_id: str = Field(..., description="ID do pedido")
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


class CancelarMDFeRequest(BaseModel):
    justificativa: str = Field(..., min_length=15, description="Motivo do cancelamento")


class ConfiguracaoFiscalRequest(BaseModel):
    emitente_cnpj: str
    emitente_razao_social: str
    emitente_nome_fantasia: Optional[str] = None
    emitente_ie: str
    emitente_endereco: str
    emitente_numero: str
    emitente_complemento: Optional[str] = None
    emitente_bairro: str
    emitente_cidade: str
    emitente_uf: str
    emitente_cep: str
    emitente_telefone: Optional[str] = None
    emitente_email: Optional[str] = None
    rntrc: Optional[str] = None
    cte_serie_padrao: Optional[str] = "1"
    mdfe_serie_padrao: Optional[str] = "1"
    focusnfe_token: Optional[str] = None


# ========================================
# Dependency
# ========================================

def get_focusnfe_client(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> FocusNFeClient:
    """Retorna cliente Focus NFe configurado para o tenant do usuário"""
    client = get_tenant_focusnfe_client(current_user.tenant_id, db)
    
    if not client:
        raise HTTPException(
            status_code=400,
            detail="Focus NFe não configurado. Configure suas credenciais em Configurações > Integrações."
        )
    
    return client


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


@router.get("/mdfe/{ref}/xml")
async def download_mdfe_xml(
    ref: str,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Baixa XML do MDF-e"""
    try:
        from fastapi.responses import Response
        
        xml_content = client.download_xml(ref, tipo="mdfe")
        
        if not xml_content:
            raise HTTPException(status_code=404, detail="XML não encontrado")
        
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={
                "Content-Disposition": f"attachment; filename=MDFE_{ref}.xml"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao baixar XML do MDF-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mdfe/{ref}")
async def consultar_mdfe(
    ref: str,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Consulta status de um MDF-e pela referência"""
    try:
        result = client.consultar_mdfe(ref)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail="MDF-e não encontrado")
        
        return result["data"]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao consultar MDF-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/mdfe/{ref}")
async def cancelar_mdfe(
    ref: str,
    request: CancelarMDFeRequest,
    client: FocusNFeClient = Depends(get_focusnfe_client)
):
    """Cancela um MDF-e"""
    try:
        result = client.cancelar_mdfe(ref, request.justificativa)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Erro ao cancelar MDF-e")
            )
        
        return {
            "success": True,
            "message": "MDF-e cancelado com sucesso",
            "data": result["data"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao cancelar MDF-e {ref}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints de Listagem
# ========================================

@router.get("/cte")
async def listar_ctes(
    request: Request,
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    pedido_id: Optional[str] = Query(None, description="Filtrar por pedido"),
    data_inicio: Optional[str] = Query(None, description="Data início (YYYY-MM-DD)"),
    data_fim: Optional[str] = Query(None, description="Data fim (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Lista todos os CT-es do tenant"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        query = db.query(CTe).filter(CTe.tenant_id == tenant_id)
        
        if status:
            query = query.filter(CTe.status == status)
        
        if pedido_id:
            query = query.filter(CTe.pedido_id == pedido_id)
        
        if data_inicio:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            query = query.filter(CTe.data_emissao >= data_inicio_dt)
        
        if data_fim:
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
            query = query.filter(CTe.data_emissao <= data_fim_dt)
        
        total = query.count()
        
        ctes = query.order_by(CTe.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "success": True,
            "data": [cte.to_dict() for cte in ctes],
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar CT-es: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mdfe")
async def listar_mdfes(
    request: Request,
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    data_inicio: Optional[str] = Query(None, description="Data início (YYYY-MM-DD)"),
    data_fim: Optional[str] = Query(None, description="Data fim (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Lista todos os MDF-es do tenant"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        query = db.query(MDFe).filter(MDFe.tenant_id == tenant_id)
        
        if status:
            query = query.filter(MDFe.status == status)
        
        if data_inicio:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            query = query.filter(MDFe.data_emissao >= data_inicio_dt)
        
        if data_fim:
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
            query = query.filter(MDFe.data_emissao <= data_fim_dt)
        
        total = query.count()
        
        mdfes = query.order_by(MDFe.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "success": True,
            "data": [mdfe.to_dict() for mdfe in mdfes],
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
        
    except Exception as e:
        logger.error(f"Erro ao listar MDF-es: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints de Configuração Fiscal
# ========================================

@router.get("/configuracao")
async def obter_configuracao_fiscal(
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtém configuração fiscal do tenant"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        config = db.query(ConfiguracaoFiscal).filter(
            ConfiguracaoFiscal.tenant_id == tenant_id
        ).first()
        
        if not config:
            return {
                "success": True,
                "data": None,
                "message": "Configuração fiscal não encontrada"
            }
        
        return {
            "success": True,
            "data": config.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter configuração fiscal: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/configuracao")
async def criar_configuracao_fiscal(
    request: Request,
    config_data: ConfiguracaoFiscalRequest,
    db: Session = Depends(get_db)
):
    """Cria ou atualiza configuração fiscal do tenant"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        config = db.query(ConfiguracaoFiscal).filter(
            ConfiguracaoFiscal.tenant_id == tenant_id
        ).first()
        
        if config:
            for key, value in config_data.dict(exclude_unset=True).items():
                setattr(config, key, value)
            config.configurado = True
            config.updated_at = datetime.utcnow()
        else:
            config = ConfiguracaoFiscal(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                **config_data.dict(exclude_unset=True),
                configurado=True
            )
            db.add(config)
        
        db.commit()
        db.refresh(config)
        
        return {
            "success": True,
            "message": "Configuração fiscal salva com sucesso",
            "data": config.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao salvar configuração fiscal: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/configuracao")
async def atualizar_configuracao_fiscal(
    request: Request,
    config_data: ConfiguracaoFiscalRequest,
    db: Session = Depends(get_db)
):
    """Atualiza configuração fiscal do tenant"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        config = db.query(ConfiguracaoFiscal).filter(
            ConfiguracaoFiscal.tenant_id == tenant_id
        ).first()
        
        if not config:
            raise HTTPException(
                status_code=404,
                detail="Configuração fiscal não encontrada"
            )
        
        for key, value in config_data.dict(exclude_unset=True).items():
            setattr(config, key, value)
        
        config.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(config)
        
        return {
            "success": True,
            "message": "Configuração fiscal atualizada com sucesso",
            "data": config.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar configuração fiscal: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Endpoints de Dashboard e Estatísticas
# ========================================

@router.get("/dashboard")
async def dashboard_fiscal(
    request: Request,
    db: Session = Depends(get_db),
    mes: Optional[int] = Query(None, ge=1, le=12),
    ano: Optional[int] = Query(None, ge=2020)
):
    """Dashboard com estatísticas fiscais"""
    try:
        tenant_id = getattr(request.state, "tenant_id", "default")
        
        now = datetime.utcnow()
        mes_atual = mes or now.month
        ano_atual = ano or now.year
        
        data_inicio = datetime(ano_atual, mes_atual, 1)
        if mes_atual == 12:
            data_fim = datetime(ano_atual + 1, 1, 1)
        else:
            data_fim = datetime(ano_atual, mes_atual + 1, 1)
        
        ctes_query = db.query(CTe).filter(
            CTe.tenant_id == tenant_id,
            CTe.data_emissao >= data_inicio,
            CTe.data_emissao < data_fim
        )
        
        mdfes_query = db.query(MDFe).filter(
            MDFe.tenant_id == tenant_id,
            MDFe.data_emissao >= data_inicio,
            MDFe.data_emissao < data_fim
        )
        
        total_ctes = ctes_query.count()
        total_mdfes = mdfes_query.count()
        
        ctes_autorizados = ctes_query.filter(CTe.status == StatusCTe.AUTORIZADO).count()
        ctes_cancelados = ctes_query.filter(CTe.status == StatusCTe.CANCELADO).count()
        ctes_rejeitados = ctes_query.filter(CTe.status == StatusCTe.REJEITADO).count()
        
        mdfes_autorizados = mdfes_query.filter(MDFe.status == StatusMDFe.AUTORIZADO).count()
        mdfes_encerrados = mdfes_query.filter(MDFe.status == StatusMDFe.ENCERRADO).count()
        mdfes_cancelados = mdfes_query.filter(MDFe.status == StatusMDFe.CANCELADO).count()
        
        valor_total_ctes = db.query(db.func.sum(CTe.valor_total)).filter(
            CTe.tenant_id == tenant_id,
            CTe.data_emissao >= data_inicio,
            CTe.data_emissao < data_fim,
            CTe.status == StatusCTe.AUTORIZADO
        ).scalar() or 0.0
        
        return {
            "success": True,
            "data": {
                "periodo": {
                    "mes": mes_atual,
                    "ano": ano_atual
                },
                "ctes": {
                    "total": total_ctes,
                    "autorizados": ctes_autorizados,
                    "cancelados": ctes_cancelados,
                    "rejeitados": ctes_rejeitados,
                    "valor_total": float(valor_total_ctes)
                },
                "mdfes": {
                    "total": total_mdfes,
                    "autorizados": mdfes_autorizados,
                    "encerrados": mdfes_encerrados,
                    "cancelados": mdfes_cancelados
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Erro ao gerar dashboard fiscal: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========================================
# Webhook Focus NFe
# ========================================

@router.post("/webhook")
async def webhook_focusnfe(
    request: Request,
    db: Session = Depends(get_db)
):
    """Recebe notificações do Focus NFe"""
    try:
        data = await request.json()
        logger.info(f"Webhook recebido: {data}")
        
        tipo = data.get("tipo")
        ref = data.get("ref")
        status = data.get("status")
        
        if tipo == "cte":
            cte = db.query(CTe).filter(CTe.ref == ref).first()
            if cte:
                if status == "autorizado":
                    cte.status = StatusCTe.AUTORIZADO
                    cte.data_autorizacao = datetime.utcnow()
                    cte.protocolo = data.get("protocolo")
                    cte.chave = data.get("chave_nfe")
                elif status == "cancelado":
                    cte.status = StatusCTe.CANCELADO
                    cte.data_cancelamento = datetime.utcnow()
                elif status == "rejeitado":
                    cte.status = StatusCTe.REJEITADO
                    cte.mensagem_erro = data.get("mensagem_sefaz")
                
                db.commit()
        
        elif tipo == "mdfe":
            mdfe = db.query(MDFe).filter(MDFe.ref == ref).first()
            if mdfe:
                if status == "autorizado":
                    mdfe.status = StatusMDFe.AUTORIZADO
                    mdfe.data_autorizacao = datetime.utcnow()
                    mdfe.protocolo = data.get("protocolo")
                    mdfe.chave = data.get("chave_nfe")
                elif status == "encerrado":
                    mdfe.status = StatusMDFe.ENCERRADO
                    mdfe.data_encerramento = datetime.utcnow()
                    mdfe.protocolo_encerramento = data.get("protocolo")
                elif status == "cancelado":
                    mdfe.status = StatusMDFe.CANCELADO
                    mdfe.data_cancelamento = datetime.utcnow()
                elif status == "rejeitado":
                    mdfe.status = StatusMDFe.REJEITADO
                    mdfe.mensagem_erro = data.get("mensagem_sefaz")
                
                db.commit()
        
        return {"success": True, "message": "Webhook processado"}
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return {"success": False, "error": str(e)}
