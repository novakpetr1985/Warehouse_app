from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Warehouse Traceability API")


# Fake databáze
materials = []


# Datový model
class Material(BaseModel):
    name: str
    quantity: int
    note: str


@app.get("/")
async def root():
    return {"status": "running"}


# CREATE
@app.post("/materials")
async def create_material(material: Material):
    materials.append(material)
    return {
        "message": "Material created",
        "data": material
    }


# READ
@app.get("/materials")
async def get_materials():
    return materials