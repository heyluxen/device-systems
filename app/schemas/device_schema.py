from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=3)
    serial_number: str = Field(..., min_length=5)
    device_type: str
    brand: Optional[str] = None
    is_available: bool = True

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    serial_number: Optional[str] = Field(None, min_length=5)
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None

class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True