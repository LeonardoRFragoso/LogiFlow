"""
Cotação Use Cases - Casos de uso para operações com cotações
"""
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from domain.entities.cotacao import Cotacao, ItemCotacao, TipoFrete, TipoCarga, StatusCotacao
from domain.interfaces.repositories import ICotacaoRepository, IClienteRepository
from domain.value_objects.endereco import Endereco
from domain.exceptions import EntityNotFoundException, BusinessRuleException

from ..dtos.cotacao_dto import CotacaoCreateDTO, CotacaoResponseDTO, ItemCotacaoDTO
from ..dtos.cliente_dto import EnderecoDTO


class CriarCotacaoUseCase:
    """Caso de uso: Criar nova cotação"""
    
    def __init__(
        self, 
        cotacao_repository: ICotacaoRepository,
        cliente_repository: IClienteRepository
    ):
        self._cotacao_repo = cotacao_repository
        self._cliente_repo = cliente_repository
        self._counter = 1000
    
    async def execute(self, dto: CotacaoCreateDTO, usuario: str = None) -> CotacaoResponseDTO:
        # Verificar se cliente existe
        cliente = await self._cliente_repo.get_by_id(dto.cliente_id)
        if not cliente:
            raise EntityNotFoundException("Cliente", str(dto.cliente_id))
        
        # Criar value objects
        origem = self._criar_endereco(dto.origem)
        destino = self._criar_endereco(dto.destino)
        itens = [self._criar_item(item) for item in dto.itens]
        
        # Gerar número da cotação
        self._counter += 1
        numero = f"COT-{datetime.now().year}-{self._counter:05d}"
        
        # Criar entidade
        cotacao = Cotacao(
            cliente_id=dto.cliente_id,
            origem=origem,
            destino=destino,
            itens=itens,
            numero=numero,
            tipo_frete=TipoFrete(dto.tipo_frete),
            tipo_carga=TipoCarga(dto.tipo_carga),
            valor_frete=dto.valor_frete or Decimal("0"),
            valor_seguro=dto.valor_seguro or Decimal("0"),
            valor_outros=dto.valor_outros or Decimal("0"),
            desconto=dto.desconto or Decimal("0"),
            validade=dto.validade,
            observacoes=dto.observacoes,
            criado_por=usuario,
        )
        
        # Persistir
        cotacao = await self._cotacao_repo.add(cotacao)
        
        return self._to_response(cotacao)
    
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
    
    def _criar_item(self, dto: ItemCotacaoDTO) -> ItemCotacao:
        return ItemCotacao(
            descricao=dto.descricao,
            quantidade=dto.quantidade,
            peso_kg=dto.peso_kg,
            volume_m3=dto.volume_m3,
            valor_mercadoria=dto.valor_mercadoria,
            observacao=dto.observacao,
        )
    
    def _to_response(self, cotacao: Cotacao) -> CotacaoResponseDTO:
        return CotacaoResponseDTO(
            id=cotacao.id,
            numero=cotacao.numero or "",
            cliente_id=cotacao.cliente_id,
            origem=self._endereco_to_dto(cotacao.origem),
            destino=self._endereco_to_dto(cotacao.destino),
            itens=[self._item_to_dto(i) for i in cotacao.itens],
            tipo_frete=cotacao.tipo_frete.value,
            tipo_carga=cotacao.tipo_carga.value,
            status=cotacao.status.value,
            valor_frete=cotacao.valor_frete,
            valor_seguro=cotacao.valor_seguro,
            valor_outros=cotacao.valor_outros,
            desconto=cotacao.desconto,
            valor_total=cotacao.valor_total,
            peso_total=cotacao.peso_total,
            volume_total=cotacao.volume_total,
            validade=cotacao.validade,
            observacoes=cotacao.observacoes,
            criado_por=cotacao.criado_por,
            created_at=cotacao.created_at,
            updated_at=cotacao.updated_at,
        )
    
    def _endereco_to_dto(self, endereco: Endereco) -> EnderecoDTO:
        return EnderecoDTO(
            logradouro=endereco.logradouro,
            numero=endereco.numero,
            bairro=endereco.bairro,
            cidade=endereco.cidade,
            uf=endereco.uf,
            cep=endereco.cep,
            complemento=endereco.complemento,
        )
    
    def _item_to_dto(self, item: ItemCotacao) -> ItemCotacaoDTO:
        return ItemCotacaoDTO(
            descricao=item.descricao,
            quantidade=item.quantidade,
            peso_kg=item.peso_kg,
            volume_m3=item.volume_m3,
            valor_mercadoria=item.valor_mercadoria,
            observacao=item.observacao,
        )


class EnviarCotacaoUseCase:
    """Caso de uso: Enviar cotação para cliente"""
    
    def __init__(self, cotacao_repository: ICotacaoRepository):
        self._repository = cotacao_repository
    
    async def execute(self, cotacao_id: UUID) -> CotacaoResponseDTO:
        cotacao = await self._repository.get_by_id(cotacao_id)
        if not cotacao:
            raise EntityNotFoundException("Cotação", str(cotacao_id))
        
        try:
            cotacao.enviar()
        except ValueError as e:
            raise BusinessRuleException(str(e), rule="enviar_cotacao")
        
        cotacao = await self._repository.update(cotacao)
        return CriarCotacaoUseCase(self._repository, None)._to_response(cotacao)


class AprovarCotacaoUseCase:
    """Caso de uso: Aprovar cotação"""
    
    def __init__(self, cotacao_repository: ICotacaoRepository):
        self._repository = cotacao_repository
    
    async def execute(self, cotacao_id: UUID) -> CotacaoResponseDTO:
        cotacao = await self._repository.get_by_id(cotacao_id)
        if not cotacao:
            raise EntityNotFoundException("Cotação", str(cotacao_id))
        
        # Verificar se expirou
        if cotacao.esta_expirada():
            cotacao.status = StatusCotacao.EXPIRADA
            await self._repository.update(cotacao)
            raise BusinessRuleException(
                "Cotação expirada e não pode ser aprovada",
                rule="aprovar_cotacao"
            )
        
        try:
            cotacao.aprovar()
        except ValueError as e:
            raise BusinessRuleException(str(e), rule="aprovar_cotacao")
        
        cotacao = await self._repository.update(cotacao)
        return CriarCotacaoUseCase(self._repository, None)._to_response(cotacao)
