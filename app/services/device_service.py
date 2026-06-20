from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate

def create_device(db: Session, device_data: DeviceCreate):
    existing = db.query(Device).filter(Device.serial_number == device_data.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Número de serie ya registrado")
    db_device = Device(**device_data.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session, device_type: str = None, is_available: bool = None, brand: str = None, search: str = None):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(Device.name.ilike(f"%{search}%"))
    return query.all()

def get_device_by_id(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

def get_device_or_404(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device

def update_device(db: Session, device_id: int, device_data: DeviceUpdate):
    device = get_device_or_404(db, device_id)
    update_data = device_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Debe enviar al menos un campo")
    for key, value in update_data.items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device

def delete_device(db: Session, device_id: int):
    device = get_device_or_404(db, device_id)
    db.delete(device)
    db.commit()
    return True