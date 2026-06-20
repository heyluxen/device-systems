from fastapi import FastAPI
from app.database.connection import create_tables
from app.routes import user_routes, device_routes, loan_routes

create_tables()

app = FastAPI(
    title="device_systems API",
    description="API con usuarios, dispositivos y préstamos (relaciones y migraciones)",
    version="4.0.0",
    contact={"name": "Tu Nombre", "email": "tuemail@ejemplo.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(user_routes.router, prefix="/api/v1", tags=["Users"])
app.include_router(device_routes.router, prefix="/api/v1", tags=["Devices"])
app.include_router(loan_routes.router, prefix="/api/v1", tags=["Loans"])

@app.get("/")
def root():
    return {"message": "Bienvenido a device_systems API con relaciones y Alembic"}