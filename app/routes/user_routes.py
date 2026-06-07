from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, RoleEnum
from app.services.user_service import (
    get_all_users, create_user, update_user_complete,
    update_user_partial, delete_user
)
from app.dependencies.user_dependencies import get_user_or_404

router = APIRouter()

@router.get(
    "/users",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Obtiene la lista de usuarios. Puede filtrar por rol y estado activo.",
    response_description="Lista de usuarios"
)
def list_users(
    role: Optional[RoleEnum] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    return get_all_users(role, is_active)

@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna un usuario específico según su ID.",
    response_description="Datos del usuario"
)
def get_user(user: dict = Depends(get_user_or_404)):
    return user

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario. Valida nombre, email y rol.",
    response_description="Usuario creado"
)
def create_new_user(user_data: UserCreate):
    return create_user(user_data)

@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente un usuario",
    description="Reemplaza todos los datos de un usuario existente.",
    response_description="Usuario actualizado"
)
def update_complete_user(
    user_id: int,
    user_data: UserCreate,
    user_exist: dict = Depends(get_user_or_404)
):
    return update_user_complete(user_id, user_data)

@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente un usuario",
    description="Modifica solo los campos enviados en la petición.",
    response_description="Usuario actualizado"
)
def update_partial_user(
    user_id: int,
    user_data: UserUpdate,
    user_exist: dict = Depends(get_user_or_404)
):
    # Filtrar solo los campos que fueron enviados (excluir None)
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )
    return update_user_partial(user_id, update_data)

@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente. No retorna contenido.",
    response_description="Usuario eliminado (sin contenido)"
)
def delete_user_endpoint(user_exist: dict = Depends(get_user_or_404)):
    delete_user(user_exist["id"])
    return None