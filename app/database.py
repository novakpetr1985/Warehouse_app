from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite databáze (soubor)
DATABASE_URL = "sqlite:///./warehouse.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# -------------------------------------------------
# DB SESSION HELPER (standard FastAPI pattern)
# -------------------------------------------------
def get_db():
    """
    Dependency pro FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# HEALTH CHECK - DB CONNECTIVITY
# -------------------------------------------------
def check_db():
    """
    Ověří, že databáze odpovídá (lightweight test)
    Používá SELECT 1 (standard)
    """
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
    finally:
        db.close()