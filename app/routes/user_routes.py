from fastapi import APIRouter, HTTPException, Header, Response, Query
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum

router = APIRouter()

fake_db = []
counter_id = 1

@router.get("/users", response_model=List[UserResponse])
def list_users(
    response: Response,
    role: Optional[RoleEnum] = Query(None),
    is_active: Optional[bool] = Query(None),
):
    users = fake_db.copy()
    if role:
        users = [u for u in users if u["role"] == role]
    if is_active is not None:
        users = [u for u in users if u["is_active"] == is_active]
    
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, response: Response):
    user = next((u for u in fake_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return user

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, response: Response):
    global counter_id
    for existing in fake_db:
        if existing["email"] == user_data.email:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    new_user = {
        "id": counter_id,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active,
    }
    fake_db.append(new_user)
    counter_id += 1
    
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    return new_user