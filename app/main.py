from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel


from app.database import engine, Base, SessionLocal
from app import models


app = FastAPI(title="Warehouse API")


# vytvoření tabulek v DB
Base.metadata.create_all(bind=engine)


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REQUEST SCHEMA (JSON input)
class MaterialCreate(BaseModel):
    name: str
    quantity: int
    qr_code: str
    location: str
    note: str


# ROOT
@app.get("/")
def root():
    return {"status": "running"}


# CREATE (DB)
@app.post("/materials")
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    db_material = models.Material(
        name=material.name,
        quantity=material.quantity,
        qr_code=material.qr_code,
        location=material.location,
        note=material.note
    )

    db.add(db_material)
    db.commit()
    db.refresh(db_material)

    return db_material


# READ ALL (DB)
@app.get("/materials")
def get_materials(db: Session = Depends(get_db)):
    return db.query(models.Material).all()