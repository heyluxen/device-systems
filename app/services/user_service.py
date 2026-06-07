from app.data.users_db import users_db, counter_id
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from fastapi import HTTPException, status

def get_all_users(role: str = None, is_active: bool = None):
    users = users_db.copy()
    if role:
        users = [u for u in users if u["role"] == role]
    if is_active is not None:
        users = [u for u in users if u["is_active"] == is_active]
    return users

def get_user_by_id(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    return None

def create_user(user_data: UserCreate):
    global counter_id
    # Verificar email duplicado
    for u in users_db:
        if u["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
    new_user = {
        "id": counter_id,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active,
    }
    users_db.append(new_user)
    counter_id += 1
    return new_user

def update_user_complete(user_id: int, user_data: UserCreate):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Verificar email duplicado (si el email cambió y ya existe otro usuario con ese email)
    for u in users_db:
        if u["id"] != user_id and u["email"] == user_data.email:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado por otro usuario"
            )
    user["name"] = user_data.name
    user["email"] = user_data.email
    user["role"] = user_data.role
    user["is_active"] = user_data.is_active
    return user

def update_user_partial(user_id: int, user_data: dict):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Validar email duplicado si viene en la actualización
    if "email" in user_data:
        for u in users_db:
            if u["id"] != user_id and u["email"] == user_data["email"]:
                raise HTTPException(
                    status_code=400,
                    detail="El email ya está registrado por otro usuario"
                )
    user.update(user_data)
    return user

def delete_user(user_id: int):
    global users_db
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    users_db = [u for u in users_db if u["id"] != user_id]
    return user