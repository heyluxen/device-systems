from fastapi import Depends, HTTPException, status
from app.services.user_service import get_user_by_id

def get_user_or_404(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user
