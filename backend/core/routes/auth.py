from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from core.models import User
from core.security import create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    user: dict


class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool
    created_at: str | None


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint for user authentication."""
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or not user.check_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "user": user.to_dict()
    }


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current logged-in user info."""
    return current_user.to_dict()
