from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, check_db

router = APIRouter(tags=["Health"])


# ---------------------------
# BASIC HEALTH
# ---------------------------
@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Warehouse API"
    }


# ---------------------------
# LIVENESS (process running)
# ---------------------------
@router.get("/health/live")
def live():
    return {
        "status": "alive"
    }


# ---------------------------
# READINESS (DB + dependencies)
# ---------------------------
@router.get("/health/ready")
def ready(db: Session = Depends(get_db)):
    
    db_ok = check_db()

    if not db_ok:
        raise HTTPException(
            status_code=503,
            detail="Database not ready"
        )

    return {
        "status": "ready",
        "database": True
    }