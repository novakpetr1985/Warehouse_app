from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# -------------------------
# MATERIAL
# -------------------------
class MaterialCreate(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    qr_code: str
    location: str
    note: str | None = None


class MaterialResponse(MaterialCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MaterialUpdate(BaseModel):
    name: str
    quantity: int
    qr_code: str
    location: str
    note: str | None = None


class MaterialPatch(BaseModel):
    name: str | None = None
    quantity: int | None = Field(default=None, ge=0)
    qr_code: str | None = None
    location: str | None = None
    note: str | None = None



# -------------------------
# MOVEMENT
# -------------------------
class MovementCreate(BaseModel):
    material_id: int
    movement_type: Literal["IN", "OUT"]
    quantity: int = Field(gt=0)
    from_location: str | None = None
    to_location: str | None = None
    note: str | None = None


class MovementResponse(MovementCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MovementUpdate(BaseModel):
    material_id: int
    movement_type: Literal["IN", "OUT"]
    quantity: int = Field(gt=0)
    from_location: str | None = None
    to_location: str | None = None
    note: str | None = None


class MovementPatch(BaseModel):
    material_id: int | None = None
    movement_type: Literal["IN", "OUT"] | None = None
    quantity: int | None = Field(default=None, gt=0)
    from_location: str | None = None
    to_location: str | None = None
    note: str | None = None
