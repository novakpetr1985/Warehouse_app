from pydantic import BaseModel


# =========================
# MATERIAL
# =========================
class MaterialCreate(BaseModel):
    name: str
    quantity: int
    qr_code: str
    location: str
    note: str | None = None


class MaterialResponse(MaterialCreate):
    id: int

    class Config:
        from_attributes = True


# =========================
# MOVEMENT
# =========================
class MovementCreate(BaseModel):
    material_id: int
    movement_type: str  # IN / OUT
    quantity: int
    from_location: str | None = None
    to_location: str | None = None
    note: str | None = None


class MovementResponse(MovementCreate):
    id: int

    class Config:
        from_attributes = True