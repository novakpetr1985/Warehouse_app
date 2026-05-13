from fastapi import FastAPI

app = FastAPI(title="Warehouse Traceability API")

@app.get("/")
async def root():
    return {"status": "running"}