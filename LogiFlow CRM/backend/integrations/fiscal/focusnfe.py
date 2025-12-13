"""
LogiFlow CRM - Integração Focus NFe
Cliente para emissão de CT-e e MDF-e
"""

import requests
from typing import Dict, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FocusNFeClient:
    """Cliente para API Focus NFe - Emissão de documentos fiscais"""
    
    BASE_URL = "https://api.focusnfe.com.br"
    HOMOLOG_URL = "https://homologacao.focusnfe.com.br"
    
    def __init__(self, token: str, ambiente: str = "producao"):
        """
        Inicializa cliente Focus NFe
        
        Args:
            token: Token de autenticação Focus NFe
            ambiente: 'producao' ou 'homologacao'
        """
        self.token = token
        self.base_url = self.BASE_URL if ambiente == "producao" else self.HOMOLOG_URL
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def emitir_cte(self, dados: Dict) -> Dict:
        """
        Emite CT-e via Focus NFe
        
        Args:
            dados: Dicionário com dados do CT-e
            
        Returns:
            Resposta da API com chave, número, etc.
        """
        try:
            payload = self._preparar_payload_cte(dados)
            
            response = requests.post(
                f"{self.base_url}/v2/cte",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"CT-e emitido com sucesso: {result.get('numero')}")
            
            return {
                "success": True,
                "numero": result.get("numero"),
                "chave": result.get("chave_nfe"),
                "status": result.get("status"),
                "protocolo": result.get("protocolo"),
                "data_emissao": result.get("data_emissao"),
                "url_danfe": result.get("caminho_danfe"),
                "xml": result.get("caminho_xml_nota_fiscal"),
                "ref": result.get("ref")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao emitir CT-e: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao comunicar com Focus NFe"
            }
        except Exception as e:
            logger.error(f"Erro inesperado ao emitir CT-e: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Erro interno ao processar CT-e"
            }
    
    def _preparar_payload_cte(self, dados: Dict) -> Dict:
        """Prepara payload no formato Focus NFe"""
        
        return {
            "natureza_operacao": dados.get("natureza_operacao", "PRESTACAO DE SERVICO DE TRANSPORTE"),
            "tipo_documento": "0",
            "modelo": "57",
            "serie": dados.get("serie", "1"),
            "numero": dados.get("numero"),
            "data_emissao": dados.get("data_emissao", datetime.now().isoformat()),
            "tipo_impressao": "1",
            "forma_emissao": "1",
            "ambiente": "2" if "homolog" in self.base_url else "1",
            "tipo_cte": "0",
            "modal": dados.get("modal", "01"),
            "tipo_servico": "0",
            "tomador": {
                "tipo": dados["tomador"]["tipo"],
                "cnpj_cpf": dados["tomador"]["documento"],
                "inscricao_estadual": dados["tomador"].get("ie", ""),
                "nome": dados["tomador"]["nome"],
                "endereco": dados["tomador"]["endereco"],
                "complemento": dados["tomador"].get("complemento", ""),
                "numero": dados["tomador"]["numero"],
                "bairro": dados["tomador"]["bairro"],
                "cidade": dados["tomador"]["cidade"],
                "uf": dados["tomador"]["uf"],
                "cep": dados["tomador"]["cep"],
                "telefone": dados["tomador"].get("telefone", ""),
                "email": dados["tomador"].get("email", "")
            },
            "remetente": {
                "cnpj_cpf": dados["remetente"]["documento"],
                "inscricao_estadual": dados["remetente"].get("ie", ""),
                "nome": dados["remetente"]["nome"],
                "endereco": dados["remetente"]["endereco"],
                "numero": dados["remetente"]["numero"],
                "bairro": dados["remetente"]["bairro"],
                "cidade": dados["remetente"]["cidade"],
                "uf": dados["remetente"]["uf"],
                "cep": dados["remetente"]["cep"]
            },
            "destinatario": {
                "cnpj_cpf": dados["destinatario"]["documento"],
                "inscricao_estadual": dados["destinatario"].get("ie", ""),
                "nome": dados["destinatario"]["nome"],
                "endereco": dados["destinatario"]["endereco"],
                "numero": dados["destinatario"]["numero"],
                "bairro": dados["destinatario"]["bairro"],
                "cidade": dados["destinatario"]["cidade"],
                "uf": dados["destinatario"]["uf"],
                "cep": dados["destinatario"]["cep"]
            },
            "valores": {
                "valor_total": str(dados["valores"]["valor_total"]),
                "valor_receber": str(dados["valores"]["valor_receber"]),
                "valor_total_carga": str(dados["valores"].get("valor_carga", dados["valores"]["valor_total"])),
                "produto_predominante": dados["valores"].get("produto_predominante", "MERCADORIA"),
                "quantidades": [
                    {
                        "codigo_unidade_medida": "01",
                        "tipo_medida": "PESO BRUTO",
                        "quantidade": str(dados["valores"]["peso_kg"])
                    }
                ]
            },
            "informacoes_carga": {
                "valor": str(dados["valores"].get("valor_carga", dados["valores"]["valor_total"])),
                "produto_predominante": dados["valores"].get("produto_predominante", "MERCADORIA"),
                "quantidades": [
                    {
                        "codigo_unidade_medida": "01",
                        "tipo_medida": "PESO BRUTO",
                        "quantidade": str(dados["valores"]["peso_kg"])
                    }
                ]
            },
            "componentes_valor": [
                {
                    "nome": "Frete",
                    "valor": str(dados["valores"]["valor_total"])
                }
            ],
            "icms": {
                "situacao_tributaria": dados.get("icms_situacao", "00"),
                "valor_base_calculo": str(dados["valores"]["valor_total"]),
                "aliquota": dados.get("icms_aliquota", "0.00"),
                "valor": dados.get("icms_valor", "0.00")
            },
            "modal_rodoviario": {
                "rntrc": dados.get("rntrc", ""),
                "ciot": dados.get("ciot", ""),
                "veiculo": {
                    "placa": dados["veiculo"]["placa"],
                    "renavam": dados["veiculo"].get("renavam", ""),
                    "uf": dados["veiculo"]["uf"],
                    "tipo": dados["veiculo"].get("tipo", "02")
                }
            }
        }
    
    def consultar_cte(self, ref: str) -> Dict:
        """Consulta status de um CT-e"""
        try:
            response = requests.get(
                f"{self.base_url}/v2/cte/{ref}",
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao consultar CT-e {ref}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def cancelar_cte(self, ref: str, justificativa: str) -> Dict:
        """Cancela um CT-e"""
        try:
            if len(justificativa) < 15:
                return {
                    "success": False,
                    "error": "Justificativa deve ter no mínimo 15 caracteres"
                }
            
            payload = {"justificativa": justificativa}
            
            response = requests.delete(
                f"{self.base_url}/v2/cte/{ref}",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao cancelar CT-e {ref}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def emitir_mdfe(self, dados: Dict) -> Dict:
        """Emite MDF-e"""
        try:
            payload = self._preparar_payload_mdfe(dados)
            
            response = requests.post(
                f"{self.base_url}/v2/mdfe",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"MDF-e emitido com sucesso: {result.get('numero')}")
            
            return {
                "success": True,
                "numero": result.get("numero"),
                "chave": result.get("chave_nfe"),
                "status": result.get("status"),
                "protocolo": result.get("protocolo"),
                "ref": result.get("ref")
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao emitir MDF-e: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _preparar_payload_mdfe(self, dados: Dict) -> Dict:
        """Prepara payload MDF-e"""
        return {
            "serie": dados.get("serie", "1"),
            "numero": dados.get("numero"),
            "data_emissao": dados.get("data_emissao", datetime.now().isoformat()),
            "ambiente": "2" if "homolog" in self.base_url else "1",
            "modal": dados.get("modal", "1"),
            "tipo_emitente": "1",
            "percurso": dados.get("percurso", []),
            "documentos": dados.get("documentos", []),
            "veiculo": {
                "placa": dados["veiculo"]["placa"],
                "renavam": dados["veiculo"].get("renavam", ""),
                "uf": dados["veiculo"]["uf"],
                "tipo": dados["veiculo"].get("tipo", "02")
            },
            "condutores": dados.get("condutores", [])
        }
    
    def encerrar_mdfe(self, ref: str, uf: str, cidade_codigo: str) -> Dict:
        """Encerra um MDF-e"""
        try:
            payload = {
                "uf": uf,
                "codigo_municipio": cidade_codigo,
                "data_encerramento": datetime.now().isoformat()
            }
            
            response = requests.patch(
                f"{self.base_url}/v2/mdfe/{ref}/encerramento",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "data": response.json()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao encerrar MDF-e {ref}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def download_pdf(self, ref: str, tipo: str = "cte") -> Optional[bytes]:
        """Baixa PDF (DACTE ou DAMDFE)"""
        try:
            response = requests.get(
                f"{self.base_url}/v2/{tipo}/{ref}.pdf",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return response.content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar PDF {tipo}/{ref}: {e}")
            return None
    
    def download_xml(self, ref: str, tipo: str = "cte") -> Optional[str]:
        """Baixa XML do documento"""
        try:
            response = requests.get(
                f"{self.base_url}/v2/{tipo}/{ref}.xml",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar XML {tipo}/{ref}: {e}")
            return None
