"""
LogiFlow CRM - Router Contatos (Contacts)
Gerenciamento de contatos vinculados a clientes (Accounts)
Integrado com SuiteCRM
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from loguru import logger

from database import get_db

router = APIRouter(prefix="/contacts", tags=["Contatos CRM"])


# ========== Schemas ==========

class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    account_id: Optional[str] = Field(None, description="ID do cliente (Account)")
    email: Optional[EmailStr] = None
    phone_work: Optional[str] = Field(None, max_length=50)
    phone_mobile: Optional[str] = Field(None, max_length=50)
    title: Optional[str] = Field(None, max_length=100, description="Cargo")
    department: Optional[str] = Field(None, max_length=100)
    primary_address_city: Optional[str] = None
    primary_address_state: Optional[str] = None
    description: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_work: Optional[str] = None
    phone_mobile: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    primary_address_city: Optional[str] = None
    primary_address_state: Optional[str] = None
    description: Optional[str] = None


class ContactResponse(ContactBase):
    id: str
    full_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ========== Endpoints ==========

@router.get("/", response_model=List[ContactResponse])
async def list_contacts(
    account_id: Optional[str] = Query(None, description="Filtrar por cliente"),
    search: Optional[str] = Query(None, description="Buscar por nome ou email"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Lista contatos com filtros opcionais
    Consulta dados sincronizados do SuiteCRM
    """
    try:
        # TODO: Implementar consulta ao banco local sincronizado
        # Por enquanto, retornar via API SuiteCRM diretamente
        
        from services.suitecrm_service import suitecrm_service
        
        filters = {}
        if account_id:
            filters["account_id"] = account_id
        
        result = await suitecrm_service.get_module_records(
            module="Contacts",
            page_number=page,
            page_size=page_size,
            filters=filters if filters else None,
            fields=["first_name", "last_name", "email1", "phone_work", 
                   "phone_mobile", "title", "department", "account_id"]
        )
        
        contacts = []
        for item in result.get("data", []):
            attrs = item.get("attributes", {})
            contacts.append({
                "id": item.get("id"),
                "first_name": attrs.get("first_name", ""),
                "last_name": attrs.get("last_name", ""),
                "full_name": f"{attrs.get('first_name', '')} {attrs.get('last_name', '')}".strip(),
                "account_id": attrs.get("account_id"),
                "email": attrs.get("email1"),
                "phone_work": attrs.get("phone_work"),
                "phone_mobile": attrs.get("phone_mobile"),
                "title": attrs.get("title"),
                "department": attrs.get("department"),
                "primary_address_city": attrs.get("primary_address_city"),
                "primary_address_state": attrs.get("primary_address_state"),
                "description": attrs.get("description"),
                "created_at": attrs.get("date_entered"),
                "updated_at": attrs.get("date_modified")
            })
        
        # Filtrar por busca se fornecido
        if search:
            search_lower = search.lower()
            contacts = [
                c for c in contacts 
                if search_lower in c["full_name"].lower() or 
                   (c["email"] and search_lower in c["email"].lower())
            ]
        
        return contacts
        
    except Exception as e:
        logger.error(f"Erro ao listar contatos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: str):
    """Obtém detalhes de um contato específico"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        result = await suitecrm_service.get_record("Contacts", contact_id)
        
        attrs = result.get("data", {}).get("attributes", {})
        
        return {
            "id": contact_id,
            "first_name": attrs.get("first_name", ""),
            "last_name": attrs.get("last_name", ""),
            "full_name": f"{attrs.get('first_name', '')} {attrs.get('last_name', '')}".strip(),
            "account_id": attrs.get("account_id"),
            "email": attrs.get("email1"),
            "phone_work": attrs.get("phone_work"),
            "phone_mobile": attrs.get("phone_mobile"),
            "title": attrs.get("title"),
            "department": attrs.get("department"),
            "primary_address_city": attrs.get("primary_address_city"),
            "primary_address_state": attrs.get("primary_address_state"),
            "description": attrs.get("description"),
            "created_at": attrs.get("date_entered"),
            "updated_at": attrs.get("date_modified")
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter contato {contact_id}: {e}")
        raise HTTPException(status_code=404, detail="Contato não encontrado")


@router.post("/", response_model=ContactResponse, status_code=201)
async def create_contact(contact: ContactCreate):
    """Cria um novo contato no SuiteCRM"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        attributes = {
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email1": contact.email,
            "phone_work": contact.phone_work,
            "phone_mobile": contact.phone_mobile,
            "title": contact.title,
            "department": contact.department,
            "primary_address_city": contact.primary_address_city,
            "primary_address_state": contact.primary_address_state,
            "description": contact.description
        }
        
        if contact.account_id:
            attributes["account_id"] = contact.account_id
        
        # Remover campos None
        attributes = {k: v for k, v in attributes.items() if v is not None}
        
        result = await suitecrm_service.create_record("Contacts", attributes)
        
        contact_id = result.get("data", {}).get("id")
        
        logger.info(f"✅ Contato criado: {contact.first_name} {contact.last_name} ({contact_id})")
        
        # Retornar o contato criado
        return await get_contact(contact_id)
        
    except Exception as e:
        logger.error(f"Erro ao criar contato: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: str, contact: ContactUpdate):
    """Atualiza um contato existente"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        # Montar attributes apenas com campos fornecidos
        attributes = {}
        
        if contact.first_name is not None:
            attributes["first_name"] = contact.first_name
        if contact.last_name is not None:
            attributes["last_name"] = contact.last_name
        if contact.email is not None:
            attributes["email1"] = contact.email
        if contact.phone_work is not None:
            attributes["phone_work"] = contact.phone_work
        if contact.phone_mobile is not None:
            attributes["phone_mobile"] = contact.phone_mobile
        if contact.title is not None:
            attributes["title"] = contact.title
        if contact.department is not None:
            attributes["department"] = contact.department
        if contact.primary_address_city is not None:
            attributes["primary_address_city"] = contact.primary_address_city
        if contact.primary_address_state is not None:
            attributes["primary_address_state"] = contact.primary_address_state
        if contact.description is not None:
            attributes["description"] = contact.description
        
        if not attributes:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        await suitecrm_service.update_record("Contacts", contact_id, attributes)
        
        logger.info(f"✅ Contato atualizado: {contact_id}")
        
        # Retornar contato atualizado
        return await get_contact(contact_id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar contato {contact_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: str):
    """Deleta um contato"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        await suitecrm_service.delete_record("Contacts", contact_id)
        
        logger.info(f"✅ Contato deletado: {contact_id}")
        
        return None
        
    except Exception as e:
        logger.error(f"Erro ao deletar contato {contact_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-account/{account_id}", response_model=List[ContactResponse])
async def get_contacts_by_account(
    account_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Lista todos os contatos de um cliente específico"""
    return await list_contacts(account_id=account_id, page=page, page_size=page_size)


@router.get("/stats/summary")
async def get_contacts_stats():
    """Estatísticas de contatos"""
    try:
        from services.suitecrm_service import suitecrm_service
        
        result = await suitecrm_service.get_module_records(
            module="Contacts",
            page_size=1000  # Limite razoável
        )
        
        contacts = result.get("data", [])
        total = len(contacts)
        
        # Contar por cliente
        by_account = {}
        for contact in contacts:
            account_id = contact.get("attributes", {}).get("account_id")
            if account_id:
                by_account[account_id] = by_account.get(account_id, 0) + 1
        
        return {
            "total_contacts": total,
            "with_account": len([c for c in contacts if c.get("attributes", {}).get("account_id")]),
            "without_account": len([c for c in contacts if not c.get("attributes", {}).get("account_id")]),
            "accounts_with_contacts": len(by_account)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de contatos: {e}")
        raise HTTPException(status_code=500, detail=str(e))
