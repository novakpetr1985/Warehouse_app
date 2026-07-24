import os

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.services.movement_service import process_movement

router = APIRouter(prefix="/movements", tags=["Movements"])

# -------------------------
# GET ALL
# -------------------------
@router.get("/")
def get_movements(db: Session = Depends(get_db)):
    return crud.get_movements(db)


# -------------------------
# DELETE ALL - API KEY REQUIRED
# Must be declared before /{movement_id} so that "all" is not parsed as an ID.
# -------------------------
@router.delete("/all")
def delete_all_movements(
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None),
):
    expected_key = os.getenv("WAREHOUSE_API_KEY")
    if not expected_key or x_api_key != expected_key:
        raise HTTPException(status_code=403, detail="Unauthorized")

    crud.delete_all_movements(db)
    return {"status": "all deleted"}


# -------------------------
# GET ONE
# -------------------------
@router.get("/{movement_id}")
def get_movement(movement_id: int, db: Session = Depends(get_db)):
    movement = crud.get_movement(db, movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movement not found")
    return movement


# -------------------------
# CREATE
# -------------------------
@router.post("/")
def create_movement(
    movement: schemas.MovementCreate,
    db: Session = Depends(get_db)
):
    return process_movement(db, movement)


# -------------------------
# UPDATE
# -------------------------
@router.put("/{movement_id}")
def update_movement(
    movement_id: int,
    movement: schemas.MovementUpdate,
    db: Session = Depends(get_db)
):

    obj = crud.update_movement(db, movement_id, movement)

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )

    return obj


# -------------------------
# PATCH
# -------------------------
@router.patch("/{movement_id}")
def patch_movement(
    movement_id: int,
    data: schemas.MovementPatch,
    db: Session = Depends(get_db)
):

    obj = crud.patch_movement(db, movement_id, data)

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )

    return obj


# -------------------------
# DELETE ONE
# -------------------------
@router.delete("/{movement_id}")
def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db)
):

    obj = crud.delete_movement(db, movement_id)

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )

    return {"status": "deleted"}
