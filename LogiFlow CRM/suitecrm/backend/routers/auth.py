"""
LogiFlow CRM - Authentication Router
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class TokenData(BaseModel):
    user_id: str
    email: str
    tenant_id: str


def create_access_token(data: dict) -> str:
    """Cria JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica senha"""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Autentica usuário e retorna token JWT
    
    TODO: Implementar validação real contra SuiteCRM
    """
    # TODO: Buscar usuário no banco/SuiteCRM
    # Por agora, apenas exemplo
    
    # Simulação - remover em produção
    if request.email == "admin@logiflow.com.br" and request.password == "admin123":
        user_data = {
            "user_id": "1",
            "email": request.email,
            "tenant_id": "default",
            "name": "Administrador"
        }
        
        token = create_access_token(user_data)
        
        return LoginResponse(
            access_token=token,
            expires_in=settings.JWT_EXPIRATION_HOURS * 3600,
            user={
                "id": user_data["user_id"],
                "email": user_data["email"],
                "name": user_data["name"],
                "tenant_id": user_data["tenant_id"]
            }
        )
    
    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@router.post("/refresh")
async def refresh_token():
    """Renova token JWT"""
    # TODO: Implementar refresh token
    raise HTTPException(status_code=501, detail="Não implementado")


@router.post("/logout")
async def logout():
    """Invalida token (client-side)"""
    return {"message": "Logout realizado com sucesso"}
