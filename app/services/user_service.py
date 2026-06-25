from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch

# Crear usuario
def create_user(db: Session, user_data: UserCreate):
    # Verificar email duplicado
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    db_user = User(**user_data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Listar usuarios con filtros opcionales
def get_users(db: Session, role: str = None, is_active: bool = None):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()

# Obtener usuario por ID (o None)
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Obtener usuario o lanzar 404
def get_user_or_404(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Actualizar completamente (PUT)
def update_user_complete(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user_or_404(db, user_id)
    # Verificar email duplicado (si cambia)
    if user_data.email != user.email:
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado por otro usuario"
            )
    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active
    db.commit()
    db.refresh(user)
    return user

# Actualizar parcialmente (PATCH)
def update_user_partial(db: Session, user_id: int, user_data: UserPatch):
    user = get_user_or_404(db, user_id)
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar"
        )
    # Verificar email duplicado solo si se envía email nuevo
    if "email" in update_data and update_data["email"] != user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="El email ya está registrado por otro usuario"
            )
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# Eliminar usuario
def delete_user(db: Session, user_id: int):
    user = get_user_or_404(db, user_id)
    db.delete(user)
    db.commit()
    return True