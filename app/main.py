from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems API",
    description="API REST para la gestión de usuarios del sistema device_systems. CRUD completo, validaciones, manejo de errores y documentación interactiva.",
    version="2.0.0",
    contact={
        "name": "Tu Nombre",
        "email": "tuemail@ejemplo.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router, prefix="/api/v1", tags=["Users"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a device_systems API v2"}