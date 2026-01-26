"""
Pedido Repository - Implementação concreta do repository de pedidos
"""
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.pedido import Pedido, StatusPedido
from domain.interfaces.repositories import IPedidoRepository
from domain.value_objects.endereco import Endereco

from ..persistence.models import PedidoModel


class PedidoRepository(IPedidoRepository):
    """Implementação do repository de pedidos usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        self._session = session
    
    async def get_by_id(self, id: UUID) -> Optional[Pedido]:
        model = self._session.query(PedidoModel).filter(PedidoModel.id == id).first()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Pedido]:
        models = (
            self._session.query(PedidoModel)
            .order_by(PedidoModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def add(self, entity: Pedido) -> Pedido:
        model = self._to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    async def update(self, entity: Pedido) -> Pedido:
        model = self._session.query(PedidoModel).filter(PedidoModel.id == entity.id).first()
        if model:
            model.status = entity.status.value
            model.motorista_id = entity.motorista_id
            model.veiculo_id = entity.veiculo_id
            model.data_coleta_realizada = entity.data_coleta_realizada
            model.data_entrega_realizada = entity.data_entrega_realizada
            model.cte_numero = entity.cte_numero
            model.cte_chave = entity.cte_chave
            model.observacoes = entity.observacoes
            self._session.commit()
            self._session.refresh(model)
        return self._to_entity(model)
    
    async def delete(self, id: UUID) -> bool:
        model = self._session.query(PedidoModel).filter(PedidoModel.id == id).first()
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False
    
    async def count(self) -> int:
        return self._session.query(PedidoModel).count()
    
    async def get_by_numero(self, numero: str) -> Optional[Pedido]:
        model = self._session.query(PedidoModel).filter(PedidoModel.numero == numero).first()
        return self._to_entity(model) if model else None
    
    async def get_by_cliente(self, cliente_id: UUID, skip: int = 0, limit: int = 100) -> List[Pedido]:
        models = (
            self._session.query(PedidoModel)
            .filter(PedidoModel.cliente_id == cliente_id)
            .order_by(PedidoModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def get_by_status(self, status: StatusPedido, skip: int = 0, limit: int = 100) -> List[Pedido]:
        models = (
            self._session.query(PedidoModel)
            .filter(PedidoModel.status == status.value)
            .order_by(PedidoModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def get_by_motorista(self, motorista_id: UUID, skip: int = 0, limit: int = 100) -> List[Pedido]:
        models = (
            self._session.query(PedidoModel)
            .filter(PedidoModel.motorista_id == motorista_id)
            .order_by(PedidoModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def get_em_transito(self) -> List[Pedido]:
        status_em_movimento = [
            StatusPedido.COLETADO.value,
            StatusPedido.EM_TRANSITO.value,
            StatusPedido.EM_TRANSFERENCIA.value,
            StatusPedido.SAIU_PARA_ENTREGA.value,
        ]
        models = (
            self._session.query(PedidoModel)
            .filter(PedidoModel.status.in_(status_em_movimento))
            .order_by(PedidoModel.data_coleta_realizada)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    def _to_entity(self, model: PedidoModel) -> Pedido:
        """Converte model para entidade de domínio"""
        origem = Endereco(
            logradouro=model.origem.get("logradouro", ""),
            numero=model.origem.get("numero", ""),
            bairro=model.origem.get("bairro", ""),
            cidade=model.origem.get("cidade", ""),
            uf=model.origem.get("uf", ""),
            cep=model.origem.get("cep", ""),
            complemento=model.origem.get("complemento"),
        )
        
        destino = Endereco(
            logradouro=model.destino.get("logradouro", ""),
            numero=model.destino.get("numero", ""),
            bairro=model.destino.get("bairro", ""),
            cidade=model.destino.get("cidade", ""),
            uf=model.destino.get("uf", ""),
            cep=model.destino.get("cep", ""),
            complemento=model.destino.get("complemento"),
        )
        
        return Pedido(
            cliente_id=model.cliente_id,
            cotacao_id=model.cotacao_id,
            origem=origem,
            destino=destino,
            numero=model.numero,
            status=StatusPedido(model.status),
            peso_kg=model.peso_kg,
            volume_m3=model.volume_m3,
            valor_mercadoria=model.valor_mercadoria,
            descricao_carga=model.descricao_carga,
            valor_frete=model.valor_frete,
            valor_seguro=model.valor_seguro,
            valor_total=model.valor_total,
            data_coleta_prevista=model.data_coleta_prevista,
            data_coleta_realizada=model.data_coleta_realizada,
            data_entrega_prevista=model.data_entrega_prevista,
            data_entrega_realizada=model.data_entrega_realizada,
            motorista_id=model.motorista_id,
            veiculo_id=model.veiculo_id,
            cte_numero=model.cte_numero,
            cte_chave=model.cte_chave,
            nfe_chave=model.nfe_chave,
            observacoes=model.observacoes,
            _id=model.id,
            _created_at=model.created_at,
            _updated_at=model.updated_at,
        )
    
    def _to_model(self, entity: Pedido) -> PedidoModel:
        """Converte entidade de domínio para model"""
        return PedidoModel(
            id=entity.id,
            numero=entity.numero,
            cliente_id=entity.cliente_id,
            cotacao_id=entity.cotacao_id,
            origem=self._endereco_to_dict(entity.origem),
            destino=self._endereco_to_dict(entity.destino),
            status=entity.status.value,
            peso_kg=entity.peso_kg,
            volume_m3=entity.volume_m3,
            valor_mercadoria=entity.valor_mercadoria,
            descricao_carga=entity.descricao_carga,
            valor_frete=entity.valor_frete,
            valor_seguro=entity.valor_seguro,
            valor_total=entity.valor_total,
            data_coleta_prevista=entity.data_coleta_prevista,
            data_coleta_realizada=entity.data_coleta_realizada,
            data_entrega_prevista=entity.data_entrega_prevista,
            data_entrega_realizada=entity.data_entrega_realizada,
            motorista_id=entity.motorista_id,
            veiculo_id=entity.veiculo_id,
            cte_numero=entity.cte_numero,
            cte_chave=entity.cte_chave,
            nfe_chave=entity.nfe_chave,
            observacoes=entity.observacoes,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _endereco_to_dict(self, endereco: Endereco) -> dict:
        return {
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "bairro": endereco.bairro,
            "cidade": endereco.cidade,
            "uf": endereco.uf,
            "cep": endereco.cep,
            "complemento": endereco.complemento,
        }
