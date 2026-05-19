from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, check_db, check_tables

router = APIRouter(tags=["Health"])


# ---------------------------
# BASIC HEALTH
# ---------------------------
@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Warehouse API"
    }


# ---------------------------
# LIVENESS (process running)
# ---------------------------
@router.get("/health/live")
def liveness_check():
    return {
        "status": "alive"
    }



@router.get("/health/ready")
def readiness_check(db: Session = Depends(get_db)):

    db_ok = check_db()
    tables_ok, missing = check_tables()

    if not db_ok:
        raise HTTPException(
            status_code=503,
            detail="Database not ready"
        )

    if not tables_ok:
        raise HTTPException(
            status_code=503,
            detail=f"Missing tables: {missing}"
        )

    return {
        "status": "ready",
        "database": True,
        "tables": "ok"
    }