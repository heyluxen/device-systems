from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service
from app.dependencies.database_dependency import get_db

router = APIRouter()

@router.post("/loans", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
    return loan_service.create_loan(db, loan_data)

@router.patch("/loans/{loan_id}/return", response_model=LoanResponse)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.return_loan(db, loan_id)

@router.get("/loans/details", response_model=List[dict])
def get_loans_details(
    status: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return loan_service.get_loans_with_details(db, status, user_email, device_type)

@router.get("/users/{user_id}/loans", response_model=List[LoanResponse])
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loans_by_user(db, user_id)

@router.get("/devices/{device_id}/loans", response_model=List[LoanResponse])
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loans_by_device(db, device_id)