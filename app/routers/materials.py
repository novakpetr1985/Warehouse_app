from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.material_service import get_materials
from app import crud, schemas

router = APIRouter(prefix="/materials", tags=["Materials"])


# -------------------------
# GET ALL
# -------------------------
@router.get("/")
def list_materials(db: Session = Depends(get_db)):
    return get_materials(db)


# -------------------------
# GET ONE
# -------------------------
@router.get("/{material_id}")
def get_material(material_id: int, db: Session = Depends(get_db)):
    return crud.get_material(db, material_id)


# -------------------------
# CREATE
# -------------------------
@router.post("/")
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material(db, material)


# -------------------------
# UPDATE
# -------------------------
@router.put("/{material_id}")
def update_material(
    material_id: int,
    material: schemas.MaterialUpdate,
    db: Session = Depends(get_db)
):

    obj = crud.update_material(db, material_id, material)

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    return obj


# -------------------------
# PATCH
# -------------------------
@router.patch("/{material_id}")
def patch_material(
    material_id: int,
    data: schemas.MaterialPatch,
    db: Session = Depends(get_db)
):

    obj = crud.patch_material(db, material_id, data)

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    return obj


# -------------------------
# DELETE ONE
# -------------------------
@router.delete("/{material_id}")
def delete_material(db, material_id: int):
    obj = db.query(models.Material).filter(
        models.Material.id == material_id
    ).first()

    if obj:
        db.delete(obj)
        db.commit()

    return obj


# -------------------------
# DELETE ALL - SECRET KEY REQUIRED 
# -------------------------
@router.delete("/")
def delete_all_materials(db):
    db.query(models.Material).delete()
    db.commit()