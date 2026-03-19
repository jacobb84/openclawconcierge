import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from core.database import get_db
from core.models import User, APIKey
from core.security import get_current_user

router = APIRouter(prefix="/api/api-keys", tags=["API Keys"])


class APIKeyCreate(BaseModel):
    name: str


class APIKeyUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class APIKeyResponse(BaseModel):
    id: int
    name: str
    key: str
    is_active: bool
    created_at: str | None
    last_used_at: str | None


class APIKeyListResponse(BaseModel):
    items: List[APIKeyResponse]
    total: int


def generate_api_key() -> str:
    """Generate a secure random API key."""
    return secrets.token_urlsafe(32)


@router.get("", response_model=APIKeyListResponse)
def list_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all API keys."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    keys = db.query(APIKey).order_by(APIKey.created_at.desc()).all()
    return {
        "items": [k.to_dict() for k in keys],
        "total": len(keys)
    }


@router.post("", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
def create_api_key(
    request: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new API key."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    api_key = APIKey(
        name=request.name,
        key=generate_api_key()
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    return api_key.to_dict()


@router.get("/{key_id}", response_model=APIKeyResponse)
def get_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single API key by ID."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return api_key.to_dict()


@router.put("/{key_id}", response_model=APIKeyResponse)
def update_api_key(
    key_id: int,
    request: APIKeyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an API key."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    if request.name is not None:
        api_key.name = request.name
    if request.is_active is not None:
        api_key.is_active = request.is_active
    
    db.commit()
    db.refresh(api_key)
    
    return api_key.to_dict()


@router.delete("/{key_id}")
def delete_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an API key."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    db.delete(api_key)
    db.commit()
    
    return {"message": "API key deleted"}


@router.post("/{key_id}/regenerate", response_model=APIKeyResponse)
def regenerate_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Regenerate an API key."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    api_key.key = generate_api_key()
    db.commit()
    db.refresh(api_key)
    
    return api_key.to_dict()
