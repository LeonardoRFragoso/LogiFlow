"""
LogiFlow CRM - Serviço Fiscal
Lógica de negócio para CT-e e MDF-e
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import logging

from models.cte import CTe, StatusCTe
from models.mdfe import MDFe, StatusMDFe
from models.configuracao_fiscal import ConfiguracaoFiscal
from integrations.fiscal.focusnfe import FocusNFeClient

logger = logging.getLogger(__name__)


class FiscalService:
    """Serviço para operações fiscais"""
    
    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id
    
    def salvar_cte(self, dados_emissao: Dict, resultado_focus: Dict) -> CTe:
        """Salva CT-e no banco de dados após emissão"""
        try:
            cte = CTe(
                id=str(uuid.uuid4()),
                tenant_id=self.tenant_id,
                numero=resultado_focus.get("numero"),
                serie=dados_emissao.get("serie", "1"),
                chave=resultado_focus.get("chave"),
                ref=resultado_focus.get("ref"),
                status=StatusCTe.AUTORIZADO if resultado_focus.get("status") == "autorizado" else StatusCTe.PROCESSANDO,
                data_emissao=datetime.utcnow(),
                data_autorizacao=datetime.utcnow() if resultado_focus.get("status") == "autorizado" else None,
                protocolo=resultado_focus.get("protocolo"),
                pedido_id=dados_emissao.get("pedido_id"),
                valor_total=float(dados_emissao["valores"]["valor_total"]),
                valor_receber=float(dados_emissao["valores"]["valor_receber"]),
                valor_carga=float(dados_emissao["valores"].get("valor_carga", dados_emissao["valores"]["valor_total"])),
                peso_kg=float(dados_emissao["valores"]["peso_kg"]),
                modal=dados_emissao.get("modal", "01"),
                tipo_servico=dados_emissao.get("tipo_servico", "0"),
                natureza_operacao=dados_emissao.get("natureza_operacao", "PRESTACAO DE SERVICO DE TRANSPORTE"),
                tomador_tipo=dados_emissao["tomador"].get("tipo", "0"),
                tomador_cnpj=dados_emissao["tomador"]["documento"],
                tomador_nome=dados_emissao["tomador"]["nome"],
                tomador_dados=dados_emissao["tomador"],
                remetente_cnpj=dados_emissao["remetente"]["documento"],
                remetente_nome=dados_emissao["remetente"]["nome"],
                remetente_dados=dados_emissao["remetente"],
                destinatario_cnpj=dados_emissao["destinatario"]["documento"],
                destinatario_nome=dados_emissao["destinatario"]["nome"],
                destinatario_dados=dados_emissao["destinatario"],
                icms_situacao=dados_emissao.get("icms_situacao", "00"),
                icms_aliquota=float(dados_emissao.get("icms_aliquota", 0)),
                icms_valor=float(dados_emissao.get("icms_valor", 0)),
                veiculo_placa=dados_emissao["veiculo"]["placa"],
                veiculo_uf=dados_emissao["veiculo"]["uf"],
                veiculo_dados=dados_emissao["veiculo"],
                rntrc=dados_emissao.get("rntrc"),
                ciot=dados_emissao.get("ciot"),
                url_danfe=resultado_focus.get("url_danfe"),
                url_xml=resultado_focus.get("xml"),
                dados_completos={"emissao": dados_emissao, "resultado": resultado_focus}
            )
            
            self.db.add(cte)
            self.db.commit()
            self.db.refresh(cte)
            
            logger.info(f"CT-e {cte.numero} salvo com sucesso")
            return cte
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar CT-e: {e}")
            raise
    
    def salvar_mdfe(self, dados_emissao: Dict, resultado_focus: Dict) -> MDFe:
        """Salva MDF-e no banco de dados após emissão"""
        try:
            mdfe = MDFe(
                id=str(uuid.uuid4()),
                tenant_id=self.tenant_id,
                numero=resultado_focus.get("numero"),
                serie=dados_emissao.get("serie", "1"),
                chave=resultado_focus.get("chave"),
                ref=resultado_focus.get("ref"),
                status=StatusMDFe.AUTORIZADO if resultado_focus.get("status") == "autorizado" else StatusMDFe.PROCESSANDO,
                data_emissao=datetime.utcnow(),
                data_autorizacao=datetime.utcnow() if resultado_focus.get("status") == "autorizado" else None,
                protocolo=resultado_focus.get("protocolo"),
                modal=dados_emissao.get("modal", "1"),
                tipo_emitente=dados_emissao.get("tipo_emitente", "1"),
                percurso=dados_emissao.get("percurso", []),
                quantidade_ctes=len(dados_emissao.get("documentos", [])),
                veiculo_placa=dados_emissao["veiculo"]["placa"],
                veiculo_uf=dados_emissao["veiculo"]["uf"],
                veiculo_dados=dados_emissao["veiculo"],
                condutores=dados_emissao.get("condutores", []),
                documentos=dados_emissao.get("documentos", []),
                url_damdfe=resultado_focus.get("url_damdfe"),
                url_xml=resultado_focus.get("xml"),
                dados_completos={"emissao": dados_emissao, "resultado": resultado_focus}
            )
            
            self.db.add(mdfe)
            self.db.commit()
            self.db.refresh(mdfe)
            
            logger.info(f"MDF-e {mdfe.numero} salvo com sucesso")
            return mdfe
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar MDF-e: {e}")
            raise
    
    def obter_proximo_numero_cte(self) -> int:
        """Obtém próximo número de CT-e disponível"""
        config = self.db.query(ConfiguracaoFiscal).filter(
            ConfiguracaoFiscal.tenant_id == self.tenant_id
        ).first()
        
        if config and config.cte_proximo_numero:
            proximo = config.cte_proximo_numero
            config.cte_proximo_numero += 1
            self.db.commit()
            return proximo
        
        ultimo_cte = self.db.query(CTe).filter(
            CTe.tenant_id == self.tenant_id
        ).order_by(CTe.numero.desc()).first()
        
        return (ultimo_cte.numero + 1) if ultimo_cte else 1
    
    def obter_proximo_numero_mdfe(self) -> int:
        """Obtém próximo número de MDF-e disponível"""
        config = self.db.query(ConfiguracaoFiscal).filter(
            ConfiguracaoFiscal.tenant_id == self.tenant_id
        ).first()
        
        if config and config.mdfe_proximo_numero:
            proximo = config.mdfe_proximo_numero
            config.mdfe_proximo_numero += 1
            self.db.commit()
            return proximo
        
        ultimo_mdfe = self.db.query(MDFe).filter(
            MDFe.tenant_id == self.tenant_id
        ).order_by(MDFe.numero.desc()).first()
        
        return (ultimo_mdfe.numero + 1) if ultimo_mdfe else 1
    
    def validar_dados_cte(self, dados: Dict) -> tuple[bool, Optional[str]]:
        """Valida dados antes de emitir CT-e"""
        config = self.db.query(ConfiguracaoFiscal).filter(
            ConfiguracaoFiscal.tenant_id == self.tenant_id
        ).first()
        
        if not config or not config.configurado:
            return False, "Configuração fiscal não encontrada"
        
        if config.validar_dados_antes_emissao:
            if config.exigir_rntrc and not dados.get("rntrc"):
                return False, "RNTRC é obrigatório"
            
            if config.exigir_ciot and not dados.get("ciot"):
                return False, "CIOT é obrigatório"
        
        required_fields = ["tomador", "remetente", "destinatario", "valores", "veiculo"]
        for field in required_fields:
            if field not in dados:
                return False, f"Campo obrigatório ausente: {field}"
        
        return True, None
    
    def agrupar_ctes_para_mdfe(self, cte_ids: List[str]) -> Dict:
        """Agrupa CT-es para criar um MDF-e"""
        ctes = self.db.query(CTe).filter(
            CTe.id.in_(cte_ids),
            CTe.tenant_id == self.tenant_id,
            CTe.status == StatusCTe.AUTORIZADO,
            CTe.mdfe_id.is_(None)
        ).all()
        
        if not ctes:
            return {"success": False, "error": "Nenhum CT-e válido encontrado"}
        
        documentos = []
        percurso = set()
        valor_total = 0.0
        peso_total = 0.0
        
        for cte in ctes:
            documentos.append({
                "chave": cte.chave,
                "tipo": "CTE"
            })
            percurso.add(cte.remetente_dados.get("uf"))
            percurso.add(cte.destinatario_dados.get("uf"))
            valor_total += cte.valor_total
            peso_total += cte.peso_kg
        
        return {
            "success": True,
            "documentos": documentos,
            "percurso": sorted(list(percurso)),
            "quantidade_ctes": len(ctes),
            "valor_total_carga": valor_total,
            "peso_total_kg": peso_total,
            "ctes": [cte.id for cte in ctes]
        }
    
    def vincular_ctes_ao_mdfe(self, mdfe_id: str, cte_ids: List[str]):
        """Vincula CT-es a um MDF-e"""
        try:
            self.db.query(CTe).filter(
                CTe.id.in_(cte_ids),
                CTe.tenant_id == self.tenant_id
            ).update({"mdfe_id": mdfe_id}, synchronize_session=False)
            
            self.db.commit()
            logger.info(f"CT-es vinculados ao MDF-e {mdfe_id}")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao vincular CT-es ao MDF-e: {e}")
            raise
