from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoanCreate(BaseModel):
    user_id: int
    device_id: int

class LoanUpdate(BaseModel):
    status: Optional[str] = None
    return_date: Optional[datetime] = None

class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True

# Para mostrar información relacionada (usuario + dispositivo)
class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]
    user: dict  # o podrías definir UserBasic
    device: dict  # o DeviceBasic

    class Config:
        from_attributes = True