"""
LogiFlow CRM - Router Autenticação
Endpoints para autenticação JWT
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
import logging
import uuid
import secrets

from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session

from config import settings
from database import get_db, SessionLocal
from models import User, RefreshToken
from middleware.rate_limiter import limiter

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Configurações JWT
# ========================================

SECRET_KEY = settings.SECRET_KEY
if SECRET_KEY == "change-this-in-production":
    logger.warning("SECRET_KEY está usando valor padrão. Defina via variável de ambiente em produção.")
ALGORITHM = "HS256"


def _hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except Exception:
        return False

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 horas
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ========================================
# OAuth2 Scheme
# ========================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ========================================
# Enums
# ========================================

class TipoUsuario(str, Enum):
    ADMIN = "admin"
    GERENTE = "gerente"
    OPERADOR = "operador"
    MOTORISTA = "motorista"
    CLIENTE = "cliente"


class StatusUsuario(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    BLOQUEADO = "bloqueado"
    PENDENTE = "pendente"


# ========================================
# Schemas
# ========================================

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    tipo: Optional[str] = None


class UsuarioBase(BaseModel):
    email: EmailStr
    nome: str
    tipo: TipoUsuario = TipoUsuario.OPERADOR


class CriarUsuarioRequest(UsuarioBase):
    senha: str = Field(..., min_length=6)
    telefone: Optional[str] = None
    cargo: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class AlterarSenhaRequest(BaseModel):
    senha_atual: str
    nova_senha: str = Field(..., min_length=6)


class RecuperarSenhaRequest(BaseModel):
    email: EmailStr


class ResetarSenhaRequest(BaseModel):
    token: str
    nova_senha: str = Field(..., min_length=6)


class UsuarioResponse(BaseModel):
    id: str
    email: str
    nome: str
    tipo: TipoUsuario
    status: StatusUsuario
    telefone: Optional[str]
    cargo: Optional[str]
    ultimo_acesso: Optional[datetime]
    criado_em: datetime


# ========================================
# Storage Simulado (substituir por DB)
# ========================================
tokens_reset: dict = {}


def _get_user_by_email(db: Session, email: str, tenant_id: Optional[int] = None) -> Optional[User]:
    """Busca usuário por email, opcionalmente filtrando por tenant"""
    query = db.query(User).filter(User.email == email)
    if tenant_id:
        query = query.filter(User.tenant_id == tenant_id)
    return query.first()


def _get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def criar_usuario_admin_se_necessario():
    """
    Cria usuário admin padrão se não existir.
    IMPORTANTE: Chamado durante startup da aplicação, NÃO no import do módulo.
    """
    try:
        from database import get_session_local
        SessionLocal = get_session_local()
        admin_email = "admin@logiflow.com"
        with SessionLocal() as db:
            if _get_user_by_email(db, admin_email):
                return
            user = User(
                email=admin_email,
                nome="Administrador",
                senha_hash=_hash_senha("admin123"),
                tipo=TipoUsuario.ADMIN.value,
                status=StatusUsuario.ATIVO.value,
            )
            db.add(user)
            db.commit()
            logger.info("Usuário admin criado")
    except Exception as e:
        logger.warning(f"Não foi possível criar usuário admin: {e}")


# REMOVIDO: Não criar admin no import - isso quebra o build no Render
# A criação do admin agora é feita no startup da aplicação (main.py lifespan)


def criar_refresh_token_db(db: Session, user_id: str) -> str:
    """Cria e persiste refresh token."""
    token = secrets.token_urlsafe(32)
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(
        token=token,
        user_id=user_id,
        expire_at=expire,
        revoked=False,
    )
    db.add(db_token)
    db.commit()
    return token


def validar_refresh_token_db(db: Session, token: str) -> RefreshToken:
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not db_token or db_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido",
        )
    if datetime.utcnow() > db_token.expire_at:
        db_token.revoked = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expirado",
        )
    return db_token


def revogar_refresh_token_db(db: Session, token: str) -> None:
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if db_token:
        db_token.revoked = True
        db.commit()


# ========================================
# Funções de Token
# ========================================

def criar_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT de acesso"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str) -> TokenData:
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        tipo: str = payload.get("tipo")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return TokenData(user_id=user_id, email=email, tipo=tipo)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )


# ========================================
# Dependencies
# ========================================

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Obtém usuário atual a partir do token"""
    token_data = verificar_token(token)

    usuario = _get_user_by_id(db, token_data.user_id)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    if usuario.status != StatusUsuario.ATIVO.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo ou bloqueado"
        )

    return usuario


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Verifica se o usuário é admin"""
    if current_user["tipo"] != TipoUsuario.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return current_user


async def get_current_gerente_ou_admin(current_user: User = Depends(get_current_user)) -> User:
    """Verifica se o usuário é gerente ou admin"""
    if current_user["tipo"] not in [TipoUsuario.ADMIN.value, TipoUsuario.GERENTE.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a gerentes ou administradores"
        )
    return current_user


# ========================================
# Endpoints
# ========================================

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login com email e senha.
    Retorna access_token e refresh_token.
    """
    try:
        email = form_data.username.lower()
        senha = form_data.password

        usuario = _get_user_by_email(db, email)

        if not usuario or not _verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        if usuario.status != StatusUsuario.ATIVO.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário {usuario.status}"
            )

        access_token = criar_access_token(data={
            "sub": str(usuario.id),
            "user_id": usuario.id,
            "email": usuario.email,
            "tipo": usuario.tipo,
            "nome": usuario.nome,
            "tenant_id": usuario.tenant_id
        })

        refresh_token = criar_refresh_token_db(db, usuario.id)

        usuario.ultimo_acesso = datetime.utcnow()
        db.add(usuario)
        db.commit()

        logger.info(f"Login realizado: {email}")

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": usuario.id,
                "email": usuario.email,
                "nome": usuario.nome,
                "tipo": usuario.tipo
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/motorista/login", response_model=Token)
@limiter.limit("5/minute")
async def login_motorista(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login específico para motoristas.
    Valida se o usuário tem role 'motorista'.
    """
    try:
        email = form_data.username.lower()
        senha = form_data.password

        usuario = _get_user_by_email(db, email)

        if not usuario or not _verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        if usuario.status != StatusUsuario.ATIVO.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário {usuario.status}"
            )

        if usuario.tipo != TipoUsuario.MOTORISTA.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso restrito a motoristas"
            )

        access_token = criar_access_token(data={
            "sub": str(usuario.id),
            "user_id": usuario.id,
            "email": usuario.email,
            "tipo": usuario.tipo,
            "nome": usuario.nome,
            "tenant_id": usuario.tenant_id
        })

        refresh_token = criar_refresh_token_db(db, usuario.id)

        usuario.ultimo_acesso = datetime.utcnow()
        db.add(usuario)
        db.commit()

        logger.info(f"✅ Login motorista realizado: {email}")

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": usuario.id,
                "email": usuario.email,
                "nome": usuario.nome,
                "tipo": usuario.tipo
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no login motorista: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cliente/login", response_model=Token)
@limiter.limit("5/minute")
async def login_cliente(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login específico para clientes.
    Valida se o usuário tem role 'cliente'.
    """
    try:
        email = form_data.username.lower()
        senha = form_data.password

        usuario = _get_user_by_email(db, email)

        if not usuario or not _verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        if usuario.status != StatusUsuario.ATIVO.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário {usuario.status}"
            )

        if usuario.tipo != TipoUsuario.CLIENTE.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso restrito a clientes"
            )

        access_token = criar_access_token(data={
            "sub": str(usuario.id),
            "user_id": usuario.id,
            "email": usuario.email,
            "tipo": usuario.tipo,
            "nome": usuario.nome,
            "tenant_id": usuario.tenant_id
        })

        refresh_token = criar_refresh_token_db(db, usuario.id)

        usuario.ultimo_acesso = datetime.utcnow()
        db.add(usuario)
        db.commit()

        logger.info(f"✅ Login cliente realizado: {email}")

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": usuario.id,
                "email": usuario.email,
                "nome": usuario.nome,
                "tipo": usuario.tipo
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no login cliente: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
async def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    """Renova access_token usando refresh_token"""
    try:
        db_token = validar_refresh_token_db(db, payload.refresh_token)

        usuario = _get_user_by_id(db, db_token.user_id)

        if not usuario or usuario.status != StatusUsuario.ATIVO.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado ou inativo"
            )

        access_token = criar_access_token(data={
            "sub": str(usuario.id),
            "email": usuario.email,
            "tipo": usuario.tipo,
            "nome": usuario.nome
        })

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao refresh token: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout")
async def logout(
    refresh_token: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Invalida refresh_token"""
    if refresh_token:
        revogar_refresh_token_db(db, refresh_token)
    
    logger.info(f"Logout: {current_user.email}")
    
    return {"success": True, "message": "Logout realizado"}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Retorna dados do usuário logado"""
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "nome": current_user.nome,
            "tipo": current_user.tipo,
            "status": current_user.status
        }
    }


@router.put("/me")
async def update_me(
    nome: Optional[str] = None,
    telefone: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza dados do próprio usuário"""
    if nome:
        current_user.nome = nome
    db.add(current_user)
    db.commit()
    
    return {
        "success": True,
        "message": "Dados atualizados",
        "data": {
            "nome": current_user.nome
        }
    }


@router.post("/alterar-senha")
async def alterar_senha(
    request: AlterarSenhaRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Altera senha do usuário logado"""
    if not _verificar_senha(request.senha_atual, current_user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    current_user.senha_hash = _hash_senha(request.nova_senha)
    current_user.atualizado_em = datetime.utcnow()
    db.add(current_user)
    db.commit()
    
    logger.info(f"Senha alterada: {current_user.email}")
    
    return {"success": True, "message": "Senha alterada com sucesso"}


@router.post("/recuperar-senha")
async def recuperar_senha(request: RecuperarSenhaRequest):
    """Envia email para recuperação de senha"""
    email = request.email.lower()
    with SessionLocal() as db:
        usuario = _get_user_by_email(db, email)
    
    # Sempre retorna sucesso para não expor emails existentes
    if usuario:
        # Criar token de reset
        token = secrets.token_urlsafe(32)
        tokens_reset[token] = {
            "email": email,
            "expire": datetime.utcnow() + timedelta(hours=1)
        }
        
        # TODO: Enviar email com link de reset
        logger.info(f"Token de recuperação gerado para: {email}")
        logger.info(f"Token (DEV ONLY): {token}")
    
    return {
        "success": True,
        "message": "Se o email existir, você receberá instruções para redefinir sua senha"
    }


@router.post("/resetar-senha")
async def resetar_senha(request: ResetarSenhaRequest):
    """Reseta senha usando token de recuperação"""
    token_data = tokens_reset.get(request.token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado"
        )
    
    if datetime.utcnow() > token_data["expire"]:
        del tokens_reset[request.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado"
        )
    
    with SessionLocal() as db:
        usuario = _get_user_by_email(db, token_data["email"])
        if usuario:
            usuario.senha_hash = _hash_senha(request.nova_senha)
            usuario.atualizado_em = datetime.utcnow()
            db.add(usuario)
            db.commit()

            del tokens_reset[request.token]
            logger.info(f"Senha resetada: {token_data['email']}")
    
    return {"success": True, "message": "Senha redefinida com sucesso"}


# ========================================
# Endpoints Admin - Gestão de Usuários
# ========================================

@router.get("/usuarios")
async def listar_usuarios(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os usuários (admin only)"""
    usuarios_query = db.query(User).all()
    usuarios = []
    for u in usuarios_query:
        usuarios.append({
            "id": u.id,
            "email": u.email,
            "nome": u.nome,
            "tipo": u.tipo,
            "status": u.status,
            "created_at": u.created_at
        })

    return {
        "success": True,
        "data": usuarios,
        "total": len(usuarios)
    }


@router.post("/usuarios")
async def criar_usuario(
    request: CriarUsuarioRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Cria novo usuário (admin only)"""
    email = request.email.lower()
    
    if _get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    usuario = User(
        email=email,
        nome=request.nome,
        senha_hash=_hash_senha(request.senha),
        tipo=request.tipo.value,
        status=StatusUsuario.ATIVO.value,
    )
    
    db.add(usuario)
    db.commit()
    
    logger.info(f"Usuário criado: {email} por {current_user.email}")
    
    return {
        "success": True,
        "message": "Usuário criado com sucesso",
        "data": {
            "id": usuario.id,
            "email": usuario.email,
            "nome": usuario.nome,
            "tipo": usuario.tipo
        }
    }


@router.patch("/usuarios/{user_id}/status")
async def alterar_status_usuario(
    user_id: str,
    status_novo: StatusUsuario,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Altera status de um usuário (admin only)"""
    usuario = _get_user_by_id(db, user_id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar o próprio status"
        )
    
    usuario.status = status_novo.value
    usuario.atualizado_em = datetime.utcnow()
    db.add(usuario)
    db.commit()
    
    logger.info(f"Status do usuário {usuario.email} alterado para {status_novo.value}")
    
    return {
        "success": True,
        "message": f"Status alterado para {status_novo.value}"
    }


@router.delete("/usuarios/{user_id}")
async def excluir_usuario(
    user_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Exclui (inativa) um usuário (admin only)"""
    usuario = _get_user_by_id(db, user_id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir o próprio usuário"
        )
    
    usuario.status = StatusUsuario.INATIVO.value
    usuario.atualizado_em = datetime.utcnow()
    db.add(usuario)
    db.commit()
    
    logger.info(f"Usuário inativado: {usuario.email}")
    
    return {"success": True, "message": "Usuário inativado"}
