"""
Cotação Repository - Implementação concreta do repository de cotações
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from domain.entities.cotacao import Cotacao, ItemCotacao, StatusCotacao, TipoFrete, TipoCarga
from domain.interfaces.repositories import ICotacaoRepository
from domain.value_objects.endereco import Endereco

from ..persistence.models import CotacaoModel


class CotacaoRepository(ICotacaoRepository):
    """Implementação do repository de cotações usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        self._session = session
    
    async def get_by_id(self, id: UUID) -> Optional[Cotacao]:
        model = self._session.query(CotacaoModel).filter(CotacaoModel.id == id).first()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Cotacao]:
        models = (
            self._session.query(CotacaoModel)
            .order_by(CotacaoModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def add(self, entity: Cotacao) -> Cotacao:
        model = self._to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    async def update(self, entity: Cotacao) -> Cotacao:
        model = self._session.query(CotacaoModel).filter(CotacaoModel.id == entity.id).first()
        if model:
            model.status = entity.status.value
            model.valor_frete = entity.valor_frete
            model.valor_seguro = entity.valor_seguro
            model.valor_outros = entity.valor_outros
            model.desconto = entity.desconto
            model.validade = entity.validade
            model.observacoes = entity.observacoes
            self._session.commit()
            self._session.refresh(model)
        return self._to_entity(model)
    
    async def delete(self, id: UUID) -> bool:
        model = self._session.query(CotacaoModel).filter(CotacaoModel.id == id).first()
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False
    
    async def count(self) -> int:
        return self._session.query(CotacaoModel).count()
    
    async def get_by_numero(self, numero: str) -> Optional[Cotacao]:
        model = self._session.query(CotacaoModel).filter(CotacaoModel.numero == numero).first()
        return self._to_entity(model) if model else None
    
    async def get_by_cliente(self, cliente_id: UUID, skip: int = 0, limit: int = 100) -> List[Cotacao]:
        models = (
            self._session.query(CotacaoModel)
            .filter(CotacaoModel.cliente_id == cliente_id)
            .order_by(CotacaoModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def get_by_status(self, status: StatusCotacao, skip: int = 0, limit: int = 100) -> List[Cotacao]:
        models = (
            self._session.query(CotacaoModel)
            .filter(CotacaoModel.status == status.value)
            .order_by(CotacaoModel.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def get_expiradas(self) -> List[Cotacao]:
        models = (
            self._session.query(CotacaoModel)
            .filter(
                CotacaoModel.status == StatusCotacao.ENVIADA.value,
                CotacaoModel.validade < date.today()
            )
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    def _to_entity(self, model: CotacaoModel) -> Cotacao:
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
        
        itens = [
            ItemCotacao(
                descricao=item.get("descricao", ""),
                quantidade=item.get("quantidade", 1),
                peso_kg=Decimal(str(item.get("peso_kg", 0))),
                volume_m3=Decimal(str(item.get("volume_m3", 0))) if item.get("volume_m3") else None,
                valor_mercadoria=Decimal(str(item.get("valor_mercadoria", 0))) if item.get("valor_mercadoria") else None,
                observacao=item.get("observacao"),
            )
            for item in model.itens
        ]
        
        return Cotacao(
            cliente_id=model.cliente_id,
            origem=origem,
            destino=destino,
            itens=itens,
            numero=model.numero,
            tipo_frete=TipoFrete(model.tipo_frete),
            tipo_carga=TipoCarga(model.tipo_carga),
            status=StatusCotacao(model.status),
            valor_frete=model.valor_frete,
            valor_seguro=model.valor_seguro,
            valor_outros=model.valor_outros,
            desconto=model.desconto,
            validade=model.validade,
            observacoes=model.observacoes,
            criado_por=model.criado_por,
            _id=model.id,
            _created_at=model.created_at,
            _updated_at=model.updated_at,
        )
    
    def _to_model(self, entity: Cotacao) -> CotacaoModel:
        """Converte entidade de domínio para model"""
        return CotacaoModel(
            id=entity.id,
            numero=entity.numero,
            cliente_id=entity.cliente_id,
            origem=self._endereco_to_dict(entity.origem),
            destino=self._endereco_to_dict(entity.destino),
            itens=[self._item_to_dict(i) for i in entity.itens],
            tipo_frete=entity.tipo_frete.value,
            tipo_carga=entity.tipo_carga.value,
            status=entity.status.value,
            valor_frete=entity.valor_frete,
            valor_seguro=entity.valor_seguro,
            valor_outros=entity.valor_outros,
            desconto=entity.desconto,
            validade=entity.validade,
            observacoes=entity.observacoes,
            criado_por=entity.criado_por,
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
    
    def _item_to_dict(self, item: ItemCotacao) -> dict:
        return {
            "descricao": item.descricao,
            "quantidade": item.quantidade,
            "peso_kg": float(item.peso_kg),
            "volume_m3": float(item.volume_m3) if item.volume_m3 else None,
            "valor_mercadoria": float(item.valor_mercadoria) if item.valor_mercadoria else None,
            "observacao": item.observacao,
        }
