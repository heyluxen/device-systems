from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.auth.auth_service import register_user, authenticate_user, create_user_token
from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserAuthResponse
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.rate_limit_dependency import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de usuario",
    description="Crea un nuevo usuario con contraseña segura."
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    return register_user(db, user_data)

@router.post(
    "/login",
    response_model=Token,
    summary="Inicio de sesión",
    description="Autentica al usuario y retorna un token JWT."
)
@limiter.limit("5/minute")
def login(
    request: Request,
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_user_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get(
    "/me",
    response_model=UserAuthResponse,
    summary="Obtener perfil propio",
    description="Retorna los datos del usuario autenticado."
)
def get_me(current_user = Depends(get_current_user)):
    return current_user