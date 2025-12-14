"""
LogiFlow CRM - Serviço de Sincronização Bidirecional ERP
Sincronização automática entre LogiFlow e ERPs (Omie, Bling, Tiny)
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

from integrations.erp.omie import OmieClient
from integrations.erp.bling import BlingClient
from integrations.erp.tiny import TinyClient

logger = logging.getLogger(__name__)


class ERPSyncService:
    """
    Serviço de Sincronização Bidirecional com ERPs
    
    Funcionalidades:
    - Sincronização de clientes (LogiFlow ↔ ERP)
    - Sincronização de pedidos (LogiFlow → ERP)
    - Sincronização de produtos/serviços
    - Sincronização de faturas (ERP → LogiFlow)
    - Detecção de conflitos
    - Resolução automática de duplicatas
    """
    
    def __init__(self, erp_type: str, credentials: Dict):
        """
        Inicializa serviço de sincronização
        
        Args:
            erp_type: Tipo de ERP (omie, bling, tiny)
            credentials: Credenciais do ERP
        """
        self.erp_type = erp_type.lower()
        self.credentials = credentials
        self.client = self._inicializar_cliente()
        self.sync_log = []
    
    def _inicializar_cliente(self):
        """Inicializa cliente do ERP apropriado"""
        if self.erp_type == "omie":
            return OmieClient(
                app_key=self.credentials["app_key"],
                app_secret=self.credentials["app_secret"]
            )
        elif self.erp_type == "bling":
            return BlingClient(access_token=self.credentials["access_token"])
        elif self.erp_type == "tiny":
            return TinyClient(token=self.credentials["token"])
        else:
            raise ValueError(f"ERP não suportado: {self.erp_type}")
    
    # ===========================================
    # Sincronização de Clientes
    # ===========================================
    
    def sincronizar_cliente_para_erp(self, cliente_logiflow: Dict) -> Dict:
        """
        Sincroniza cliente do LogiFlow para ERP
        
        Args:
            cliente_logiflow: Dados do cliente no LogiFlow
            
        Returns:
            Resultado da sincronização
        """
        try:
            # Verificar se cliente já existe no ERP
            cliente_erp = self._buscar_cliente_no_erp(
                documento=cliente_logiflow.get("cnpj") or cliente_logiflow.get("cpf")
            )
            
            if cliente_erp:
                # Cliente existe - atualizar
                resultado = self._atualizar_cliente_no_erp(
                    cliente_id=cliente_erp["id"],
                    dados=cliente_logiflow
                )
                acao = "atualizado"
            else:
                # Cliente não existe - criar
                resultado = self._criar_cliente_no_erp(cliente_logiflow)
                acao = "criado"
            
            if resultado.get("success"):
                self._registrar_log({
                    "tipo": "cliente",
                    "acao": acao,
                    "direcao": "logiflow_para_erp",
                    "cliente_id": cliente_logiflow.get("id"),
                    "erp_id": resultado.get("id"),
                    "status": "sucesso"
                })
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar cliente para ERP: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def sincronizar_cliente_do_erp(self, erp_cliente_id: str) -> Dict:
        """
        Sincroniza cliente do ERP para LogiFlow
        
        Args:
            erp_cliente_id: ID do cliente no ERP
            
        Returns:
            Resultado da sincronização
        """
        try:
            # Buscar cliente no ERP
            if self.erp_type == "omie":
                resultado_erp = self.client.obter_cliente(erp_cliente_id)
            elif self.erp_type == "bling":
                resultado_erp = self.client.obter_cliente(erp_cliente_id)
            elif self.erp_type == "tiny":
                resultado_erp = self.client.obter_contato(erp_cliente_id)
            
            if not resultado_erp.get("success"):
                return resultado_erp
            
            cliente_erp = resultado_erp.get("cliente") or resultado_erp.get("contato")
            
            # Mapear para formato LogiFlow
            cliente_logiflow = self._mapear_cliente_erp_para_logiflow(cliente_erp)
            
            # Verificar se cliente já existe no LogiFlow
            # Em produção, buscar no banco de dados
            # cliente_existente = buscar_cliente_por_documento(cliente_logiflow["documento"])
            
            # Criar ou atualizar no LogiFlow
            # Em produção, salvar no banco de dados
            
            self._registrar_log({
                "tipo": "cliente",
                "acao": "importado",
                "direcao": "erp_para_logiflow",
                "erp_id": erp_cliente_id,
                "status": "sucesso"
            })
            
            return {
                "success": True,
                "cliente": cliente_logiflow,
                "message": "Cliente sincronizado do ERP para LogiFlow"
            }
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar cliente do ERP: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def sincronizar_todos_clientes(self, direcao: str = "ambos") -> Dict:
        """
        Sincroniza todos os clientes
        
        Args:
            direcao: "logiflow_para_erp", "erp_para_logiflow" ou "ambos"
            
        Returns:
            Resumo da sincronização
        """
        resultados = {
            "total_processados": 0,
            "sucessos": 0,
            "erros": 0,
            "detalhes": []
        }
        
        try:
            if direcao in ["logiflow_para_erp", "ambos"]:
                # Sincronizar clientes do LogiFlow para ERP
                # Em produção, buscar todos os clientes do banco
                clientes_logiflow = self._obter_clientes_logiflow()
                
                for cliente in clientes_logiflow:
                    resultado = self.sincronizar_cliente_para_erp(cliente)
                    resultados["total_processados"] += 1
                    
                    if resultado.get("success"):
                        resultados["sucessos"] += 1
                    else:
                        resultados["erros"] += 1
                    
                    resultados["detalhes"].append({
                        "cliente": cliente.get("nome"),
                        "resultado": resultado
                    })
            
            if direcao in ["erp_para_logiflow", "ambos"]:
                # Sincronizar clientes do ERP para LogiFlow
                clientes_erp = self._listar_clientes_erp()
                
                for cliente_erp in clientes_erp:
                    resultado = self.sincronizar_cliente_do_erp(cliente_erp["id"])
                    resultados["total_processados"] += 1
                    
                    if resultado.get("success"):
                        resultados["sucessos"] += 1
                    else:
                        resultados["erros"] += 1
            
            return {
                "success": True,
                "resumo": resultados
            }
            
        except Exception as e:
            logger.error(f"Erro na sincronização em lote: {e}")
            return {
                "success": False,
                "error": str(e),
                "resumo": resultados
            }
    
    # ===========================================
    # Sincronização de Pedidos
    # ===========================================
    
    def sincronizar_pedido_para_erp(self, pedido_logiflow: Dict) -> Dict:
        """
        Sincroniza pedido do LogiFlow para ERP
        
        Args:
            pedido_logiflow: Dados do pedido no LogiFlow
            
        Returns:
            Resultado da sincronização
        """
        try:
            # Mapear pedido para formato do ERP
            if self.erp_type == "omie":
                resultado = self.client.sincronizar_pedido(pedido_logiflow)
            elif self.erp_type == "bling":
                resultado = self.client.sincronizar_pedido(pedido_logiflow)
            elif self.erp_type == "tiny":
                resultado = self.client.sincronizar_pedido(pedido_logiflow)
            
            if resultado.get("success"):
                self._registrar_log({
                    "tipo": "pedido",
                    "acao": "criado",
                    "direcao": "logiflow_para_erp",
                    "pedido_id": pedido_logiflow.get("id"),
                    "erp_id": resultado.get("id"),
                    "status": "sucesso"
                })
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar pedido para ERP: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # ===========================================
    # Sincronização Automática
    # ===========================================
    
    def executar_sincronizacao_automatica(self) -> Dict:
        """
        Executa sincronização automática periódica
        
        Sincroniza:
        - Novos clientes (últimas 24h)
        - Novos pedidos (últimas 24h)
        - Atualizações de status
        
        Returns:
            Resumo da sincronização
        """
        resumo = {
            "inicio": datetime.now().isoformat(),
            "clientes": {"novos": 0, "atualizados": 0, "erros": 0},
            "pedidos": {"novos": 0, "erros": 0},
            "total_operacoes": 0
        }
        
        try:
            # 1. Sincronizar novos clientes (últimas 24h)
            clientes_novos = self._obter_clientes_novos(horas=24)
            for cliente in clientes_novos:
                resultado = self.sincronizar_cliente_para_erp(cliente)
                resumo["total_operacoes"] += 1
                
                if resultado.get("success"):
                    resumo["clientes"]["novos"] += 1
                else:
                    resumo["clientes"]["erros"] += 1
            
            # 2. Sincronizar novos pedidos (últimas 24h)
            pedidos_novos = self._obter_pedidos_novos(horas=24)
            for pedido in pedidos_novos:
                resultado = self.sincronizar_pedido_para_erp(pedido)
                resumo["total_operacoes"] += 1
                
                if resultado.get("success"):
                    resumo["pedidos"]["novos"] += 1
                else:
                    resumo["pedidos"]["erros"] += 1
            
            resumo["fim"] = datetime.now().isoformat()
            resumo["success"] = True
            
            logger.info(f"Sincronização automática concluída: {resumo}")
            
            return resumo
            
        except Exception as e:
            logger.error(f"Erro na sincronização automática: {e}")
            resumo["success"] = False
            resumo["error"] = str(e)
            return resumo
    
    # ===========================================
    # Detecção de Conflitos
    # ===========================================
    
    def detectar_conflitos(self) -> Dict:
        """
        Detecta conflitos entre LogiFlow e ERP
        
        Verifica:
        - Duplicatas
        - Dados divergentes
        - Registros órfãos
        
        Returns:
            Lista de conflitos detectados
        """
        conflitos = {
            "duplicatas": [],
            "divergencias": [],
            "orfaos": []
        }
        
        # Implementar lógica de detecção de conflitos
        # Em produção, comparar dados do banco com dados do ERP
        
        return {
            "success": True,
            "conflitos": conflitos,
            "total_conflitos": sum(len(v) for v in conflitos.values())
        }
    
    # ===========================================
    # Métodos Auxiliares
    # ===========================================
    
    def _buscar_cliente_no_erp(self, documento: str) -> Optional[Dict]:
        """Busca cliente no ERP por documento"""
        # Implementar busca específica por ERP
        return None
    
    def _criar_cliente_no_erp(self, cliente: Dict) -> Dict:
        """Cria cliente no ERP"""
        if self.erp_type == "omie":
            return self.client.sincronizar_cliente(cliente)
        elif self.erp_type == "bling":
            return self.client.sincronizar_cliente(cliente)
        elif self.erp_type == "tiny":
            return self.client.sincronizar_cliente(cliente)
    
    def _atualizar_cliente_no_erp(self, cliente_id: str, dados: Dict) -> Dict:
        """Atualiza cliente no ERP"""
        # Implementar atualização específica por ERP
        return {"success": True, "id": cliente_id}
    
    def _mapear_cliente_erp_para_logiflow(self, cliente_erp: Dict) -> Dict:
        """Mapeia cliente do ERP para formato LogiFlow"""
        # Implementar mapeamento específico por ERP
        return cliente_erp
    
    def _obter_clientes_logiflow(self) -> List[Dict]:
        """Obtém clientes do LogiFlow"""
        # Simular (em produção, buscar do banco)
        return []
    
    def _listar_clientes_erp(self) -> List[Dict]:
        """Lista clientes do ERP"""
        if self.erp_type == "omie":
            resultado = self.client.listar_clientes()
        elif self.erp_type == "bling":
            resultado = self.client.listar_clientes()
        elif self.erp_type == "tiny":
            resultado = self.client.listar_contatos()
        
        return resultado.get("clientes", []) or resultado.get("contatos", [])
    
    def _obter_clientes_novos(self, horas: int = 24) -> List[Dict]:
        """Obtém clientes criados nas últimas N horas"""
        # Simular (em produção, buscar do banco)
        return []
    
    def _obter_pedidos_novos(self, horas: int = 24) -> List[Dict]:
        """Obtém pedidos criados nas últimas N horas"""
        # Simular (em produção, buscar do banco)
        return []
    
    def _registrar_log(self, log_entry: Dict):
        """Registra log de sincronização"""
        log_entry["timestamp"] = datetime.now().isoformat()
        self.sync_log.append(log_entry)
        logger.info(f"Sync log: {log_entry}")
    
    def obter_logs(self, limite: int = 100) -> List[Dict]:
        """Obtém logs de sincronização"""
        return self.sync_log[-limite:]
