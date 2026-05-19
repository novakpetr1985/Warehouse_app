from app import crud


# -------------------------
# GET ALL (business layer)
# -------------------------
def get_materials(db):
    materials = crud.get_materials(db)

    return {
        "count": len(materials),
        "items": materials
    }