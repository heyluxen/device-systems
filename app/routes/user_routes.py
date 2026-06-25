from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse, RoleEnum
from app.services import user_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin, require_support_or_admin
from app.dependencies.rate_limit_dependency import limiter
from app.models.user_model import User

router = APIRouter()

@router.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def list_users(
    request: Request,
    role: Optional[RoleEnum] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return user_service.get_users(db, role, is_active)

@router.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return user_service.get_user_or_404(db, user_id)

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_user(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(db, user_data)

@router.put("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def update_complete_user(
    request: Request,
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):
    return user_service.update_user_complete(db, user_id, user_data)

@router.patch("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def update_partial_user(
    request: Request,
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):
    return user_service.update_user_partial(db, user_id, user_data)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user_service.delete_user(db, user_id)
    return None