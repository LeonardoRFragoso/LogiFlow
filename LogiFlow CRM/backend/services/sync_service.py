"""
LogiFlow CRM - Serviço de Sincronização Bidirecional
=====================================================
Sincroniza dados entre banco local e SuiteCRM (Arquitetura Híbrida - Opção 1)
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal
from services.suitecrm_service import suitecrm_service
from models import Pedido, Motorista, Veiculo, Cliente, Cotacao


class SyncService:
    """
    Gerencia sincronização bidirecional entre banco local e SuiteCRM
    
    Estratégia:
    - Escrita: Local + SuiteCRM simultâneo
    - Leitura: Apenas local (performance)
    - Sync: Job periódico (5-15 min) ou manual
    """
    
    def __init__(self):
        self.sync_interval_minutes = 10
        self.last_sync: Dict[str, datetime] = {}
        
    # ========== Mapeamento de Módulos ==========
    
    MODULE_MAPPING = {
        "pedidos": {
            "local_model": Pedido,
            "suitecrm_module": "LF_PedidosFrete",
            "fields_map": {
                "id": "id",
                "numero_pedido": "numero_pedido",
                "cliente_id": "account_id_c",
                "status": "status_operacional",
                "motorista_id": "motorista_id_c",
                "veiculo_id": "veiculo_id_c",
                "origem_cidade": "origem_cidade",
                "destino_cidade": "destino_cidade",
                "peso_total_kg": "peso_total",
                "valor_frete": "valor_frete",
                "data_coleta_prevista": "data_coleta",
                "data_entrega_prevista": "previsao_entrega",
            }
        },
        "motoristas": {
            "local_model": Motorista,
            "suitecrm_module": "LF_Motoristas",
            "fields_map": {
                "id": "id",
                "nome": "name",
                "cpf": "cpf",
                "cnh": "cnh_numero",
                "categoria_cnh": "categoria_cnh",
                "celular": "celular",
                "email": "email",
                "status": "status",
            }
        },
        "veiculos": {
            "local_model": Veiculo,
            "suitecrm_module": "LF_Veiculos",
            "fields_map": {
                "id": "id",
                "placa": "placa",
                "tipo": "tipo_veiculo",
                "marca": "marca",
                "modelo": "modelo",
                "ano": "ano_fabricacao",
                "capacidade_kg": "capacidade_kg",
                "status": "status",
            }
        },
        "clientes": {
            "local_model": Cliente,
            "suitecrm_module": "Accounts",
            "fields_map": {
                "id": "id",
                "nome": "name",
                "cnpj": "cnpj_c",
                "email": "email1",
                "telefone": "phone_office",
                "cidade": "billing_address_city",
                "uf": "billing_address_state",
            }
        },
        "cotacoes": {
            "local_model": Cotacao,
            "suitecrm_module": "LF_Cotacoes",
            "fields_map": {
                "id": "id",
                "cliente_id": "account_id_c",
                "numero": "numero_cotacao",
                "status": "status",
                "valor_total": "valor_total",
                "origem": "origem",
                "destino": "destino",
            }
        }
    }
    
    # ========== Sincronização Individual ==========
    
    async def sync_to_suitecrm(
        self, 
        module_name: str, 
        local_record: Any,
        operation: str = "create"
    ) -> Optional[Dict[str, Any]]:
        """
        Sincroniza um registro do banco local para o SuiteCRM
        
        Args:
            module_name: Nome do módulo (pedidos, motoristas, etc)
            local_record: Objeto SQLAlchemy do registro local
            operation: create, update, delete
        
        Returns:
            Resposta do SuiteCRM ou None em caso de erro
        """
        try:
            mapping = self.MODULE_MAPPING.get(module_name)
            if not mapping:
                logger.warning(f"Módulo {module_name} não mapeado para sincronização")
                return None
            
            suitecrm_module = mapping["suitecrm_module"]
            fields_map = mapping["fields_map"]
            
            # Converter dados locais para formato SuiteCRM
            suitecrm_data = {}
            for local_field, crm_field in fields_map.items():
                value = getattr(local_record, local_field, None)
                if value is not None:
                    # Converter datetime para ISO string
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    suitecrm_data[crm_field] = value
            
            # Executar operação no SuiteCRM
            if operation == "create":
                result = await suitecrm_service.create_record(
                    suitecrm_module, 
                    suitecrm_data
                )
                logger.info(f"✅ {module_name}/{local_record.id} criado no SuiteCRM")
                
            elif operation == "update":
                result = await suitecrm_service.update_record(
                    suitecrm_module,
                    local_record.id,
                    suitecrm_data
                )
                logger.info(f"✅ {module_name}/{local_record.id} atualizado no SuiteCRM")
                
            elif operation == "delete":
                result = await suitecrm_service.delete_record(
                    suitecrm_module,
                    local_record.id
                )
                logger.info(f"✅ {module_name}/{local_record.id} deletado no SuiteCRM")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao sincronizar {module_name}/{getattr(local_record, 'id', 'unknown')} para SuiteCRM: {e}")
            return None
    
    async def sync_from_suitecrm(
        self,
        module_name: str,
        db: Session,
        since: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Sincroniza registros do SuiteCRM para o banco local
        
        Args:
            module_name: Nome do módulo
            db: Sessão do banco de dados
            since: Sincronizar apenas registros modificados após esta data
        
        Returns:
            Estatísticas da sincronização
        """
        try:
            mapping = self.MODULE_MAPPING.get(module_name)
            if not mapping:
                return {"success": False, "error": f"Módulo {module_name} não mapeado"}
            
            suitecrm_module = mapping["suitecrm_module"]
            local_model = mapping["local_model"]
            fields_map = mapping["fields_map"]
            
            # Buscar registros do SuiteCRM
            result = await suitecrm_service.get_module_records(
                module=suitecrm_module,
                page_size=100
            )
            
            records = result.get("data", [])
            
            created = 0
            updated = 0
            skipped = 0
            
            for record in records:
                try:
                    record_id = record.get("id")
                    attributes = record.get("attributes", {})
                    
                    # Verificar se já existe localmente
                    existing = db.query(local_model).filter(
                        local_model.id == record_id
                    ).first()
                    
                    # Converter dados do SuiteCRM para formato local
                    local_data = {}
                    for local_field, crm_field in fields_map.items():
                        if crm_field in attributes:
                            local_data[local_field] = attributes[crm_field]
                    
                    if existing:
                        # Atualizar registro existente
                        for key, value in local_data.items():
                            setattr(existing, key, value)
                        updated += 1
                    else:
                        # Criar novo registro
                        new_record = local_model(**local_data)
                        db.add(new_record)
                        created += 1
                    
                except Exception as e:
                    logger.error(f"Erro ao processar registro {record.get('id')}: {e}")
                    skipped += 1
                    continue
            
            db.commit()
            
            logger.success(
                f"✅ {module_name}: {created} criados, {updated} atualizados, {skipped} ignorados"
            )
            
            self.last_sync[module_name] = datetime.now()
            
            return {
                "success": True,
                "module": module_name,
                "created": created,
                "updated": updated,
                "skipped": skipped,
                "total": len(records),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao sincronizar {module_name} do SuiteCRM: {e}")
            return {
                "success": False,
                "module": module_name,
                "error": str(e)
            }
    
    # ========== Sincronização em Lote ==========
    
    async def sync_all_to_suitecrm(self, db: Session) -> Dict[str, Any]:
        """Sincroniza todos os módulos locais para o SuiteCRM"""
        results = []
        
        for module_name in self.MODULE_MAPPING.keys():
            try:
                result = await self.sync_module_to_suitecrm(module_name, db)
                results.append(result)
            except Exception as e:
                logger.error(f"Erro ao sincronizar módulo {module_name}: {e}")
                results.append({
                    "module": module_name,
                    "success": False,
                    "error": str(e)
                })
        
        success_count = sum(1 for r in results if r.get("success"))
        
        return {
            "success": True,
            "modules_synced": success_count,
            "total_modules": len(self.MODULE_MAPPING),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    async def sync_module_to_suitecrm(
        self, 
        module_name: str, 
        db: Session
    ) -> Dict[str, Any]:
        """Sincroniza todos os registros de um módulo para o SuiteCRM"""
        try:
            mapping = self.MODULE_MAPPING.get(module_name)
            if not mapping:
                return {"success": False, "error": "Módulo não mapeado"}
            
            local_model = mapping["local_model"]
            
            # Buscar todos os registros locais
            records = db.query(local_model).all()
            
            synced = 0
            errors = 0
            
            for record in records:
                result = await self.sync_to_suitecrm(module_name, record, "update")
                if result:
                    synced += 1
                else:
                    errors += 1
            
            return {
                "success": True,
                "module": module_name,
                "synced": synced,
                "errors": errors,
                "total": len(records)
            }
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar módulo {module_name}: {e}")
            return {
                "success": False,
                "module": module_name,
                "error": str(e)
            }
    
    async def sync_all_from_suitecrm(self, db: Session) -> Dict[str, Any]:
        """Sincroniza todos os módulos do SuiteCRM para o local"""
        results = []
        
        for module_name in self.MODULE_MAPPING.keys():
            result = await self.sync_from_suitecrm(module_name, db)
            results.append(result)
        
        success_count = sum(1 for r in results if r.get("success"))
        total_created = sum(r.get("created", 0) for r in results)
        total_updated = sum(r.get("updated", 0) for r in results)
        
        return {
            "success": True,
            "modules_synced": success_count,
            "total_modules": len(self.MODULE_MAPPING),
            "total_created": total_created,
            "total_updated": total_updated,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    # ========== Utilitários ==========
    
    def needs_sync(self, module_name: str) -> bool:
        """Verifica se um módulo precisa ser sincronizado"""
        last = self.last_sync.get(module_name)
        if not last:
            return True
        
        elapsed = datetime.now() - last
        return elapsed > timedelta(minutes=self.sync_interval_minutes)
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Retorna status da sincronização"""
        return {
            "modules": list(self.MODULE_MAPPING.keys()),
            "last_sync": {
                module: sync_time.isoformat() if sync_time else None
                for module, sync_time in self.last_sync.items()
            },
            "sync_interval_minutes": self.sync_interval_minutes,
            "timestamp": datetime.now().isoformat()
        }


# Instância global
sync_service = SyncService()
