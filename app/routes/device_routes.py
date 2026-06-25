from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_support_or_admin, require_admin
from app.dependencies.rate_limit_dependency import limiter
from app.models.user_model import User

router = APIRouter()

@router.get("/devices", response_model=List[DeviceResponse], status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def list_devices(
    request: Request,
    device_type: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    brand: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return device_service.get_devices(db, device_type, is_available, brand, search)

@router.get("/devices/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_device(
    request: Request,
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return device_service.get_device_or_404(db, device_id)

@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_device(
    request: Request,
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):
    return device_service.create_device(db, device_data)

@router.put("/devices/{device_id}", response_model=DeviceResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def update_device(
    request: Request,
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):
    return device_service.update_device(db, device_id, device_data)

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_device(
    request: Request,
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    device_service.delete_device(db, device_id)
    return None