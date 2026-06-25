from fastapi import APIRouter, Depends, status, Request, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.loan_schema import LoanCreate, LoanResponse
from app.services import loan_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_support_or_admin
from app.dependencies.rate_limit_dependency import limiter
from app.models.user_model import User

router = APIRouter()

@router.post("/loans", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.create_loan(db, loan_data)

@router.patch("/loans/{loan_id}/return", response_model=LoanResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def return_loan(
    request: Request,
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):
    return loan_service.return_loan(db, loan_id)

@router.get("/loans/details", response_model=List[dict], status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_loans_details(
    request: Request,
    status: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    device_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):
    return loan_service.get_loans_with_details(db, status, user_email, device_type)

@router.get("/users/{user_id}/loans", response_model=List[LoanResponse], status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_user_loans(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.get_loans_by_user(db, user_id)

@router.get("/devices/{device_id}/loans", response_model=List[LoanResponse], status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_device_loans(
    request: Request,
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.get_loans_by_device(db, device_id)