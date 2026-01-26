"""
Dependency Injection Container
==============================
Configura e gerencia as dependências da aplicação.
Uso com FastAPI Depends() para injeção automática.
"""
from functools import lru_cache
from typing import Generator

from sqlalchemy.orm import Session

from domain.interfaces.repositories import (
    IClienteRepository,
    ICotacaoRepository,
    IPedidoRepository,
)
from application.use_cases.cliente_use_cases import (
    CriarClienteUseCase,
    AtualizarClienteUseCase,
    BuscarClienteUseCase,
    ListarClientesUseCase,
)
from application.use_cases.cotacao_use_cases import (
    CriarCotacaoUseCase,
    EnviarCotacaoUseCase,
    AprovarCotacaoUseCase,
)

from .persistence.database import SessionLocal
from .repositories.cliente_repository import ClienteRepository
from .repositories.cotacao_repository import CotacaoRepository
from .repositories.pedido_repository import PedidoRepository


def get_db() -> Generator[Session, None, None]:
    """Dependency: Sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cliente_repository(db: Session) -> IClienteRepository:
    """Dependency: Repository de clientes"""
    return ClienteRepository(db)


def get_cotacao_repository(db: Session) -> ICotacaoRepository:
    """Dependency: Repository de cotações"""
    return CotacaoRepository(db)


def get_pedido_repository(db: Session) -> IPedidoRepository:
    """Dependency: Repository de pedidos"""
    return PedidoRepository(db)


def get_criar_cliente_use_case(
    cliente_repo: IClienteRepository
) -> CriarClienteUseCase:
    """Dependency: Use case para criar cliente"""
    return CriarClienteUseCase(cliente_repo)


def get_atualizar_cliente_use_case(
    cliente_repo: IClienteRepository
) -> AtualizarClienteUseCase:
    """Dependency: Use case para atualizar cliente"""
    return AtualizarClienteUseCase(cliente_repo)


def get_buscar_cliente_use_case(
    cliente_repo: IClienteRepository
) -> BuscarClienteUseCase:
    """Dependency: Use case para buscar cliente"""
    return BuscarClienteUseCase(cliente_repo)


def get_listar_clientes_use_case(
    cliente_repo: IClienteRepository
) -> ListarClientesUseCase:
    """Dependency: Use case para listar clientes"""
    return ListarClientesUseCase(cliente_repo)


def get_criar_cotacao_use_case(
    cotacao_repo: ICotacaoRepository,
    cliente_repo: IClienteRepository
) -> CriarCotacaoUseCase:
    """Dependency: Use case para criar cotação"""
    return CriarCotacaoUseCase(cotacao_repo, cliente_repo)


def get_enviar_cotacao_use_case(
    cotacao_repo: ICotacaoRepository
) -> EnviarCotacaoUseCase:
    """Dependency: Use case para enviar cotação"""
    return EnviarCotacaoUseCase(cotacao_repo)


def get_aprovar_cotacao_use_case(
    cotacao_repo: ICotacaoRepository
) -> AprovarCotacaoUseCase:
    """Dependency: Use case para aprovar cotação"""
    return AprovarCotacaoUseCase(cotacao_repo)


class Container:
    """
    Container de Dependências centralizado.
    
    Uso em routers FastAPI:
    ```python
    from fastapi import Depends
    from infrastructure.container import Container
    
    @router.post("/clientes")
    async def criar_cliente(
        dto: ClienteCreateDTO,
        use_case: CriarClienteUseCase = Depends(Container.criar_cliente_use_case)
    ):
        return await use_case.execute(dto)
    ```
    """
    
    @staticmethod
    def db() -> Generator[Session, None, None]:
        return get_db()
    
    @staticmethod
    def cliente_repository(db: Session) -> IClienteRepository:
        return get_cliente_repository(db)
    
    @staticmethod
    def cotacao_repository(db: Session) -> ICotacaoRepository:
        return get_cotacao_repository(db)
    
    @staticmethod
    def pedido_repository(db: Session) -> IPedidoRepository:
        return get_pedido_repository(db)
    
    @staticmethod
    def criar_cliente_use_case(
        db: Session
    ) -> CriarClienteUseCase:
        repo = ClienteRepository(db)
        return CriarClienteUseCase(repo)
    
    @staticmethod
    def atualizar_cliente_use_case(
        db: Session
    ) -> AtualizarClienteUseCase:
        repo = ClienteRepository(db)
        return AtualizarClienteUseCase(repo)
    
    @staticmethod
    def buscar_cliente_use_case(
        db: Session
    ) -> BuscarClienteUseCase:
        repo = ClienteRepository(db)
        return BuscarClienteUseCase(repo)
    
    @staticmethod
    def listar_clientes_use_case(
        db: Session
    ) -> ListarClientesUseCase:
        repo = ClienteRepository(db)
        return ListarClientesUseCase(repo)
    
    @staticmethod
    def criar_cotacao_use_case(
        db: Session
    ) -> CriarCotacaoUseCase:
        cotacao_repo = CotacaoRepository(db)
        cliente_repo = ClienteRepository(db)
        return CriarCotacaoUseCase(cotacao_repo, cliente_repo)
    
    @staticmethod
    def enviar_cotacao_use_case(
        db: Session
    ) -> EnviarCotacaoUseCase:
        repo = CotacaoRepository(db)
        return EnviarCotacaoUseCase(repo)
    
    @staticmethod
    def aprovar_cotacao_use_case(
        db: Session
    ) -> AprovarCotacaoUseCase:
        repo = CotacaoRepository(db)
        return AprovarCotacaoUseCase(repo)
