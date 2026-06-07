from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: RoleEnum
    is_active: bool = True

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool