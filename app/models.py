from sqlalchemy import Column, Integer, String
from app.database import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    qr_code = Column(String)
    location = Column(String)
    note = Column(String)