"""
Cliente Repository - Implementação concreta do repository de clientes
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.entities.cliente import Cliente
from domain.interfaces.repositories import IClienteRepository
from domain.value_objects.documento import CNPJ, CPF
from domain.value_objects.endereco import Endereco

from ..persistence.models import ClienteModel


class ClienteRepository(IClienteRepository):
    """Implementação do repository de clientes usando SQLAlchemy"""
    
    def __init__(self, session: Session):
        self._session = session
    
    async def get_by_id(self, id: UUID) -> Optional[Cliente]:
        model = self._session.query(ClienteModel).filter(ClienteModel.id == id).first()
        return self._to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        models = (
            self._session.query(ClienteModel)
            .order_by(ClienteModel.razao_social)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def add(self, entity: Cliente) -> Cliente:
        model = self._to_model(entity)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    async def update(self, entity: Cliente) -> Cliente:
        model = self._session.query(ClienteModel).filter(ClienteModel.id == entity.id).first()
        if model:
            model.razao_social = entity.razao_social
            model.nome_fantasia = entity.nome_fantasia
            model.documento = entity.documento.valor if entity.documento else None
            model.email = entity.email
            model.telefone = entity.telefone
            model.inscricao_estadual = entity.inscricao_estadual
            model.ativo = entity.ativo
            model.observacoes = entity.observacoes
            model.endereco = self._endereco_to_dict(entity.endereco) if entity.endereco else None
            self._session.commit()
            self._session.refresh(model)
        return self._to_entity(model)
    
    async def delete(self, id: UUID) -> bool:
        model = self._session.query(ClienteModel).filter(ClienteModel.id == id).first()
        if model:
            self._session.delete(model)
            self._session.commit()
            return True
        return False
    
    async def count(self) -> int:
        return self._session.query(ClienteModel).count()
    
    async def get_by_documento(self, documento: str) -> Optional[Cliente]:
        doc_limpo = "".join(filter(str.isdigit, documento))
        model = self._session.query(ClienteModel).filter(ClienteModel.documento == doc_limpo).first()
        return self._to_entity(model) if model else None
    
    async def get_by_email(self, email: str) -> Optional[Cliente]:
        model = self._session.query(ClienteModel).filter(ClienteModel.email == email).first()
        return self._to_entity(model) if model else None
    
    async def search(self, termo: str, skip: int = 0, limit: int = 100) -> List[Cliente]:
        termo_like = f"%{termo}%"
        models = (
            self._session.query(ClienteModel)
            .filter(
                or_(
                    ClienteModel.razao_social.ilike(termo_like),
                    ClienteModel.nome_fantasia.ilike(termo_like),
                    ClienteModel.documento.ilike(termo_like),
                    ClienteModel.email.ilike(termo_like),
                )
            )
            .order_by(ClienteModel.razao_social)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    async def get_ativos(self, skip: int = 0, limit: int = 100) -> List[Cliente]:
        models = (
            self._session.query(ClienteModel)
            .filter(ClienteModel.ativo == True)
            .order_by(ClienteModel.razao_social)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_entity(m) for m in models]
    
    def _to_entity(self, model: ClienteModel) -> Cliente:
        """Converte model para entidade de domínio"""
        documento = None
        if model.documento:
            if len(model.documento) == 14:
                documento = CNPJ(model.documento)
            elif len(model.documento) == 11:
                documento = CPF(model.documento)
        
        endereco = None
        if model.endereco:
            endereco = Endereco(
                logradouro=model.endereco.get("logradouro", ""),
                numero=model.endereco.get("numero", ""),
                bairro=model.endereco.get("bairro", ""),
                cidade=model.endereco.get("cidade", ""),
                uf=model.endereco.get("uf", ""),
                cep=model.endereco.get("cep", ""),
                complemento=model.endereco.get("complemento"),
            )
        
        return Cliente(
            razao_social=model.razao_social,
            nome_fantasia=model.nome_fantasia,
            documento=documento,
            email=model.email,
            telefone=model.telefone,
            endereco=endereco,
            inscricao_estadual=model.inscricao_estadual,
            ativo=model.ativo,
            observacoes=model.observacoes,
            _id=model.id,
            _created_at=model.created_at,
            _updated_at=model.updated_at,
        )
    
    def _to_model(self, entity: Cliente) -> ClienteModel:
        """Converte entidade de domínio para model"""
        return ClienteModel(
            id=entity.id,
            razao_social=entity.razao_social,
            nome_fantasia=entity.nome_fantasia,
            documento=entity.documento.valor if entity.documento else None,
            email=entity.email,
            telefone=entity.telefone,
            inscricao_estadual=entity.inscricao_estadual,
            ativo=entity.ativo,
            observacoes=entity.observacoes,
            endereco=self._endereco_to_dict(entity.endereco) if entity.endereco else None,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def _endereco_to_dict(self, endereco: Endereco) -> dict:
        """Converte Endereco para dict para persistir como JSON"""
        return {
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "bairro": endereco.bairro,
            "cidade": endereco.cidade,
            "uf": endereco.uf,
            "cep": endereco.cep,
            "complemento": endereco.complemento,
        }
