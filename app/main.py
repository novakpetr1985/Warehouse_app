from fastapi import FastAPI
from app.routers import health, materials, movements

from app.database import engine, Base

app = FastAPI(title="Warehouse API")


# =========================
# ROUTERS
# =========================
app.include_router(health.router)
app.include_router(materials.router)
app.include_router(movements.router)


# =========================
# DB INIT (prozatím OK)
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "running"}