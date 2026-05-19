from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.material_service import get_materials
from app import crud, schemas

router = APIRouter(prefix="/materials", tags=["Materials"])


# -------------------------
# GET ALL
# -------------------------
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_materials(db)


# -------------------------
# GET ONE
# -------------------------
@router.get("/{material_id}")
def get_one(material_id: int, db: Session = Depends(get_db)):
    return crud.get_material(db, material_id)


# -------------------------
# CREATE
# -------------------------
@router.post("/")
def create(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material(db, material)