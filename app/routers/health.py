from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, check_db, check_tables, engine

router = APIRouter(tags=["Health"])


# =========================
# BASIC HEALTH CHECK
# =========================
@router.get("/health")
def health():
    """
    Basic service check.
    Returns only whether API is running.
    """
    return {
        "status": "ok",
        "service": "Warehouse API"
    }


# =========================
# LIVENESS PROBE
# =========================
@router.get("/health/live")
def live():
    """
    Liveness probe.
    Used to check if application process is running.
    """
    return {
        "status": "alive"
    }


# =========================
# READINESS PROBE
# =========================
@router.get("/health/ready")
def ready(db: Session = Depends(get_db)):
    """
    Readiness probe.
    Checks:
    - database connection
    - required tables existence
    """

    # 1) DB connection check
    db_ok = check_db()

    # 2) tables check (materials, movements)
    tables_ok, tables_status = check_tables(engine)

    # =========================
    # DB NOT READY
    # =========================
    if not db_ok:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "DB not ready",
                "database": "FAIL",
                "tables": tables_status
            }
        )

    # =========================
    # TABLES NOT READY
    # =========================
    if not tables_ok:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "Tables missing",
                "database": "OK",
                "tables": tables_status
            }
        )

    # =========================
    # ALL OK
    # =========================
    return {
        "status": "ready",
        "database": "OK",
        "tables": tables_status
    }