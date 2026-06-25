from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.database.connection import create_tables
from app.routes import user_routes, device_routes, loan_routes
from app.auth import auth_routes
from app.middlewares.request_middleware import RequestMiddleware
from app.dependencies.rate_limit_dependency import limiter
from dotenv import load_dotenv

load_dotenv()

create_tables()

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos con autenticación JWT, middleware, CORS y rate limiting.",
    version="3.0.0",
    contact={
        "name": "Tu Nombre",
        "email": "tuemail@ejemplo.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Auth", "description": "Autenticación y registro de usuarios"},
        {"name": "Users", "description": "Gestión de usuarios (protegido)"},
        {"name": "Devices", "description": "Gestión de dispositivos (protegido)"},
        {"name": "Loans", "description": "Gestión de préstamos (protegido)"},
    ]
)

app.add_middleware(RequestMiddleware)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_routes.router, prefix="/api/v1", tags=["Auth"])
app.include_router(user_routes.router, prefix="/api/v1", tags=["Users"])
app.include_router(device_routes.router, prefix="/api/v1", tags=["Devices"])
app.include_router(loan_routes.router, prefix="/api/v1", tags=["Loans"])

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a device_systems API - Versión Segura",
        "docs": "/docs",
        "redoc": "/redoc"
    }