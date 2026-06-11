from fastapi import FastAPI
from app.routes import user_routes
from app.database.connection import create_tables

# Crear tablas al iniciar la aplicación
create_tables()

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios con persistencia SQLAlchemy",
    version="3.0.0",
    contact={"name": "Tu Nombre", "email": "tuemail@ejemplo.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(user_routes.router, prefix="/api/v1", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Bienvenido a device_systems API con SQLAlchemy"}