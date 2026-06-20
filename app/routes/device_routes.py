from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service
from app.dependencies.database_dependency import get_db

router = APIRouter()

@router.get("/devices", response_model=List[DeviceResponse])
def list_devices(
    device_type: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    brand: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return device_service.get_devices(db, device_type, is_available, brand, search)

@router.get("/devices/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    return device_service.get_device_or_404(db, device_id)

@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
    return device_service.create_device(db, device_data)

@router.put("/devices/{device_id}", response_model=DeviceResponse)
def update_device(device_id: int, device_data: DeviceUpdate, db: Session = Depends(get_db)):
    return device_service.update_device(db, device_id, device_data)

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device_service.delete_device(db, device_id)
    return None