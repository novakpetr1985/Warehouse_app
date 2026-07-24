import os

from fastapi import APIRouter, Depends, Header, HTTPException
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
# DELETE ALL - API KEY REQUIRED
# Must be declared before /{material_id} so that "all" is not parsed as an ID.
# -------------------------
@router.delete("/all")
def delete_all_materials(
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None),
):
    expected_key = os.getenv("WAREHOUSE_API_KEY")
    if not expected_key or x_api_key != expected_key:
        raise HTTPException(status_code=403, detail="Unauthorized")

    crud.delete_all_materials(db)
    return {"status": "all deleted"}


# -------------------------
# GET ONE
# -------------------------
@router.get("/{material_id}")
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = crud.get_material(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


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
def delete_material(material_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_material(db, material_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"status": "deleted"}
