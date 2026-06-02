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

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool