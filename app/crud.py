from sqlalchemy.orm import Session
from app import models, schemas


# -------------------------
# GET MATERIALS - READ ALL
# -------------------------
def get_materials(db: Session):
    return db.query(models.Material).all()


# -------------------------
# GET MATERIALS - READ ONE
# -------------------------
def get_material(db: Session, material_id: int):
    return db.query(models.Material).filter(
        models.Material.id == material_id
    ).first()


# -------------------------
# POST MATERIALS CREATE
# -------------------------
def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material



# -------------------------
# GET MOVEMENTS - READ ALL
# -------------------------
def get_movements(db):
    return db.query(models.Movement).all()


# -------------------------
# GET MOVEMENTS - READ ONE
# -------------------------
def get_movement(db, movement_id: int):
    return db.query(models.Movement).filter(
        models.Movement.id == movement_id
    ).first()


# -------------------------
# POST MOVEMENTS CREATE
# -------------------------
def create_movement(db, movement):
    db_movement = models.Movement(**movement.dict())
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement