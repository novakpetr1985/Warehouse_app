from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud

router = APIRouter(prefix="/movements", tags=["Movements"])


# -------------------------
# GET ALL MOVEMENTS
# -------------------------
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return crud.get_movements(db)


# -------------------------
# GET BY ID
# -------------------------
@router.get("/{movement_id}")
def get_one(movement_id: int, db: Session = Depends(get_db)):
    return crud.get_movement(db, movement_id)