from fastapi import HTTPException

from app import crud, models


def process_movement(db, movement):

    # najdi material
    material = db.query(models.Material).filter(
        models.Material.id == movement.material_id
    ).first()

    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # IN (příjem)
    if movement.movement_type == "IN":
        material.quantity += movement.quantity

    # OUT (výdej)
    elif movement.movement_type == "OUT":

        if material.quantity < movement.quantity:
            raise HTTPException(status_code=409, detail="Not enough stock")

        material.quantity -= movement.quantity

    else:
        raise HTTPException(status_code=422, detail="Invalid movement type")

    # ulož movement
    db_movement = crud.create_movement(db, movement)

    db.commit()
    db.refresh(material)

    return {
        "material": material,
        "movement": db_movement
    }
