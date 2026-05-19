from sqlalchemy import create_engine, text, inspect
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


# -------------------------------------------------
# HEALTH CHECK - REAL STAV DB TABLES
# -------------------------------------------------
def check_tables():
    """
    Ověří, že základní tabulky existují
    """
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        required_tables = ["materials", "movements"]

        missing = [t for t in required_tables if t not in tables]

        if missing:
            return False, missing

        return True, []
    except Exception:
        return False, ["inspection_failed"]
    

# -------------------------------------------------
# CHECK DB TABLES
# -------------------------------------------------
from sqlalchemy import inspect

def check_tables(engine):
    inspector = inspect(engine)

    required_tables = ["materials", "movements"]

    existing_tables = inspector.get_table_names()

    result = {}

    for table in required_tables:
        if table in existing_tables:
            result[table] = "OK"
        else:
            result[table] = "MISSING"

    all_ok = all(v == "OK" for v in result.values())

    return all_ok, result