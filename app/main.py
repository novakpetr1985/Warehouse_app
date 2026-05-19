from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.routers import health


from app.database import engine, Base, SessionLocal
from app import models


app = FastAPI(title="Warehouse API")
app.include_router(health.router)

# vytvoření tabulek v DB
Base.metadata.create_all(bind=engine)


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# SCHEMAS
# =========================

class MaterialCreate(BaseModel):
    name: str
    quantity: int
    qr_code: str
    location: str
    note: str


class MovementCreate(BaseModel):
    material_id: int
    movement_type: str   # IN / OUT
    quantity: int
    from_location: str | None = None
    to_location: str | None = None
    note: str | None = None


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {"status": "running"}


# =========================
# MATERIALS
# =========================

@app.post("/materials")
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    db_material = models.Material(
        name=material.name,
        quantity=material.quantity,
        qr_code=material.qr_code,
        location=material.location,
        note=material.note
    )

    db.add(db_material)
    db.commit()
    db.refresh(db_material)

    return db_material


@app.get("/materials")
def get_materials(db: Session = Depends(get_db)):
    return db.query(models.Material).all()


# =========================
# MOVEMENTS
# =========================

@app.post("/movements")
def create_movement(movement: MovementCreate, db: Session = Depends(get_db)):

    # najdi material
    material = db.query(models.Material).filter(
        models.Material.id == movement.material_id
    ).first()

    if not material:
        return {"error": "Material not found"}

    # IN - příjem
    if movement.movement_type == "IN":
        material.quantity += movement.quantity

    # OUT - výdej
    elif movement.movement_type == "OUT":

        if material.quantity < movement.quantity:
            return {"error": "Not enough stock"}

        material.quantity -= movement.quantity

    else:
        return {"error": "Invalid movement type (use IN or OUT)"}

    # uložit movement do DB
    db_movement = models.Movement(
        material_id=movement.material_id,
        movement_type=movement.movement_type,
        quantity=movement.quantity,
        from_location=movement.from_location,
        to_location=movement.to_location,
        note=movement.note
    )

    db.add(db_movement)

    db.commit()
    db.refresh(material)
    db.refresh(db_movement)

    return {
        "material": material,
        "movement": db_movement
    }