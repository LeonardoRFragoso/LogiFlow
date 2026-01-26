"""
Cliente Use Cases - Casos de uso para operações com clientes
"""
from typing import List, Optional
from uuid import UUID

from domain.entities.cliente import Cliente
from domain.interfaces.repositories import IClienteRepository
from domain.value_objects.documento import CNPJ, CPF
from domain.value_objects.endereco import Endereco
from domain.exceptions import EntityNotFoundException, ValidationException

from ..dtos.cliente_dto import (
    ClienteCreateDTO,
    ClienteUpdateDTO,
    ClienteResponseDTO,
    EnderecoDTO,
)


class CriarClienteUseCase:
    """Caso de uso: Criar novo cliente"""
    
    def __init__(self, cliente_repository: IClienteRepository):
        self._repository = cliente_repository
    
    async def execute(self, dto: ClienteCreateDTO) -> ClienteResponseDTO:
        # Verificar se documento já existe
        existing = await self._repository.get_by_documento(dto.documento)
        if existing:
            raise ValidationException(
                f"Já existe cliente com documento {dto.documento}",
                field="documento"
            )
        
        # Criar value objects
        documento = self._criar_documento(dto.documento)
        endereco = self._criar_endereco(dto.endereco) if dto.endereco else None
        
        # Criar entidade
        cliente = Cliente(
            razao_social=dto.razao_social,
            nome_fantasia=dto.nome_fantasia,
            documento=documento,
            email=dto.email,
            telefone=dto.telefone,
            endereco=endereco,
            inscricao_estadual=dto.inscricao_estadual,
            observacoes=dto.observacoes,
        )
        
        # Persistir
        cliente = await self._repository.add(cliente)
        
        return self._to_response(cliente)
    
    def _criar_documento(self, valor: str) -> CNPJ | CPF:
        if len(valor) == 14:
            return CNPJ(valor)
        elif len(valor) == 11:
            return CPF(valor)
        raise ValidationException(f"Documento inválido: {valor}", field="documento")
    
    def _criar_endereco(self, dto: EnderecoDTO) -> Endereco:
        return Endereco(
            logradouro=dto.logradouro,
            numero=dto.numero,
            bairro=dto.bairro,
            cidade=dto.cidade,
            uf=dto.uf,
            cep=dto.cep,
            complemento=dto.complemento,
        )
    
    def _to_response(self, cliente: Cliente) -> ClienteResponseDTO:
        endereco_dto = None
        if cliente.endereco:
            endereco_dto = EnderecoDTO(
                logradouro=cliente.endereco.logradouro,
                numero=cliente.endereco.numero,
                bairro=cliente.endereco.bairro,
                cidade=cliente.endereco.cidade,
                uf=cliente.endereco.uf,
                cep=cliente.endereco.cep,
                complemento=cliente.endereco.complemento,
            )
        
        return ClienteResponseDTO(
            id=cliente.id,
            razao_social=cliente.razao_social,
            nome_fantasia=cliente.nome_fantasia,
            documento=cliente.documento.valor if cliente.documento else "",
            documento_formatado=str(cliente.documento) if cliente.documento else "",
            email=cliente.email,
            telefone=cliente.telefone,
            endereco=endereco_dto,
            inscricao_estadual=cliente.inscricao_estadual,
            ativo=cliente.ativo,
            observacoes=cliente.observacoes,
            created_at=cliente.created_at,
            updated_at=cliente.updated_at,
        )


class AtualizarClienteUseCase:
    """Caso de uso: Atualizar cliente existente"""
    
    def __init__(self, cliente_repository: IClienteRepository):
        self._repository = cliente_repository
    
    async def execute(self, id: UUID, dto: ClienteUpdateDTO) -> ClienteResponseDTO:
        cliente = await self._repository.get_by_id(id)
        if not cliente:
            raise EntityNotFoundException("Cliente", str(id))
        
        # Atualizar campos
        if dto.razao_social is not None:
            cliente.razao_social = dto.razao_social
        if dto.nome_fantasia is not None:
            cliente.nome_fantasia = dto.nome_fantasia
        if dto.email is not None:
            cliente.email = dto.email
        if dto.telefone is not None:
            cliente.telefone = dto.telefone
        if dto.inscricao_estadual is not None:
            cliente.inscricao_estadual = dto.inscricao_estadual
        if dto.observacoes is not None:
            cliente.observacoes = dto.observacoes
        if dto.ativo is not None:
            if dto.ativo:
                cliente.ativar()
            else:
                cliente.desativar()
        if dto.endereco is not None:
            endereco = Endereco(
                logradouro=dto.endereco.logradouro,
                numero=dto.endereco.numero,
                bairro=dto.endereco.bairro,
                cidade=dto.endereco.cidade,
                uf=dto.endereco.uf,
                cep=dto.endereco.cep,
                complemento=dto.endereco.complemento,
            )
            cliente.atualizar_endereco(endereco)
        
        cliente = await self._repository.update(cliente)
        return CriarClienteUseCase(self._repository)._to_response(cliente)


class BuscarClienteUseCase:
    """Caso de uso: Buscar cliente por ID"""
    
    def __init__(self, cliente_repository: IClienteRepository):
        self._repository = cliente_repository
    
    async def execute(self, id: UUID) -> ClienteResponseDTO:
        cliente = await self._repository.get_by_id(id)
        if not cliente:
            raise EntityNotFoundException("Cliente", str(id))
        return CriarClienteUseCase(self._repository)._to_response(cliente)


class ListarClientesUseCase:
    """Caso de uso: Listar clientes com paginação"""
    
    def __init__(self, cliente_repository: IClienteRepository):
        self._repository = cliente_repository
    
    async def execute(
        self, 
        skip: int = 0, 
        limit: int = 100,
        apenas_ativos: bool = False,
        termo_busca: Optional[str] = None
    ) -> List[ClienteResponseDTO]:
        if termo_busca:
            clientes = await self._repository.search(termo_busca, skip, limit)
        elif apenas_ativos:
            clientes = await self._repository.get_ativos(skip, limit)
        else:
            clientes = await self._repository.get_all(skip, limit)
        
        converter = CriarClienteUseCase(self._repository)
        return [converter._to_response(c) for c in clientes]
