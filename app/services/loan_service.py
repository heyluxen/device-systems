from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from datetime import datetime
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate

def create_loan(db: Session, loan_data: LoanCreate):
    # Validar usuario
    user = db.query(User).filter(User.id == loan_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar dispositivo
    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if not device.is_available:
        raise HTTPException(status_code=409, detail="Dispositivo no disponible")
    # Crear préstamo
    db_loan = Loan(user_id=loan_data.user_id, device_id=loan_data.device_id, status="active")
    db.add(db_loan)
    # Marcar dispositivo como no disponible
    device.is_available = False
    db.commit()
    db.refresh(db_loan)
    return db_loan

def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="El préstamo ya fue devuelto")
    loan.status = "returned"
    loan.return_date = datetime.utcnow()
    # Marcar dispositivo como disponible
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan

def get_loans_with_details(db: Session, status: str = None, user_email: str = None, device_type: str = None):
    query = db.query(Loan)
    if status:
        query = query.filter(Loan.status == status)
    if user_email:
        query = query.join(User).filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.join(Device).filter(Device.device_type == device_type)
    loans = query.all()
    # Construir respuesta con datos relacionados
    result = []
    for loan in loans:
        result.append({
            "loan_id": loan.id,
            "status": loan.status,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "user": {
                "id": loan.user.id,
                "name": loan.user.name,
                "email": loan.user.email
            },
            "device": {
                "id": loan.device.id,
                "name": loan.device.name,
                "serial_number": loan.device.serial_number,
                "device_type": loan.device.device_type
            }
        })
    return result

def get_loans_by_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Loan).filter(Loan.user_id == user_id).all()

def get_loans_by_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db.query(Loan).filter(Loan.device_id == device_id).all()