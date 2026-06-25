from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

# Para crear usuario (POST)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: RoleEnum
    is_active: bool = True

# Para actualización completa (PUT)
class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: RoleEnum
    is_active: bool

# Para actualización parcial (PATCH)
class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

# Para respuesta (GET, POST, PUT, PATCH)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy