"""
LogiFlow CRM - Router Autenticação
Endpoints para autenticação JWT
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
import logging
import uuid
import hashlib
import secrets

# JWT
from jose import JWTError, jwt

logger = logging.getLogger(__name__)
router = APIRouter()


# ========================================
# Configurações JWT
# ========================================

SECRET_KEY = "logiflow-crm-secret-key-change-in-production-2024"
ALGORITHM = "HS256"
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

usuarios_db: dict = {}
tokens_refresh: dict = {}
tokens_reset: dict = {}


def _hash_senha(senha: str) -> str:
    """Hash de senha usando SHA256"""
    return hashlib.sha256(senha.encode()).hexdigest()


def _criar_usuario_admin():
    """Cria usuário admin padrão se não existir"""
    admin_email = "admin@logiflow.com"
    if admin_email not in usuarios_db:
        usuarios_db[admin_email] = {
            "id": str(uuid.uuid4()),
            "email": admin_email,
            "nome": "Administrador",
            "senha_hash": _hash_senha("admin123"),
            "tipo": TipoUsuario.ADMIN.value,
            "status": StatusUsuario.ATIVO.value,
            "telefone": None,
            "cargo": "Administrador do Sistema",
            "criado_em": datetime.utcnow(),
            "atualizado_em": datetime.utcnow(),
            "ultimo_acesso": None
        }
        logger.info("Usuário admin criado")

# Criar admin ao importar módulo
_criar_usuario_admin()


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


def criar_refresh_token(user_id: str) -> str:
    """Cria token de refresh"""
    token = secrets.token_urlsafe(32)
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    tokens_refresh[token] = {
        "user_id": user_id,
        "expire": expire
    }
    
    return token


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

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Obtém usuário atual a partir do token"""
    token_data = verificar_token(token)
    
    # Buscar usuário
    usuario = None
    for u in usuarios_db.values():
        if u["id"] == token_data.user_id:
            usuario = u
            break
    
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )
    
    if usuario["status"] != StatusUsuario.ATIVO.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo ou bloqueado"
        )
    
    return usuario


async def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Verifica se o usuário é admin"""
    if current_user["tipo"] != TipoUsuario.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    return current_user


async def get_current_gerente_ou_admin(current_user: dict = Depends(get_current_user)) -> dict:
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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login com email e senha.
    Retorna access_token e refresh_token.
    """
    try:
        email = form_data.username.lower()
        senha = form_data.password
        
        # Buscar usuário
        usuario = usuarios_db.get(email)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        # Verificar senha
        if usuario["senha_hash"] != _hash_senha(senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        # Verificar status
        if usuario["status"] != StatusUsuario.ATIVO.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuário {usuario['status']}"
            )
        
        # Criar tokens
        access_token = criar_access_token(data={
            "sub": usuario["id"],
            "email": usuario["email"],
            "tipo": usuario["tipo"],
            "nome": usuario["nome"]
        })
        
        refresh_token = criar_refresh_token(usuario["id"])
        
        # Atualizar último acesso
        usuario["ultimo_acesso"] = datetime.utcnow()
        
        logger.info(f"Login realizado: {email}")
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": usuario["id"],
                "email": usuario["email"],
                "nome": usuario["nome"],
                "tipo": usuario["tipo"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no login: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Renova access_token usando refresh_token"""
    try:
        token_data = tokens_refresh.get(refresh_token)
        
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )
        
        if datetime.utcnow() > token_data["expire"]:
            del tokens_refresh[refresh_token]
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expirado"
            )
        
        # Buscar usuário
        usuario = None
        for u in usuarios_db.values():
            if u["id"] == token_data["user_id"]:
                usuario = u
                break
        
        if not usuario or usuario["status"] != StatusUsuario.ATIVO.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado ou inativo"
            )
        
        # Criar novo access_token
        access_token = criar_access_token(data={
            "sub": usuario["id"],
            "email": usuario["email"],
            "tipo": usuario["tipo"],
            "nome": usuario["nome"]
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
    current_user: dict = Depends(get_current_user)
):
    """Invalida refresh_token"""
    if refresh_token and refresh_token in tokens_refresh:
        del tokens_refresh[refresh_token]
    
    logger.info(f"Logout: {current_user['email']}")
    
    return {"success": True, "message": "Logout realizado"}


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Retorna dados do usuário logado"""
    return {
        "success": True,
        "data": {
            "id": current_user["id"],
            "email": current_user["email"],
            "nome": current_user["nome"],
            "tipo": current_user["tipo"],
            "telefone": current_user.get("telefone"),
            "cargo": current_user.get("cargo"),
            "ultimo_acesso": current_user.get("ultimo_acesso")
        }
    }


@router.put("/me")
async def update_me(
    nome: Optional[str] = None,
    telefone: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Atualiza dados do próprio usuário"""
    if nome:
        current_user["nome"] = nome
    if telefone:
        current_user["telefone"] = telefone
    
    current_user["atualizado_em"] = datetime.utcnow()
    
    return {
        "success": True,
        "message": "Dados atualizados",
        "data": {
            "nome": current_user["nome"],
            "telefone": current_user.get("telefone")
        }
    }


@router.post("/alterar-senha")
async def alterar_senha(
    request: AlterarSenhaRequest,
    current_user: dict = Depends(get_current_user)
):
    """Altera senha do usuário logado"""
    # Verificar senha atual
    if current_user["senha_hash"] != _hash_senha(request.senha_atual):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualizar senha
    current_user["senha_hash"] = _hash_senha(request.nova_senha)
    current_user["atualizado_em"] = datetime.utcnow()
    
    logger.info(f"Senha alterada: {current_user['email']}")
    
    return {"success": True, "message": "Senha alterada com sucesso"}


@router.post("/recuperar-senha")
async def recuperar_senha(request: RecuperarSenhaRequest):
    """Envia email para recuperação de senha"""
    email = request.email.lower()
    usuario = usuarios_db.get(email)
    
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
    
    # Atualizar senha
    usuario = usuarios_db.get(token_data["email"])
    if usuario:
        usuario["senha_hash"] = _hash_senha(request.nova_senha)
        usuario["atualizado_em"] = datetime.utcnow()
        
        # Invalidar token
        del tokens_reset[request.token]
        
        logger.info(f"Senha resetada: {token_data['email']}")
    
    return {"success": True, "message": "Senha redefinida com sucesso"}


# ========================================
# Endpoints Admin - Gestão de Usuários
# ========================================

@router.get("/usuarios")
async def listar_usuarios(
    current_user: dict = Depends(get_current_admin)
):
    """Lista todos os usuários (admin only)"""
    usuarios = [
        {
            "id": u["id"],
            "email": u["email"],
            "nome": u["nome"],
            "tipo": u["tipo"],
            "status": u["status"],
            "ultimo_acesso": u.get("ultimo_acesso"),
            "criado_em": u["criado_em"]
        }
        for u in usuarios_db.values()
    ]
    
    return {
        "success": True,
        "data": usuarios,
        "total": len(usuarios)
    }


@router.post("/usuarios")
async def criar_usuario(
    request: CriarUsuarioRequest,
    current_user: dict = Depends(get_current_admin)
):
    """Cria novo usuário (admin only)"""
    email = request.email.lower()
    
    if email in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    usuario = {
        "id": str(uuid.uuid4()),
        "email": email,
        "nome": request.nome,
        "senha_hash": _hash_senha(request.senha),
        "tipo": request.tipo.value,
        "status": StatusUsuario.ATIVO.value,
        "telefone": request.telefone,
        "cargo": request.cargo,
        "criado_em": datetime.utcnow(),
        "atualizado_em": datetime.utcnow(),
        "ultimo_acesso": None,
        "criado_por": current_user["id"]
    }
    
    usuarios_db[email] = usuario
    
    logger.info(f"Usuário criado: {email} por {current_user['email']}")
    
    return {
        "success": True,
        "message": "Usuário criado com sucesso",
        "data": {
            "id": usuario["id"],
            "email": usuario["email"],
            "nome": usuario["nome"],
            "tipo": usuario["tipo"]
        }
    }


@router.patch("/usuarios/{user_id}/status")
async def alterar_status_usuario(
    user_id: str,
    status_novo: StatusUsuario,
    current_user: dict = Depends(get_current_admin)
):
    """Altera status de um usuário (admin only)"""
    usuario = None
    for u in usuarios_db.values():
        if u["id"] == user_id:
            usuario = u
            break
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario["id"] == current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar o próprio status"
        )
    
    usuario["status"] = status_novo.value
    usuario["atualizado_em"] = datetime.utcnow()
    
    logger.info(f"Status do usuário {usuario['email']} alterado para {status_novo.value}")
    
    return {
        "success": True,
        "message": f"Status alterado para {status_novo.value}"
    }


@router.delete("/usuarios/{user_id}")
async def excluir_usuario(
    user_id: str,
    current_user: dict = Depends(get_current_admin)
):
    """Exclui (inativa) um usuário (admin only)"""
    email_to_delete = None
    for email, u in usuarios_db.items():
        if u["id"] == user_id:
            email_to_delete = email
            break
    
    if not email_to_delete:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuarios_db[email_to_delete]["id"] == current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível excluir o próprio usuário"
        )
    
    # Soft delete
    usuarios_db[email_to_delete]["status"] = StatusUsuario.INATIVO.value
    usuarios_db[email_to_delete]["atualizado_em"] = datetime.utcnow()
    
    logger.info(f"Usuário inativado: {email_to_delete}")
    
    return {"success": True, "message": "Usuário inativado"}
