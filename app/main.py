from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(title="Device Systems API", version="1.0")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Bienvenido a Device Systems API"}