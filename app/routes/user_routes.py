from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse, RoleEnum
from app.services import user_service
from app.dependencies.database_dependency import get_db
router = APIRouter()

@router.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(
    role: Optional[RoleEnum] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    return user_service.get_users(db, role, is_active)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_or_404(db, user_id)

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_complete_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user_complete(db, user_id, user_data)

@router.patch("/users/{user_id}", response_model=UserResponse)
def update_partial_user(user_id: int, user_data: UserPatch, db: Session = Depends(get_db)):
    return user_service.update_user_partial(db, user_id, user_data)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None