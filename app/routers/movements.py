from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud
from app import schemas
from app.services.movement_service import process_movement

router = APIRouter(prefix="/movements", tags=["Movements"])


# -------------------------
# GET ALL MOVEMENTS
# -------------------------
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return crud.get_movements(db)


# -------------------------
# GET BY ID - ONE MOVEMENT
# -------------------------
@router.get("/{movement_id}")
def get_one(movement_id: int, db: Session = Depends(get_db)):
    return crud.get_movement(db, movement_id)


# -------------------------
# CREATE MOVEMENT
# -------------------------
@router.post("/")
def create_movement(movement: schemas.MovementCreate, db: Session = Depends(get_db)):
    return process_movement(db, movement)