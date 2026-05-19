from sqlalchemy.orm import Session
from app import models, schemas


# -------------------------
# GET - MATERIALS - READ ALL
# -------------------------
def get_materials(db: Session):
    return db.query(models.Material).all()


# -------------------------
# GET - MATERIALS - READ ONE
# -------------------------
def get_material(db: Session, material_id: int):
    return db.query(models.Material).filter(
        models.Material.id == material_id
    ).first()


# -------------------------
# POST - MATERIALS - CREATE
# -------------------------
def create_material(db: Session, material: schemas.MaterialCreate):
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


# -------------------------
# PUT - MATERIALS - UPDATE
# -------------------------
def update_material(db, material_id: int, material):

    db_material = db.query(models.Material).filter(
        models.Material.id == material_id
    ).first()

    if not db_material:
        return None

    db_material.name = material.name
    db_material.quantity = material.quantity
    db_material.qr_code = material.qr_code
    db_material.location = material.location
    db_material.note = material.note

    db.commit()
    db.refresh(db_material)

    return db_material


# -------------------------
# DELETE - MATERIALS - ONE
# -------------------------
def delete_material(db, material_id: int):
    obj = db.query(models.Material).filter(
        models.Material.id == material_id
    ).first()

    if obj:
        db.delete(obj)
        db.commit()

    return obj

# -------------------------
# DELETE - MATERIALS - ALL
# -------------------------
def delete_all_materials(db):
    db.query(models.Material).delete()
    db.commit()


# -------------------------
# GET - MOVEMENTS - READ ALL
# -------------------------
def get_movements(db):
    return db.query(models.Movement).all()


# -------------------------
# GET - MOVEMENTS - READ ONE
# -------------------------
def get_movement(db, movement_id: int):
    return db.query(models.Movement).filter(
        models.Movement.id == movement_id
    ).first()


# -------------------------
# POST - MOVEMENTS - CREATE
# -------------------------
def create_movement(db, movement):
    db_movement = models.Movement(**movement.dict())
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement


# -------------------------
# PUT - MOVEMENTS - UPDATE
# -------------------------
def update_movement(db, movement_id: int, movement):

    db_movement = db.query(models.Movement).filter(
        models.Movement.id == movement_id
    ).first()

    if not db_movement:
        return None

    db_movement.material_id = movement.material_id
    db_movement.movement_type = movement.movement_type
    db_movement.quantity = movement.quantity
    db_movement.from_location = movement.from_location
    db_movement.to_location = movement.to_location
    db_movement.note = movement.note

    db.commit()
    db.refresh(db_movement)

    return db_movement


# -------------------------
# DELETE - MOVEMENTS - ONE
# -------------------------
def delete_movement(db, movement_id: int):
    obj = db.query(models.Movement).filter(
        models.Movement.id == movement_id
    ).first()

    if obj:
        db.delete(obj)
        db.commit()

    return obj

# -------------------------
# DELETE - MOVEMENTS - ALL
# -------------------------
def delete_all_movements(db):
    db.query(models.Movement).delete()
    db.commit()